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

    def get_appointment(self, uid: int):
        data = self.DB.select('''
            SELECT
                appointment.uid AS appointment_uid,
                appointment.date AS appointment_date,
                appointment_timeslots.timeslot_start AS appointment_start,
                appointment_timeslots.timeslot_end AS appointment_end,
                employee.uid AS employee_uid,
                employee.name AS employee_name,
                employee_types.uid AS employee_type_uid,
                employee_types.type AS employee_type,
                practice.uid AS practice_uid,
                practice.name AS practice_name,
                practice.telephone AS practice_telephone,
                practice.address AS practice_address,
                pet.uid AS pet_uid,
                pet.name AS pet_name,
                pet.animal AS pet_animal,
                pet.breed AS pet_breed,
                pet.date_of_birth AS pet_date_of_birth,
                owner.uid AS owner_uid,
                owner.name AS owner_name,
                owner.telephone AS owner_telephone,
                appointment.reason IS NOT NULL AS appointment_is_cancelled,
                appointment.reason AS appointment_cancellation_reason,
                appointment.cancelled AS appointment_cancellation_time

            FROM appointment
                INNER JOIN appointment_timeslots ON appointment_timeslots.uid = appointment.timeslot

                INNER JOIN employee ON employee.uid = appointment.employee
                    INNER JOIN employee_types ON employee_types.uid = employee.employee_type
                    INNER JOIN practice ON practice.uid = employee.practice

                INNER JOIN pet ON pet.uid = appointment.pet
                    INNER JOIN owner ON owner.uid = pet.owner

            WHERE appointment.uid = ?;
        ''', [ uid ])

        return data[0] if data else None
