from sqlmodel import Session

from dineswap.models import Restaurant
from dineswap.db import engine, create_db_tables


def create_test_data():
    foodopolis = Restaurant(
        name="Foodopolis",
        address="261 Ogui Rd, opposite Fire Service, GRA, Enugu",
        image="https://asset.cloudinary.com/melodyogonna/7db029f84051b9c7523990d6028feb19",
    )
    octopus = Restaurant(
        name="Octopus",
        address="21A Nza St, Independence Layout, Enugu",
        image="https://asset.cloudinary.com/melodyogonna/2d12b9048eeb08d219142c34ed8fbe22",
    )
    kilimanjaro = Restaurant(
        name="kilimanjaro",
        address="Enugu Mall, Independence Layout, Enugu",
        image="https://asset.cloudinary.com/melodyogonna/5841302c91c3d579230887e0359c77d0",
    )
    ntachi = Restaurant(
        name="Ntachi-Osa",
        address="97 Chime Ave, New Haven, Enugu 400102, Enugu",
        image="https://asset.cloudinary.com/melodyogonna/a3cbb11038ec5dffb87686f83306f27a",
    )
    with Session(engine) as session:
        session.add_all([foodopolis, octopus, kilimanjaro, ntachi])
        session.commit()


if __name__ == "__main__":
    create_db_tables()
    create_test_data()

