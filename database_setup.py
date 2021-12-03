from app.db import DatabaseConnection

if __name__ == "__main__":
    # noinspection PyProtectedMember
    DatabaseConnection()._reset_database()
