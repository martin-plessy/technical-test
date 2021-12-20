CREATE TABLE IF NOT EXISTS employee_types (
    uid INTEGER PRIMARY KEY,
    type VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS owner (
    uid INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    telephone VARCHAR NOT NULL,
    address VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS pet (
    uid INTEGER PRIMARY KEY,
    owner INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    animal VARCHAR NOT NULL,
    breed VARCHAR,
    date_of_birth DATE NOT NULL,
    CONSTRAINT owner_fkey FOREIGN KEY(owner) REFERENCES owner(uid)
);

CREATE TABLE IF NOT EXISTS appointment_timeslots (
    uid INTEGER PRIMARY KEY,
    timeslot_start TIME NOT NULL,
    timeslot_end TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS employee (
    uid INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    telephone VARCHAR NOT NULL,
    employee_type INTEGER NOT NULL,
    CONSTRAINT employee_type_fkey FOREIGN KEY(employee_type) REFERENCES employee_types(uid)
);

CREATE TABLE IF NOT EXISTS practice (
    uid INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    telephone VARCHAR NOT NULL,
    manager INTEGER NOT NULL,
    address VARCHAR NOT NULL,
    branch VARCHAR NOT NULL,
    CONSTRAINT manager_fkey FOREIGN KEY(manager) REFERENCES employee(uid)
);

ALTER TABLE employee ADD COLUMN practice INTEGER REFERENCES practice(uid);

CREATE TABLE IF NOT EXISTS appointment (
    uid INTEGER PRIMARY KEY,
    employee INTEGER NOT NULL,
    pet INTEGER NOT NULL,
    date DATE NOT NULL,
    timeslot INTEGER NOT NULL,
    reason VARCHAR,
    cancelled TIMESTAMP,
    CONSTRAINT pet_fkey FOREIGN KEY(pet) REFERENCES pet(uid),
    CONSTRAINT employee_fkey FOREIGN KEY(employee) REFERENCES employee(uid),
    CONSTRAINT timeslot_fkey FOREIGN KEY(timeslot) REFERENCES appointment_timeslots(uid)
);

-- TEST DATA

-- Pets with and without breed:

INSERT INTO pet
(owner, name, animal, breed, date_of_birth)
VALUES
(1, 'A pet has a breed', 'A', 'B', '2020-03-24'),
(2, 'A pet has no breed', 'A', NULL, '2020-04-23');

INSERT INTO owner
(name, email, telephone, address)
VALUES
('Owen Snow', 'o.snow@gmail.com', '07000 000042', '123 Test Street, Teston, TS7 7CT'),
('Oliver Burk', 'o.burk@outlook.com', '07000 001955', '123 Test Street, Teston, TS7 7CT');

-- Practices at Exeter or elsewhere:

INSERT INTO practice
(name, telephone, manager, address, branch)
VALUES
('Plymouth Vets', '01752 000000', 1, '123 Test Street, Plymouth, Devon, PL1 1AA', 'Plymouth'),
('Exeter Vets', '01392 000000', 2, '123 Test Street, Exeter, Devon, EX1 1AA', 'Exeter');

-- Nurses and non-nurses:

INSERT INTO employee_types
(type)
VALUES
('Manager'),
('Veterinarian'),
('Nurse');

-- People working at the Exeter practice or elsewhere:

INSERT INTO employee
(name, email, telephone, employee_type, practice)
VALUES
('John Smith', 'm.smith@ukvets.com', '07000 001011', 1, 1),
('Janet Thomas', 'm.thomas@ukvets.com', '07000 001012', 1, 2),
('Dr. Rick', 'd-rick@ukvets.com', '07000 002021', 2, 1),
('Dr. Virgo', 'd-virgo@ukvets.com', '07000 002022', 2, 2),
('Nurse Anee', 'n-anee@ukvets.com', '07000 003031', 3, 1),
('Nurse Andres', 'n-andres@ukvets.com', '07000 003032', 3, 2);

-- Appointments
--  * scheduled and cancelled,
--  * with nurses and with non-nurses,
--  * before July 5th 2021,
--  * the July 5th 2021,
--  * between July 5th 2021 and July 11th 2021,
--  * the July 11th 2021,
--  * after July 11th 2021:

INSERT INTO appointment
(employee, pet, date, timeslot, reason, cancelled)
VALUES
(3, 1, '2021-06-15', 1, NULL, NULL),
(3, 2, '2021-06-15', 1, NULL, NULL),
(3, 1, '2021-07-05', 2, NULL, NULL),
(3, 2, '2021-07-05', 2, NULL, NULL),
(3, 1, '2021-07-09', 3, NULL, NULL),
(3, 2, '2021-07-09', 3, NULL, NULL),
(3, 1, '2021-07-11', 4, NULL, NULL),
(3, 2, '2021-07-11', 4, NULL, NULL),
(3, 1, '2021-08-13', 5, NULL, NULL),
(3, 2, '2021-08-13', 5, NULL, NULL),
(4, 1, '2021-06-15', 6, NULL, NULL),
(4, 2, '2021-06-15', 6, NULL, NULL),
(4, 1, '2021-07-05', 7, NULL, NULL),
(4, 2, '2021-07-05', 7, NULL, NULL),
(4, 1, '2021-07-09', 8, NULL, NULL),
(4, 2, '2021-07-09', 8, NULL, NULL),
(4, 1, '2021-07-11', 9, NULL, NULL),
(4, 2, '2021-07-11', 9, NULL, NULL),
(4, 1, '2021-08-13', 10, NULL, NULL),
(4, 2, '2021-08-13', 10, NULL, NULL),
(5, 1, '2021-06-15', 11, NULL, NULL),
(5, 2, '2021-06-15', 11, NULL, NULL),
(5, 1, '2021-07-05', 12, NULL, NULL),
(5, 2, '2021-07-05', 12, NULL, NULL),
(5, 1, '2021-07-09', 13, NULL, NULL),
(5, 2, '2021-07-09', 13, NULL, NULL),
(5, 1, '2021-07-11', 14, NULL, NULL),
(5, 2, '2021-07-11', 14, NULL, NULL),
(5, 1, '2021-08-13', 15, NULL, NULL),
(5, 2, '2021-08-13', 15, NULL, NULL),
(6, 1, '2021-06-15', 16, NULL, NULL),
(6, 2, '2021-06-15', 16, NULL, NULL),
(6, 1, '2021-07-05', 1, NULL, NULL),
(6, 2, '2021-07-05', 1, NULL, NULL),
(6, 1, '2021-07-09', 2, NULL, NULL),
(6, 2, '2021-07-09', 2, NULL, NULL),
(6, 1, '2021-07-11', 3, NULL, NULL),
(6, 2, '2021-07-11', 3, NULL, NULL),
(6, 1, '2021-08-13', 4, NULL, NULL),
(6, 2, '2021-08-13', 4, NULL, NULL),
(3, 1, '2021-06-15', 5, 'Cancelled for testing pruposes.', '2021-05-22'),
(3, 2, '2021-06-15', 5, 'Cancelled for testing pruposes.', '2021-05-22'),
(3, 1, '2021-07-05', 6, 'Cancelled for testing pruposes.', '2021-05-22'),
(3, 2, '2021-07-05', 6, 'Cancelled for testing pruposes.', '2021-05-22'),
(3, 1, '2021-07-09', 7, 'Cancelled for testing pruposes.', '2021-05-22'),
(3, 2, '2021-07-09', 7, 'Cancelled for testing pruposes.', '2021-05-22'),
(3, 1, '2021-07-11', 8, 'Cancelled for testing pruposes.', '2021-05-22'),
(3, 2, '2021-07-11', 8, 'Cancelled for testing pruposes.', '2021-05-22'),
(3, 1, '2021-08-13', 9, 'Cancelled for testing pruposes.', '2021-05-22'),
(3, 2, '2021-08-13', 9, 'Cancelled for testing pruposes.', '2021-05-22'),
(4, 1, '2021-06-15', 10, 'Cancelled for testing pruposes.', '2021-05-22'),
(4, 2, '2021-06-15', 10, 'Cancelled for testing pruposes.', '2021-05-22'),
(4, 1, '2021-07-05', 11, 'Cancelled for testing pruposes.', '2021-05-22'),
(4, 2, '2021-07-05', 11, 'Cancelled for testing pruposes.', '2021-05-22'),
(4, 1, '2021-07-09', 12, 'Cancelled for testing pruposes.', '2021-05-22'),
(4, 2, '2021-07-09', 12, 'Cancelled for testing pruposes.', '2021-05-22'),
(4, 1, '2021-07-11', 13, 'Cancelled for testing pruposes.', '2021-05-22'),
(4, 2, '2021-07-11', 13, 'Cancelled for testing pruposes.', '2021-05-22'),
(4, 1, '2021-08-13', 14, 'Cancelled for testing pruposes.', '2021-05-22'),
(4, 2, '2021-08-13', 14, 'Cancelled for testing pruposes.', '2021-05-22'),
(5, 1, '2021-06-15', 15, 'Cancelled for testing pruposes.', '2021-05-22'),
(5, 2, '2021-06-15', 15, 'Cancelled for testing pruposes.', '2021-05-22'),
(5, 1, '2021-07-05', 16, 'Cancelled for testing pruposes.', '2021-05-22'),
(5, 2, '2021-07-05', 16, 'Cancelled for testing pruposes.', '2021-05-22'),
(5, 1, '2021-07-09', 1, 'Cancelled for testing pruposes.', '2021-05-22'),
(5, 2, '2021-07-09', 1, 'Cancelled for testing pruposes.', '2021-05-22'),
(5, 1, '2021-07-11', 2, 'Cancelled for testing pruposes.', '2021-05-22'),
(5, 2, '2021-07-11', 2, 'Cancelled for testing pruposes.', '2021-05-22'),
(5, 1, '2021-08-13', 3, 'Cancelled for testing pruposes.', '2021-05-22'),
(5, 2, '2021-08-13', 3, 'Cancelled for testing pruposes.', '2021-05-22'),
(6, 1, '2021-06-15', 4, 'Cancelled for testing pruposes.', '2021-05-22'),
(6, 2, '2021-06-15', 4, 'Cancelled for testing pruposes.', '2021-05-22'),
(6, 1, '2021-07-05', 5, 'Cancelled for testing pruposes.', '2021-05-22'),
(6, 2, '2021-07-05', 5, 'Cancelled for testing pruposes.', '2021-05-22'),
(6, 1, '2021-07-09', 6, 'Cancelled for testing pruposes.', '2021-05-22'),
(6, 2, '2021-07-09', 6, 'Cancelled for testing pruposes.', '2021-05-22'),
(6, 1, '2021-07-11', 7, 'Cancelled for testing pruposes.', '2021-05-22'),
(6, 2, '2021-07-11', 7, 'Cancelled for testing pruposes.', '2021-05-22'),
(6, 1, '2021-08-13', 8, 'Cancelled for testing pruposes.', '2021-05-22'),
(6, 2, '2021-08-13', 8, 'Cancelled for testing pruposes.', '2021-05-22');

INSERT INTO appointment_timeslots
(timeslot_start, timeslot_end)
VALUES
('09:00:00', '09:30:00'),
('09:30:00', '10:00:00'),
('10:00:00', '10:30:00'),
('10:30:00', '11:00:00'),
('11:00:00', '11:30:00'),
('11:30:00', '12:00:00'),
('12:00:00', '12:30:00'),
('12:30:00', '13:00:00'),
('13:00:00', '13:30:00'),
('13:30:00', '14:00:00'),
('14:00:00', '14:30:00'),
('14:30:00', '15:00:00'),
('15:00:00', '15:30:00'),
('15:30:00', '16:00:00'),
('16:00:00', '16:30:00'),
('16:30:00', '17:00:00');
