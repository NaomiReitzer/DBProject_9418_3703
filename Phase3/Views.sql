-- מבט 1: פרטי אוטובוסים עם פעילות תפעולית (מנקודת מבט של אגף האוטובוסים)
CREATE VIEW BusOperationalSummary AS
SELECT 
    b.bus_id,
    b.plate_number,
    b.model,
    b.capacity,
    b.bus_status,
    COUNT(bo.operation_id) AS total_operations,
    COALESCE(SUM(bo.operation_cost), 0) AS total_operation_cost,
    MAX(bo.operation_date) AS last_operation_date,
    MIN(bo.operation_date) AS first_operation_date
FROM Bus b
LEFT JOIN BusOperation bo ON b.bus_id = bo.bus_id
GROUP BY b.bus_id, b.plate_number, b.model, b.capacity, b.bus_status;

-- מבט 2: פרטי נהגים עם משמרות (מנקודת מבט של אגף הנהגים)
CREATE VIEW DriverShiftSummary AS
SELECT 
    d.driver_id,
    d.id_number,
    d.first_name,
    d.last_name,
    d.phone,
    d.driver_status,
    COUNT(s.shift_id) AS total_shifts,
    MAX(s.shift_date) AS last_shift_date,
    MIN(s.shift_date) AS first_shift_date,
    COUNT(DISTINCT s.bus_id) AS buses_driven
FROM Driver d
LEFT JOIN Shift s ON d.driver_id = s.driver_id
GROUP BY d.driver_id, d.id_number, d.first_name, d.last_name, d.phone, d.driver_status;

-- שאילתות על מבט 1

-- שאילתה 1.1: איתור האוטובוסים הכי יקרים בתפעול
SELECT 
    plate_number,
    model,
    total_operation_cost,
    total_operations,
    ROUND(CAST(total_operation_cost / NULLIF(total_operations, 0) AS NUMERIC), 2) AS avg_cost_per_operation
FROM BusOperationalSummary
WHERE total_operations > 0
ORDER BY total_operation_cost DESC
LIMIT 5;

-- שאילתה 1.2: אוטובוסים פעילים שלא הופעלו לאחרונה (יותר מ-30 יום)
SELECT 
    plate_number,
    model,
    bus_status,
    last_operation_date,
    CURRENT_DATE - last_operation_date AS days_since_last_operation
FROM BusOperationalSummary
WHERE bus_status = 'Active' 
    AND (last_operation_date IS NULL OR last_operation_date < CURRENT_DATE - INTERVAL '30 days')
ORDER BY last_operation_date ASC;

-- שאילתות על מבט 2

-- שאילתה 2.1: נהגים פעילים עם הכי הרבה משמרות
SELECT 
    first_name,
    last_name,
    phone,
    total_shifts,
    buses_driven,
    last_shift_date
FROM DriverShiftSummary
WHERE driver_status = 'Active'
ORDER BY total_shifts DESC
LIMIT 10;

-- שאילתה 2.2: נהגים שלא עבדו לאחרונה (יותר מ-15 יום) אבל עדיין פעילים
SELECT 
    first_name,
    last_name,
    id_number,
    phone,
    driver_status,
    last_shift_date,
    CURRENT_DATE - last_shift_date AS days_since_last_shift
FROM DriverShiftSummary
WHERE driver_status = 'Active' 
    AND (last_shift_date IS NULL OR last_shift_date < CURRENT_DATE - INTERVAL '15 days')
ORDER BY last_shift_date ASC;