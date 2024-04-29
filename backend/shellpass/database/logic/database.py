from database.client_db.requests import Utils_IO

def create(
    organization_id: int,
    user: dict):

    Utils_IO.create_database(
        organization_id = organization_id,
        creator = user
    )