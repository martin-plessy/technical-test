from db import DatabaseConnection

DB = DatabaseConnection()
DB._reset_database()

expected = [
  { 'appointment_id': 33, 'appointment_date': '2021-07-05', 'appointment_start': '09:00:00', 'appointment_end': '09:30:00',
    'practice_name': 'Exeter Vets', 'practice_phone': '01392 000000', 'practice_address': '123 Test Street, Exeter, Devon, EX1 1AA',
    'owner_id': 1, 'owner_name': 'Owen Snow', 'owner_email': 'o.snow@gmail.com', 'owner_phone': '07000 000042', 'owner_address': '123 Test Street, Teston, TS7 7CT',
    'pet_id': 1, 'pet_name':'A pet has a breed', 'pet_species': 'A (B)', 'pet_birthdate': '2020-03-24' },

  { 'appointment_id': 34, 'appointment_date': '2021-07-05', 'appointment_start': '09:00:00', 'appointment_end': '09:30:00',
    'practice_name': 'Exeter Vets', 'practice_phone': '01392 000000', 'practice_address': '123 Test Street, Exeter, Devon, EX1 1AA',
    'owner_id': 2, 'owner_name': 'Oliver Burk', 'owner_email': 'o.burk@outlook.com', 'owner_phone': '07000 001955', 'owner_address': '123 Test Street, Teston, TS7 7CT',
    'pet_id': 2, 'pet_name':'A pet has no breed', 'pet_species': 'A', 'pet_birthdate': '2020-04-23' },

  { 'appointment_id': 35, 'appointment_date': '2021-07-09', 'appointment_start': '09:30:00', 'appointment_end': '10:00:00',
    'practice_name': 'Exeter Vets', 'practice_phone': '01392 000000', 'practice_address': '123 Test Street, Exeter, Devon, EX1 1AA',
    'owner_id': 1, 'owner_name': 'Owen Snow', 'owner_email': 'o.snow@gmail.com', 'owner_phone': '07000 000042', 'owner_address': '123 Test Street, Teston, TS7 7CT',
    'pet_id': 1, 'pet_name':'A pet has a breed', 'pet_species': 'A (B)', 'pet_birthdate': '2020-03-24' },

  { 'appointment_id': 36, 'appointment_date': '2021-07-09', 'appointment_start': '09:30:00', 'appointment_end': '10:00:00',
    'practice_name': 'Exeter Vets', 'practice_phone': '01392 000000', 'practice_address': '123 Test Street, Exeter, Devon, EX1 1AA',
    'owner_id': 2, 'owner_name': 'Oliver Burk', 'owner_email': 'o.burk@outlook.com', 'owner_phone': '07000 001955', 'owner_address': '123 Test Street, Teston, TS7 7CT',
    'pet_id': 2, 'pet_name':'A pet has no breed', 'pet_species': 'A', 'pet_birthdate': '2020-04-23' },

  { 'appointment_id': 37, 'appointment_date': '2021-07-11', 'appointment_start': '10:00:00', 'appointment_end': '10:30:00',
    'practice_name': 'Exeter Vets', 'practice_phone': '01392 000000', 'practice_address': '123 Test Street, Exeter, Devon, EX1 1AA',
    'owner_id': 1, 'owner_name': 'Owen Snow', 'owner_email': 'o.snow@gmail.com', 'owner_phone': '07000 000042', 'owner_address': '123 Test Street, Teston, TS7 7CT',
    'pet_id': 1, 'pet_name':'A pet has a breed', 'pet_species': 'A (B)', 'pet_birthdate': '2020-03-24' },

  { 'appointment_id': 38, 'appointment_date': '2021-07-11', 'appointment_start': '10:00:00', 'appointment_end': '10:30:00',
    'practice_name': 'Exeter Vets', 'practice_phone': '01392 000000', 'practice_address': '123 Test Street, Exeter, Devon, EX1 1AA',
    'owner_id': 2, 'owner_name': 'Oliver Burk', 'owner_email': 'o.burk@outlook.com', 'owner_phone': '07000 001955', 'owner_address': '123 Test Street, Teston, TS7 7CT',
    'pet_id': 2, 'pet_name':'A pet has no breed', 'pet_species': 'A', 'pet_birthdate': '2020-04-23' }
]

with open("database_query.sql", 'r') as sql_file:
    sql_string = sql_file.read()
    actual = DB.select(sql_string)

assert actual == expected
print("Passed!")

