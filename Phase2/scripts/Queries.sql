SELECT B.bus_id, EXTRACT(YEAR FROM O.operation_date) AS year, SUM(O.operation_cost) AS total_cost
FROM BusOperation O
JOIN Bus B ON B.bus_id = O.bus_id
WHERE EXTRACT(YEAR FROM O.operation_date) = 2025
GROUP BY B.bus_id, year
ORDER BY total_cost DESC;

SELECT insurance_id, bus_id, insurance_start_date, end_date
FROM Insurance
WHERE EXTRACT(MONTH FROM end_date) = EXTRACT(MONTH FROM CURRENT_DATE)
  AND EXTRACT(YEAR FROM end_date) = EXTRACT(YEAR FROM CURRENT_DATE);

SELECT B.bus_id, AVG(O.operation_cost) AS avg_cost
FROM Bus B
JOIN BusOperation O ON B.bus_id = O.bus_id
WHERE B.bus_status = 'Inactive'
GROUP BY B.bus_id;

SELECT B.bus_id, F.station_name, F.fuel_added_liters, O.operation_date
FROM FuelLog F
JOIN BusOperation O ON O.operation_id = F.operation_id
JOIN Bus B ON B.bus_id = O.bus_id
ORDER BY F.fuel_added_liters DESC
LIMIT 5;

SELECT bus_id, plate_number
FROM Bus
WHERE bus_id IN (
  SELECT B.bus_id
  FROM Bus B
  JOIN BusOperation O ON B.bus_id = O.bus_id
  JOIN Inspection I ON O.operation_id = I.operation_id
  GROUP BY B.bus_id
  HAVING COUNT(*) > 3
);

SELECT B.bus_id, EXTRACT(YEAR FROM O.operation_date) AS year, I.inspection_result, COUNT(*) AS total_inspections
FROM Inspection I
JOIN BusOperation O ON O.operation_id = I.operation_id
JOIN Bus B ON B.bus_id = O.bus_id
GROUP BY B.bus_id, year, I.inspection_result
ORDER BY year, B.bus_id;

SELECT B.bus_id, O.operation_date, M.maintenance_type
FROM BusOperation O
JOIN Bus B ON B.bus_id = O.bus_id
JOIN Maintenance M ON M.operation_id = O.operation_id
WHERE EXTRACT(MONTH FROM O.operation_date) BETWEEN 1 AND 5;

SELECT maintenance_type, COUNT(*) AS upcoming_maintenances
FROM Maintenance
WHERE next_due_date > CURRENT_DATE
GROUP BY maintenance_type;


DELETE FROM Insurance
WHERE end_date < CURRENT_DATE;

DELETE FROM BusOperation
WHERE operation_cost = 0;

DELETE FROM Insurance
WHERE bus_id NOT IN (
  SELECT DISTINCT bus_id FROM BusOperation
);
DELETE FROM Bus
WHERE bus_id NOT IN (
  SELECT DISTINCT bus_id FROM BusOperation
);



UPDATE Bus
SET bus_status = 'Inactive'
WHERE bus_id IN (
  SELECT bus_id FROM Insurance
  WHERE end_date < CURRENT_DATE
);

UPDATE BusOperation
SET operation_cost = operation_cost * 1.10
WHERE operation_id IN (
  SELECT operation_id FROM FuelLog
  WHERE fuel_added_liters > 50
);

UPDATE FuelLog
SET station_name = 'Yang Hill'
WHERE station_name = 'Yang-Hill';
