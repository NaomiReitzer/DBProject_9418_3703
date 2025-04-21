import pandas as pd
import random
from faker import Faker
from datetime import date

fake = Faker()
Faker.seed(0)
random.seed(0)

# Constants
NUM_BUS_OPERATIONS = 1200
BUS_IDS = list(range(1, 401))
OPERATION_IDS = list(range(1, NUM_BUS_OPERATIONS + 1))

# 1. BusOperation
bus_operations = []
for op_id in OPERATION_IDS:
    bus_id = random.choice(BUS_IDS)
    operation_date = fake.date_between(start_date=date(2025, 4, 1), end_date=date(2025, 4, 10)).strftime('%Y-%m-%d')
    operation_cost = round(random.uniform(100.0, 5000.0), 2)
    bus_operations.append({
        'operation_id': op_id,
        'operation_date': operation_date,
        'operation_cost': operation_cost,
        'bus_id': bus_id
    })
bus_op_df = pd.DataFrame(bus_operations)
bus_op_df.to_csv('BusOperation.csv', index=False)

# Shuffle and assign 400 unique IDs to each inheritor
random.shuffle(OPERATION_IDS)
maintenance_ids = OPERATION_IDS[0:400]
inspection_ids = OPERATION_IDS[400:800]
fuellog_ids = OPERATION_IDS[800:1200]

# 2. Maintenance
maintenance = []
for op_id in maintenance_ids:
    maintenance_type = random.choice(['Engine Check', 'Oil Change', 'Brake Replacement'])
    who_maintained = fake.name()
    next_due_date = fake.date_between(start_date='+30d', end_date='+180d').strftime('%Y-%m-%d')
    maintenance.append({
        'maintenance_type': maintenance_type,
        'who_maintained': who_maintained,
        'next_due_date': next_due_date,
        'operation_id': op_id
    })
pd.DataFrame(maintenance).to_csv('Maintenance.csv', index=False)

# 3. Inspection
inspection = []
for op_id in inspection_ids:
    inspection_type = random.choice(['Safety', 'Emissions', 'General'])
    inspection_result = random.choice(['Pass', 'Fail'])
    inspector_name = fake.name()
    inspection.append({
        'inspection_type': inspection_type,
        'inspection_result': inspection_result,
        'inspector_name': inspector_name,
        'operation_id': op_id
    })
pd.DataFrame(inspection).to_csv('Inspection.csv', index=False)

# 4. FuelLog
fuel_log = []
for op_id in fuellog_ids:
    start_fuel = round(random.uniform(10, 150), 1)
    fuel_added = round(random.uniform(20, 100), 1)
    station_name = fake.company()
    fuel_log.append({
        'start_fuel_amount_liters': start_fuel,
        'station_name': station_name,
        'fuel_added_liters': fuel_added,
        'operation_id': op_id
    })
pd.DataFrame(fuel_log).to_csv('FuelLog.csv', index=False)

print("Done! 1200 BusOperations created. Each inheritor table has 400 unique operation_ids.")
