from sqlalchemy import create_engine, select
from sqlalchemy_utils import database_exists, create_database

from database.client_db.database import DataBase, User as Local_User, Role, Category, UserToRole, Account

# Move
ALL = 0
ADD = 1
CREATE = 2
DELETE = 3
EDIT = 4
VIEW = 5

# Object
ALL_OBJECTS = 0
ACCOUNT = 1
CATEGORY = 2
ORGANIZATION = 3
ROLE = 4
USER = 5

# Roles
OWNER = "Owner"

class Signature:
    def __init__(self, category_id: int = 0, account_id: int = 0, move: int = 0, obj: int = 0):
        self.__category_id = category_id
        self.__account_id = account_id
        self.__move = move
        self.__obj = obj

    def __str__(self):
        return f"{self.__category_id}:{self.__account_id}:{self.__move}:{self.__obj}"

class Utils_IO:
    def create_database(organization_id: int, creator: dict):
        Database_IO.create(organization_id)
        Role_IO.create_admin_role(organization_id)
        User_IO.create(organization_id, creator)
        admin_role: Role = Role_IO.get(organization_id, OWNER)
        User_IO.add_role(organization_id, creator, admin_role)

class Database_IO:
    
    def create(organization_id: int):
        engine = create_engine(f"postgresql://server:server_connect@shellpass_db/{organization_id}_organization")
        if not database_exists(engine.url):
            create_database(engine.url)

    def connect(organization_id: int) -> DataBase:
        database = DataBase(organization_id)
        return database
    
class Role_IO:

    def delete(organization_id: int, role_id: int):
        database: DataBase = Database_IO.connect(organization_id)
        with database.Session as conn:
            role = conn.scalar(select(Role).where(Role.id == role_id))
            conn.delete(role)
            conn.commit()

    def create(organization_id: int, name: str, signatures: list[Signature]):
        database: DataBase = Database_IO.connect(organization_id)
        with database.Session as conn:
            role = Role(name=name, signatures=list(map(str, signatures)))
            conn.add(role)
            conn.commit()
    
    def get(organization_id: int, name: str):
        database: DataBase = Database_IO.connect(organization_id)
        with database.Session as conn:
            role = conn.scalar(select(Role).where(Role.name == name))
            return role

    def get_all(organization_id: int):
        database: DataBase = Database_IO.connect(organization_id)
        with database.Session as conn:
            roles = conn.scalars(select(Role)).all()
            return roles

    def create_admin_role(organization_id: int):
        Role_IO.create(organization_id, OWNER, [Signature()])

    def edit_name(organization_id: int, role_id: int, name: str):
        database: DataBase = Database_IO.connect(organization_id)
        with database.Session as conn:
            role = conn.scalar(select(Role).where(Role.id == role_id))
            role.name = name
            conn.commit()

class Category_IO:

    def create(organization_id: int, category_name: str):
        database: DataBase = Database_IO.connect(organization_id)
        with database.Session as conn:
            category = Category(name=category_name)
            conn.add(category)
            conn.commit()

    def get(organization_id: int, category_id: int):
        database: DataBase = Database_IO.connect(organization_id)
        with database.Session as conn:
            category = conn.scalar(select(Category).where(Category.id == category_id))
            return category

class User_IO:

    def inOrganization(organization_id: int, user: dict):
        database: DataBase = Database_IO.connect(organization_id)
        with database.Session as conn:
            isOrganization = len(conn.scalars(select(Local_User).where(Local_User.id == user["id"])).all()) != 0
            conn.commit()
            return isOrganization


    def create(organization_id: int, user: dict):
        database: DataBase = Database_IO.connect(organization_id)
        with database.Session as conn:
            local_user = Local_User(id=user["id"])
            conn.add(local_user)
            conn.commit()

    def add_role(organization_id: int, user: dict, role: Role):
        database: DataBase = Database_IO.connect(organization_id)
        with database.Session as conn:
            utr = UserToRole(user_id=user["id"], role_id=role.id)
            conn.add(utr)
            conn.commit()
    
    def get_user_permission(organization_id: int, user: dict):
        database: DataBase = Database_IO.connect(organization_id)
        with database.Session as conn:
            utrs = conn.scalars(select(UserToRole).where(UserToRole.user_id == user["id"])).all()
            role_ids = [utr.role_id for utr in utrs]
            roles = conn.scalars(select(Role).where(Role.id.in_(role_ids))).all()
            permission = set()
            for role in roles:
                for signature in role.signatures:
                    permission.add(signature)
            return list(permission)

class Account_IO:

    def create(organization_id: int, category_id, name: str, site: str, login: str, email: str, password: str):
        database: DataBase = Database_IO.connect(organization_id)
        with database.Session as conn:
            account = Account(category_id=category_id, name=name, site=site, login=login, email=email, password=password)
            conn.add(account)
            conn.commit()