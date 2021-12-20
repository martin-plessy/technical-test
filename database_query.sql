-- Write a query that returns
--  * the appointment details,                           ->  uid, date, time slot start & end,
--  * owner's contact details,                           ->  uid, name, email, telephone, address
--  * and pet's details                                  ->  uid, name, animal, [breed], date_of_birth
-- for all scheduled                                     ->  where not [cancelled]
-- Nurse appointments                                    ->  employee type
-- at the Exeter practice                                ->  name | branch | address like
-- between July 5th 2021 and July 11th 2021 (inclusive)  ->  between
-- in ascending chronological order.                     ->  order by

SELECT
    -- Appointment details:
    appointment.uid AS appointment_id,
    appointment.date AS appointment_date,
    appointment_timeslots.timeslot_start AS appointment_start,
    appointment_timeslots.timeslot_end AS appointment_end,

    -- Returning some unrequested details about the practice as well,
    -- if only: phone and address, in case the owner gets lost while on their journey.
    -- Dependeing on the use case, they may be relevant as part of the "appointment details".
    practice.name AS practice_name,
    practice.telephone AS practice_phone,
    practice.address AS practice_address,

    -- Owner's contact details:
    -- ID and address might be overkill for "just contact details",
    -- although it might prove useful for creating hyperlinks.
    owner.uid AS owner_id,
    owner.name AS owner_name,
    owner.email AS owner_email,
    owner.telephone AS owner_phone,
    owner.address AS owner_address,

    -- Pet's details:
    pet.uid AS pet_id,
    pet.name AS pet_name,
    CASE WHEN pet.breed IS NOT NULL
        THEN pet.animal || ' (' || pet.breed || ')'
        ELSE pet.animal
    END AS pet_species,
    pet.date_of_birth AS pet_birthdate

FROM appointment
    INNER JOIN appointment_timeslots ON appointment_timeslots.uid = appointment.timeslot

    INNER JOIN employee ON employee.uid = appointment.employee
        INNER JOIN employee_types ON employee_types.uid = employee.employee_type
        INNER JOIN practice ON practice.uid = employee.practice

    INNER JOIN pet ON pet.uid = appointment.pet
        INNER JOIN owner ON owner.uid = pet.owner

WHERE appointment.cancelled IS NULL

-- Case sensitivity differs from one RDBMS to another; converting to uppercase feels safer.
  AND UPPER(employee_types.type) = 'NURSE'

-- When is a practice considered "the Exeter practice"?
-- What if there are multiple practices there?
-- Again, looking for "EXETER" averywhere might be overkill,
-- but it fits the abstract use case of the question.
  AND (
      INSTR(UPPER(practice.name), 'EXETER') > 0
   OR INSTR(UPPER(practice.address), 'EXETER') > 0
   OR INSTR(UPPER(practice.branch), 'EXETER') > 0)

  AND appointment.date BETWEEN '2021-07-05' AND '2021-07-11'

ORDER BY
    appointment.date,
    appointment_timeslots.timeslot_start;
