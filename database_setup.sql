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
    CONSTRAINT employee_fkey FOREIGN KEY(employee) REFERENCES employee(uid),
    CONSTRAINT pet_fkey FOREIGN KEY(pet) REFERENCES pet(uid),
    CONSTRAINT timeslot_fkey FOREIGN KEY(timeslot) REFERENCES appointment_timeslots(uid)
);

-- Test data:
--  * A single employee type is good enough,
--  * 2 practices,
--  * 3 employees: 1 in practice #1 + 2 in practice #2,
--  * 2 pet owners,
--  * 3 pets: 1 for owner #1 + 2 for owner #2,
--  * The appointment timeslots already present.

INSERT INTO employee_types
(type)
VALUES
('Veterinarian');

INSERT INTO practice
(name, telephone, manager, address, branch)
VALUES
('Plymouth Vets', '01 752 000001', 1, '123 Test Street, Plymouth, Devon, PL1 1AA', 'Plymouth'),
('Exeter Vets', '01 392 000002', 2, '234 Test Street, Exeter, Devon, EX1 1AA', 'Exeter');

INSERT INTO employee
(name, email, telephone, employee_type, practice)
VALUES
('Carl Smith', 'john.smith@plymouthvets.co.uk', '07 001 000001', 1, 1),

('Janet Thomas', 'janet.thomas@exetervets.co.uk', '07 002 000001', 1, 2),
('Andre Robins', 'andre.robins@exetervets.co.uk', '07 002 000002', 1, 2);

INSERT INTO owner
(name, email, telephone, address)
VALUES
('Timmy Jerico', 'timmy.jerico@team-cat.com', '07 465 000001', '456 Owner Square, Test City, TS7 1NG'),
('Joseph Cramson', 'joseph.cramson@team-cat.com', '07 465 000002', '567 Owner Square, Test City, TS7 1NG');

INSERT INTO pet
(owner, name, animal, breed, date_of_birth)
VALUES
(1, 'Rex', 'Dog', 'Bonkus', '2019-12-24'),

(2, 'Jigsaw', 'Cat', 'Chonkus', '2019-10-16'),
(2, 'Pouic-Pouic', 'Chicken', NULL, '1963-11-20');

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
('16:30:00', '17:00:00'),

('00:00:00', '00:00:00'); -- A time slot that should always be in the past.
