from app.db import DatabaseConnection


class AppointmentResources:

    def __init__(self):
        self.DB = DatabaseConnection()
