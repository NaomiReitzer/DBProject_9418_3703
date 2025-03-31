INSERT INTO Bus (bus_id, plate_number, model, capacity, status) VALUES (1, '123-45-678', 'Volvo B8R', 50, 'Active');
INSERT INTO Bus (bus_id, plate_number, model, capacity, status) VALUES (2, '234-56-789', 'Mercedes Sprinter', 20, 'In Maintenance');
INSERT INTO Bus (bus_id, plate_number, model, capacity, status) VALUES (3, '345-67-890', 'MAN Lion’s Coach', 60, 'Active');

INSERT INTO Insurance (insurance_id, start_date, end_date, bus_id) VALUES (1001, '2024-01-01', '2025-01-01', 1);
INSERT INTO Insurance (insurance_id, start_date, end_date, bus_id) VALUES (1002, '2024-02-01', '2025-02-01', 2);
INSERT INTO Insurance (insurance_id, start_date, end_date, bus_id) VALUES (1003, '2024-03-01', '2025-03-01', 3);

INSERT INTO BusOperation (operation_id, operation_date, operation_cost, bus_id) VALUES (2001, '2024-03-15', 500.00, 1);
INSERT INTO BusOperation (operation_id, operation_date, operation_cost, bus_id) VALUES (2002, '2024-03-20', 300.00, 2);
INSERT INTO BusOperation (operation_id, operation_date, operation_cost, bus_id) VALUES (2003, '2024-03-25', 450.00, 3);

INSERT INTO Maintenance (operation_id, maintenance_type) VALUES (2001, 'Engine Check');
INSERT INTO Maintenance (operation_id, maintenance_type) VALUES (2002, 'Brake Replacement');
INSERT INTO Maintenance (operation_id, maintenance_type) VALUES (2003, 'Tire Change');

INSERT INTO Inspection (operation_id, inspection_name, inspection_result) VALUES (2001, 'Annual Safety Check', 'Pass');
INSERT INTO Inspection (operation_id, inspection_name, inspection_result) VALUES (2002, 'Emission Test', 'Fail');
INSERT INTO Inspection (operation_id, inspection_name, inspection_result) VALUES (2003, 'Brake Test', 'Pass');

INSERT INTO FuelLog (operation_id, fuel_amount_liters) VALUES (2001, 120.5);
INSERT INTO FuelLog (operation_id, fuel_amount_liters) VALUES (2002, 95.3);
INSERT INTO FuelLog (operation_id, fuel_amount_liters) VALUES (2003, 110.0);
