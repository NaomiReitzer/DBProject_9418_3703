

# Bus Company Management System

Naomi Reitzer and Sara Koskas

## Table of Contents  
- [Phase 1: Design and Build the Database](#phase-1-design-and-build-the-database)  
  - [Introduction](#introduction)  
  - [ERD (Entity-Relationship Diagram)](#erd-entity-relationship-diagram)  
  - [DSD (Data Structure Diagram)](#dsd-data-structure-diagram)  
  - [SQL Scripts](#sql-scripts)  
  - [Data](#data)
  - [Backup](#backup)

- [Phase 2: Queries and constraints](#phase-2-queries-and-constraints)
  - [SELECT Queries (8)](#-select-queries-8)  
  - [DELETE Queries (3)](#-delete-queries-3)  
  - [UPDATE Queries (3)](#-update-queries-3)  
  - [Constraints Added (`ALTER TABLE`)](#-constraints-added-alter-table)  
  - [Backup](#-backup)  


## Phase 1: Design and Build the Database  

### Introduction

The **Bus Company Management System** is designed to efficiently oversee the operations of a public transportation organization. This system ensures seamless coordination between different divisions, including fleet management, employee assignments, route scheduling, ticketing, finance, and customer support.

#### Purpose of the Database
This database serves as a structured and reliable solution for bus company operations by:
- **Managing the fleet through** detailed tracking of buses, maintenance records, fuel consumption and inspections.
- **Organizing driver and staff assignments,** ensuring proper scheduling and payroll management.
- **Optimizing route planning and scheduling** to improve operational efficiency and passenger service.  
- **Handling ticketing and booking,** allowing passengers to reserve seats and track ticket purchases.
- **Maintaining financial records,** including revenue, expenses, and tax reporting.
- **Providing customer support,** allowing for complaint tracking, lost-and-found management and feedback collection.

#### Potential Use Cases
- **Fleet Managers** can track bus maintenance, fuel logs and inspections to ensure operational efficiency. 
- **Drivers and Staff** can view their schedules, salary details and attendance records.
- **Passengers** can book tickets, view schedules, and submit feedback or complaints.
- **Customer Support Representatives** can manage inquiries, complaints and lost-and-found items.

This structured database enhances operational efficiency, financial tracking and customer satisfaction, making it an essential tool for managing large-scale bus transportation services.

###  ERD (Entity-Relationship Diagram)    
![ERD Diagram](Phase1/ERDAndDSTFiles/ERD.png)  

###  DSD (Data Structure Diagram)   
![DSD Diagram](Phase1/ERDAndDSTFiles/DSD.png)  

###  SQL Scripts  
Provide the following SQL scripts:  
- **Create Tables Script** - The SQL script for creating the database tables is available in the repository:  

📜 **[View `create_tables.sql`](Phase1/Scripts/FleetManagementCreateTable.sql)**  

- **Insert Data Script** - The SQL script for insert data to the database tables is available in the repository:  

📜 **[View `insert_tables.sql`](Phase1/Scripts/FleetManagementInsertTables.sql)**  
 
- **Drop Tables Script** - The SQL script for droping all tables is available in the repository:  

📜 **[View `drop_tables.sql`](Phase1/Scripts/FleetManagementDropTable.sql)**  

- **Select All Data Script**  - The SQL script for selectAll tables is available in the repository:  

📜 **[View `selectAll_tables.sql`](Phase1/Scripts/FleetManagementSelectAll.sql)**  
  
###  Data  
####  First tool: using [mockaro](https://www.mockaroo.com/) to create csv file
#####  Entering a data to Bus table
-  bus id scope 1-400
📜[View `Bus.csv`](Phase1/MockedData/Bus.csv)
![image](Phase1/UploadDataImages/bus1.png)
![image](Phase1/UploadDataImages/bus2.png)
results for  the command `SELECT COUNT(*) FROM Bus;`:
![image](Phase1/UploadDataImages/bus3.png)

####  Second tool: using [generatedata](https://generatedata.com/generator). to create csv file 
#####  Entering a data to Insurance table
- insurance id scope 1-400
📜[View `Insurance.csv`](Phase1/MockedData/Insurance.csv)
![image](Phase1/UploadDataImages/Insurance1.png)
![image](Phase1/UploadDataImages/Insurance2.png)
results for  the command `SELECT COUNT(*) FROM Insurance;`:
![image](Phase1/UploadDataImages/Insurance3.png)

####  Third tool: using python to create csv file
#####  Entering a data to BusOperation, FuelLog, Inspection and Maintenance tables
📜[View `generate_data.py`](Phase1/MockDataScript/generate_data.py)
[Enter CSV files folder](Phase1/MockedData)

![image](Phase1/UploadDataImages/BusOperation1.png)
![image](Phase1/UploadDataImages/BusOperation2.png)
![image](Phase1/UploadDataImages/FuelLog1.png)
![image](Phase1/UploadDataImages/FuelLog2.png)
![image](Phase1/UploadDataImages/Inspection1.png)
![image](Phase1/UploadDataImages/Inspection2.png)
![image](Phase1/UploadDataImages/Maintenance1.png)
![image](Phase1/UploadDataImages/Maintenance2.png)

### Backup 
-   backups files are kept with the date and hour of the backup:  
[Enter Backup folder](Phase1/Backup)


## Phase 2: Queries and constraints

### SELECT Queries (8)

1. עלות כוללת של פעולות לכל אוטובוס בשנת 2025

<pre>
SELECT B.bus_id, EXTRACT(YEAR FROM O.operation_date) AS year, SUM(O.operation_cost) AS total_cost
FROM BusOperation O
JOIN Bus B ON B.bus_id = O.bus_id
WHERE EXTRACT(YEAR FROM O.operation_date) = 2025
GROUP BY B.bus_id, year
ORDER BY total_cost DESC;
</pre>

![image](Phase2/SelectQueriesImages/Select1.png)

2. ביטוחים שפג תוקפם החודש
<pre>
SELECT insurance_id, bus_id, insurance_start_date, end_date
FROM Insurance
WHERE EXTRACT(MONTH FROM end_date) = EXTRACT(MONTH FROM CURRENT_DATE)
  AND EXTRACT(YEAR FROM end_date) = EXTRACT(YEAR FROM CURRENT_DATE);
</pre>

![image](Phase2/SelectQueriesImages/Select2.png)

3. ממוצע עלות פעולות לאוטובוסים לא פעילים
<pre>
SELECT B.bus_id, AVG(O.operation_cost) AS avg_cost
FROM Bus B
JOIN BusOperation O ON B.bus_id = O.bus_id
WHERE B.bus_status = 'Inactive'
GROUP BY B.bus_id;
</pre>

![image](Phase2/SelectQueriesImages/Select3.png)

4. חמש פעולות התדלוק עם כמות הדלק הגבוהה ביותר
<pre>
SELECT B.bus_id, F.station_name, F.fuel_added_liters, O.operation_date
FROM FuelLog F
JOIN BusOperation O ON O.operation_id = F.operation_id
JOIN Bus B ON B.bus_id = O.bus_id
ORDER BY F.fuel_added_liters DESC
LIMIT 5;
</pre>

![image](Phase2/SelectQueriesImages/select4.png)

5. אוטובוסים עם יותר מ-3 ביקורות
<pre>
SELECT bus_id
FROM Bus
WHERE bus_id IN (
  SELECT B.bus_id
  FROM Bus B
  JOIN BusOperation O ON B.bus_id = O.bus_id
  JOIN Inspection I ON O.operation_id = I.operation_id
  GROUP BY B.bus_id
  HAVING COUNT(*) > 3
);
</pre>

![image](Phase2/SelectQueriesImages/select5.png)

6. סך הביקורות לכל אוטובוס לפי שנה ותוצאה
<pre>
SELECT B.bus_id, EXTRACT(YEAR FROM O.operation_date) AS year, I.inspection_result, COUNT(*) AS total_inspections
FROM Inspection I
JOIN BusOperation O ON O.operation_id = I.operation_id
JOIN Bus B ON B.bus_id = O.bus_id
GROUP BY B.bus_id, year, I.inspection_result
ORDER BY year, B.bus_id;
</pre>

![image](Phase2/SelectQueriesImages/select6.png)

7. תחזוקות שבוצעו בין ינואר למאי
<pre>
SELECT B.bus_id, O.operation_date, M.maintenance_type
FROM BusOperation O
JOIN Bus B ON B.bus_id = O.bus_id
JOIN Maintenance M ON M.operation_id = O.operation_id
WHERE EXTRACT(MONTH FROM O.operation_date) BETWEEN 1 AND 5;
</pre>

![image](Phase2/SelectQueriesImages/select7.png)

8. מספר תחזוקות עתידיות לכל סוג טיפול
<pre>
SELECT maintenance_type, COUNT(*) AS upcoming_maintenances
FROM Maintenance
WHERE next_due_date > CURRENT_DATE
GROUP BY maintenance_type;
</pre>

![image](Phase2/SelectQueriesImages/select8.png)
