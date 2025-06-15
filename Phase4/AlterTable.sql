ALTER TABLE Shift DROP CONSTRAINT IF EXISTS shift_driver_id_fkey;
ALTER TABLE Shift DROP CONSTRAINT IF EXISTS shift_bus_id_fkey;

ALTER TABLE Shift 
ADD CONSTRAINT shift_driver_id_fkey 
FOREIGN KEY (driver_id) REFERENCES Driver(driver_id);

ALTER TABLE Shift 
ADD CONSTRAINT shift_bus_id_fkey 
FOREIGN KEY (bus_id) REFERENCES Bus(bus_id);

ALTER TABLE Shift 
ADD CONSTRAINT check_shift_times 
CHECK (end_time IS NULL OR end_time > start_time);

ALTER TABLE BusOperation 
ALTER COLUMN operation_cost TYPE NUMERIC(10,2);

ALTER TABLE FuelLog 
ALTER COLUMN start_fuel_amount_liters TYPE NUMERIC(8,2);

ALTER TABLE FuelLog 
ALTER COLUMN fuel_added_liters TYPE NUMERIC(8,2);