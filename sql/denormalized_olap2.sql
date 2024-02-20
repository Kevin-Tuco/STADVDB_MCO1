CREATE TABLE denormalized_table_appointments AS
SELECT a.apptid, c.RegionName, c.Province, c.City
FROM clinics c
JOIN appointments a ON a.clinicid = c.clinicid;

SELECT RegionName, COUNT(apptid) AS AppidCount
FROM denormalized_table_appointments
GROUP BY RegionName;
