CREATE TABLE IF NOT EXISTS Bus (
  bus_id INT NOT NULL,
  plate_number VARCHAR(15) NOT NULL,
  model VARCHAR(30) NOT NULL,
  capacity NUMERIC(3) NOT NULL,
  status VARCHAR(15) NOT NULL,
  PRIMARY KEY (bus_id)
);

CREATE TABLE IF NOT EXISTS Insurance (
  insurance_id INT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  bus_id INT NOT NULL,
  PRIMARY KEY (insurance_id),
  FOREIGN KEY (bus_id) REFERENCES Bus(bus_id)
);

CREATE TABLE IF NOT EXISTS BusOperation (
  operation_id INT NOT NULL,
  operation_date DATE NOT NULL,
  operation_cost FLOAT NOT NULL,
  bus_id INT NOT NULL,
  PRIMARY KEY (operation_id),
  FOREIGN KEY (bus_id) REFERENCES Bus(bus_id)
);

CREATE TABLE IF NOT EXISTS Maintenance (
  maintenance_type VARCHAR(30) NOT NULL,
  who_maintained VARCHAR(50) NOT NULL,
  next_due_date DATE NOT NULL,
  operation_id INT NOT NULL,
  PRIMARY KEY (operation_id),
  FOREIGN KEY (operation_id) REFERENCES BusOperation(operation_id)
);

CREATE TABLE IF NOT EXISTS Inspection (
  inspection_type VARCHAR(30) NOT NULL,
  inspection_result VARCHAR(15) NOT NULL,
  inspector_name VARCHAR(50) NOT NULL,
  operation_id INT NOT NULL,
  PRIMARY KEY (operation_id),
  FOREIGN KEY (operation_id) REFERENCES BusOperation(operation_id)
);

CREATE TABLE IF NOT EXISTS FuelLog (
  start_fuel_amount_liters FLOAT NOT NULL,
  station_name VARCHAR(100) NOT NULL,
  fuel_added_liters FLOAT NOT NULL,
  operation_id INT NOT NULL,
  PRIMARY KEY (operation_id),
  FOREIGN KEY (operation_id) REFERENCES BusOperation(operation_id)
);
