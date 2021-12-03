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
    date DATE NOT NULL,
    timeslot INTEGER NOT NULL,
    reason VARCHAR,
    cancelled TIMESTAMP,
    CONSTRAINT employee_fkey FOREIGN KEY(employee) REFERENCES employee(uid),
    CONSTRAINT timeslot_fkey FOREIGN KEY(timeslot) REFERENCES appointment_timeslots(uid)
);

INSERT INTO employee_types
(type)
VALUES
('Veterinarian'),
('Nurse');

INSERT INTO practice
(name, telephone, manager, address, branch)
VALUES
('Plymouth Vets', '01752 000000', 2, '123 Test Street, Plymouth, Devon, PL1 1AA', 'Plymouth'),
('Exeter Vets', '01392 000000', 1, '123 Test Street, Exeter, Devon, EX1 1AA', 'Exeter');

INSERT INTO employee
(name, email, telephone, employee_type, practice)
VALUES
('John Smith', 'john.smith@plymouthvets.co.uk', '07000 000000', 1, 1),
('Janet Thomas', 'janet.thomas@exetervets.co.uk', '07000 000000', 2, 1);

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