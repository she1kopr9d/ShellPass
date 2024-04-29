import sqlalchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric, Sequence, BigInteger

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger(), primary_key=True)

class Role(Base):
    __tablename__ = "roles"
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(String(), unique=True)
    signatures = Column(ARRAY(String))

    def sort(signs, usl):
        ok = []
        for sign in signs:
            if usl(sign):
                ok.append(sign)
        return ok

    def check(mainsign: str, signs: list) -> bool:
        msa = mainsign.split(":")
        for i in range(4):
            signs = Role.sort(signs, lambda sign: sign.split(":")[i] == "0" or sign.split(":")[i] == msa[i])
        return len(signs) != 0
    
    def toJson(self):
        return {
            "id" : self.id, 
            "name" : self.name,
            "permission" : self.signatures
        }

class UserToRole(Base):
    __tablename__ = "userstoroles"
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    user_id = Column(BigInteger(), ForeignKey("users.id"), nullable=False)
    role_id = Column(BigInteger(), ForeignKey("roles.id"), nullable=False)

class Category(Base):
    __tablename__ = "categories"
    seq = Sequence('article_id_seq', start=1, increment=True)
    id = Column('id', BigInteger(), seq, server_default=seq.next_value(), primary_key=True)
    name = Column(String(), unique=True)

class Account(Base):
    __tablename__ = "accounts"
    seq = Sequence('article_id_seq', start=1, increment=True)
    id = Column('id', BigInteger(), seq, server_default=seq.next_value(), primary_key=True)
    category_id = Column(BigInteger(), ForeignKey("categories.id"), nullable=False)
    name = Column(String(), unique=True)
    site = Column(String())
    login = Column(String())
    email = Column(String())
    password = Column(String())

class DataBase:    
    def __init__(self, db_id: int) -> None:
        self.__db_id = db_id
        self.__engine = create_engine(f"postgresql://server:server_connect@shellpass_db/{self.__db_id}_organization")
        self.__session = sessionmaker(self.__engine)
        Base.metadata.create_all(self.__engine)
        
    @property
    def Session(self):
        return self.__session()

