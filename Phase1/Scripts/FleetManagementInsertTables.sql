-- ============================
-- Insert Data into Bus Table
-- ============================
INSERT INTO Bus (bus_id, plate_number, model, capacity, status) VALUES
(1, '123-45-678', 'Volvo 9700', 50, 'active'),
(2, '234-56-789', 'Mercedes Tourismo', 55, 'under maintenance'),
(3, '345-67-890', 'Scania Irizar', 49, 'active'),
(4, '456-78-901', 'MAN Lion’s Coach', 53, 'active'),
(5, '567-89-012', 'Setra S 417', 60, 'inactive');

-- ================================
-- Insert Data into Insurance Table
-- ================================
INSERT INTO Insurance (insurance_id, start_date, end_date, bus_id) VALUES
(101, '2025-01-01', '2026-01-01', 1),
(102, '2024-06-15', '2025-06-14', 2),
(103, '2025-03-01', '2026-02-28', 3),
(104, '2025-04-01', '2026-03-31', 4),
(105, '2023-12-01', '2024-11-30', 5);

-- ====================================
-- Insert Data into BusOperation Table
-- ====================================
INSERT INTO BusOperation (operation_id, operation_date, operation_cost, bus_id) VALUES
(1001, '2025-04-01', 200.00, 1),
(1002, '2025-04-02', 150.00, 2),
(1003, '2025-04-03', 180.00, 1),
(1004, '2025-04-05', 220.00, 3),
(1005, '2025-04-07', 300.00, 4),
(1006, '2025-04-08', 175.50, 5);

-- ====================================
-- Insert Data into Maintenance Table
-- ====================================
INSERT INTO Maintenance (maintenance_type, who_maintained, next_due_date, operation_id) VALUES
('Oil Change', 'AutoFix Ltd.', '2025-07-01', 1001),
('Brake Check', 'QuickService', '2025-08-15', 1002),
('Tire Rotation', 'WheelPro', '2025-09-01', 1005),
('Engine Check', 'Elite Mechanics', '2025-12-01', 1006);

-- ===================================
-- Insert Data into Inspection Table
-- ===================================
INSERT INTO Inspection (inspection_type, inspection_result, inspector_name, operation_id) VALUES
('Safety', 'pass', 'Dana Cohen', 1003),
('Emission', 'fail', 'Avi Levi', 1004),
('Safety', 'pass', 'Ron Ben-David', 1005),
('Emission', 'pass', 'Lea Bar', 1006);

-- ================================
-- Insert Data into FuelLog Table
-- ================================
INSERT INTO FuelLog (start_fuel_amount_liters, station_name, fuel_added_liters, operation_id) VALUES
(100.0, 'Paz Station', 250.0, 1001),
(80.5, 'Sonol Central', 220.0, 1004),
(95.0, 'Delek North', 230.0, 1005),
(60.0, 'Ten Fuel', 260.0, 1006);