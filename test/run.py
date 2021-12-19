from db import DatabaseConnection

DB = DatabaseConnection()
DB._reset_database()

expected = [
    { 'name': 'Plymouth', 'telephone': '01752 000000' },
    { 'name': 'Exeter', 'telephone': '01392 000000' },
]

with open("database_query.sql", 'r') as sql_file:
    sql_string = sql_file.read()
    actual = DB.select(sql_string)

assert actual == expected
print("Passed!")

