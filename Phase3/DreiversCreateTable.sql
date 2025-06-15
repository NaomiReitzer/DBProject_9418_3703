CREATE TABLE IF NOT EXISTS Driver (
  driver_id INT NOT NULL,
  id_number VARCHAR(15) NOT NULL UNIQUE,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  phone VARCHAR(15),
  driver_status VARCHAR(20) CHECK (driver_status IN ('Active', 'Inactive', 'On Leave')),
  PRIMARY KEY (driver_id)
);

CREATE TABLE IF NOT EXISTS Shift (
  shift_id INT NOT NULL,
  shift_date DATE NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME,
  driver_id INT NOT NULL,
  bus_id INT NOT NULL,
  PRIMARY KEY (shift_id),
  FOREIGN KEY (driver_id) REFERENCES Driver(driver_id)
  -- FOREIGN KEY (bus_id) REFERENCES Bus(bus_id) - יתווסף באינטגרציה
);
