select * from appointments;
select * from clinics;
select * from doctors;
select * from px;
select * from px_dup;

select distinct mainspecialty from doctors;

select distinct City from clinics;

select distinct app_type from appointments;

select distict hospitalname;
-- select distinct app_type from appointments;

--  Popularity by space (default by area) (area, province, city)
--  	Amount of complete consultations
--  	Amount of canceled consultations
--  	Amount of NoShow consultations
SELECT status, COUNT(*) as status_count
FROM appointments
GROUP BY status;

SELECT c.RegionName,
       COUNT(CASE WHEN a.status = 'Complete' THEN 1 END) AS Complete_Count,
       COUNT(CASE WHEN a.status = 'Queued' THEN 1 END) AS Queued_Count,
       COUNT(CASE WHEN a.status = 'NoShow' THEN 1 END) AS NoShow_Count,
       COUNT(CASE WHEN a.status = 'Serving' THEN 1 END) AS Serving_Count,
       COUNT(CASE WHEN a.status = 'Cancel' THEN 1 END) AS Cancel_Count
FROM appointments a
JOIN clinics c ON a.clinicid = c.clinicid
GROUP BY c.RegionName;

SELECT c.RegionName,
       COUNT(CASE WHEN a.status = 'Complete' THEN 1 END) AS Complete_Count,
       COUNT(CASE WHEN a.status = 'Queued' THEN 1 END) AS Queued_Count,
       COUNT(CASE WHEN a.status = 'NoShow' THEN 1 END) AS NoShow_Count,
       COUNT(CASE WHEN a.status = 'Serving' THEN 1 END) AS Serving_Count,
       COUNT(CASE WHEN a.status = 'Cancel' THEN 1 END) AS Cancel_Count
FROM appointments a
JOIN clinics c ON a.clinicid = c.clinicid
WHERE c.RegionName = 'Cagayan Valley (II)'
GROUP BY c.RegionName;


CREATE INDEX idx_clinics_clinicid ON clinics (clinicid); -- Donee!
CREATE INDEX idx_clinics_apptid ON appointments (clinicid,apptid); -- Donee!
CREATE INDEX idx_StartTime ON appointments (StartTime);

DELETE FROM appointments 
WHERE pxid NOT IN (SELECT pxid FROM px);

SELECT
                    CASE MONTH(TimeQueued)
                        WHEN 1 THEN 'January'
                        WHEN 2 THEN 'February'
                        WHEN 3 THEN 'March'
                        WHEN 4 THEN 'April'
                        WHEN 5 THEN 'May'
                        WHEN 6 THEN 'June'
                        WHEN 7 THEN 'July'
                        WHEN 8 THEN 'August'
                        WHEN 9 THEN 'September'
                        WHEN 10 THEN 'October'
                        WHEN 11 THEN 'November'
                        WHEN 12 THEN 'December'
                    END AS Month,
                    status,
                    COUNT(*) AS StatusCount
                FROM
                    appointments
                WHERE
                    YEAR(TimeQueued) = 2020
                GROUP BY
                    Month,
                    status;

SELECT
                    CASE MONTH(TimeQueued)
                        WHEN 1 THEN 'January'
                        WHEN 2 THEN 'February'
                        WHEN 3 THEN 'March'
                        WHEN 4 THEN 'April'
                        WHEN 5 THEN 'May'
                        WHEN 6 THEN 'June'
                        WHEN 7 THEN 'July'
                        WHEN 8 THEN 'August'
                        WHEN 9 THEN 'September'
                        WHEN 10 THEN 'October'
                        WHEN 11 THEN 'November'
                        WHEN 12 THEN 'December'
                    END AS Month,
                    is_Virtual,
                    COUNT(*) AS VirtualCount
                FROM
                    appointments
                WHERE
                    YEAR(TimeQueued) = 2020
                GROUP BY
                    Month,
                    is_Virtual;

SELECT
                    CASE MONTH(TimeQueued)
                        WHEN 1 THEN 'January'
                        WHEN 2 THEN 'February'
                        WHEN 3 THEN 'March'
                        WHEN 4 THEN 'April'
                        WHEN 5 THEN 'May'
                        WHEN 6 THEN 'June'
                        WHEN 7 THEN 'July'
                        WHEN 8 THEN 'August'
                        WHEN 9 THEN 'September'
                        WHEN 10 THEN 'October'
                        WHEN 11 THEN 'November'
                        WHEN 12 THEN 'December'
                    END AS Month,
                    app_type,
                    COUNT(*) AS AppTypeCount
                FROM
                    appointments
                WHERE
                    YEAR(TimeQueued) = 2020
                GROUP BY
                    Month,
                    app_type;