-- אילוץ 1: ברירת מחדל לסטטוס אוטובוס
ALTER TABLE Bus
ALTER COLUMN bus_status SET DEFAULT 'Active';

-- אילוץ 2: לבדוק שעלות פעולה גדולה מאפס
ALTER TABLE BusOperation
ADD CONSTRAINT check_operation_cost_positive CHECK (operation_cost > 0);

-- אילוץ 3: לא לאפשר שדה תחנת דלק ריק
ALTER TABLE FuelLog
ALTER COLUMN station_name SET NOT NULL;