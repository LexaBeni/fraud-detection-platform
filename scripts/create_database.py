from sqlalchemy import create_engine, text

from src.api.core.settings import settings

DATABASE_NAME = "fraud_detection"


def create_database():
    engine = create_engine(settings.database_server_url)

    try:
        with engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}`"))
            connection.commit()

            print(f"Database '{DATABASE_NAME}' is ready.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    create_database()
