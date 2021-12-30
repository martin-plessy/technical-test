from app.db import DatabaseConnection
from datetime import date, datetime, time

class AppointmentResources:
    def __init__(self):
        self.DB = DatabaseConnection()

    def pet_exists(self, uid: int) -> bool:
        return bool(self.DB.select(''' SELECT 1 FROM pet WHERE uid = ? ''', [ uid ]))

    def employee_exists(self, uid: int) -> bool:
        return bool(self.DB.select(''' SELECT 1 FROM employee WHERE uid = ? ''', [ uid ]))

    def timeslot_exists(self, uid: int) -> bool:
        return bool(self.DB.select(''' SELECT 1 FROM appointment_timeslots WHERE uid = ? ''', [ uid ]))

    def get_timeslot_start(self, uid: int) -> time:
        slot = self.DB.select(''' SELECT timeslot_start FROM appointment_timeslots WHERE uid = ? ''', [ uid ])[0]

        return datetime.strptime(slot['timeslot_start'], '%H:%M:%S').time()

    def pet_has_appointment(self, pet: int, timeslot: int, date: date) -> bool:
        return bool(self.DB.select(''' SELECT 1 FROM appointment WHERE pet = ? AND timeslot = ? AND date = ? ''', [ pet, timeslot, date ]))

    def pet_owner_has_appointment(self, pet: int, employee: int, timeslot: int, date: date) -> bool:
        return bool(self.DB.select('''
            SELECT 1 FROM appointment
            -- 3. The appointments of those pets.
            WHERE appointment.pet IN (
                -- 2. The other pets from the owner.
                SELECT another_pet.uid FROM pet AS another_pet WHERE another_pet.owner = (
                    -- 1. The owner from the pet.
                    SELECT the_pet.owner FROM pet AS the_pet WHERE the_pet.uid = ?
                )
            )
            -- 3. The appointments of those employees.
            AND appointment.employee NOT IN (
                -- 2. The other employees of the practice.
                SELECT another_employee.uid FROM employee AS another_employee WHERE another_employee.practice = (
                    -- 1. The practice from the employee.
                    SELECT the_employee.practice FROM employee AS the_employee WHERE the_employee.uid = ?
                )
            )
            AND appointment.timeslot = ?
            AND appointment.date = ?
        ''', [ pet, employee, timeslot, date ]))

    def employee_has_appointment(self, employee: int, timeslot: int, date: date) -> bool:
        return bool(self.DB.select(''' SELECT 1 FROM appointment WHERE employee = ? AND timeslot = ? AND date = ? ''', [ employee, timeslot, date ]))

    def create_appointment(self, pet: int, employee: int, timeslot: int, date: date) -> int:
        created_uid = self.DB.insert('''
            INSERT INTO appointment (employee, pet, date, timeslot)
            VALUES (?, ?, ?, ?)
        ''', [ employee, pet, date, timeslot ])

        return created_uid
