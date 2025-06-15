-- ========================================
-- Purpose: Returns REF CURSOR with maintenance summary
-- Parameters: p_days_ahead - number of days to look ahead for maintenance
-- Returns: REFCURSOR with bus maintenance information
-- ========================================
CREATE OR REPLACE FUNCTION get_maintenance_summary(p_days_ahead INT DEFAULT 30) 
RETURNS REFCURSOR
LANGUAGE plpgsql
AS $$
DECLARE
    -- Declare named cursor for maintenance data
    maintenance_cursor REFCURSOR := 'maintenance_cur';
    v_count INT := 0;
BEGIN
    -- Open explicit cursor to select maintenance records within date range
    OPEN maintenance_cursor FOR
        SELECT 
            b.bus_id,
            b.plate_number,
            m.maintenance_type,
            m.next_due_date,
            -- Use CASE to determine maintenance priority based on due date
            CASE 
                WHEN m.next_due_date < CURRENT_DATE THEN 'OVERDUE'
                WHEN m.next_due_date <= CURRENT_DATE + 7 THEN 'URGENT'
                ELSE 'UPCOMING'
            END AS priority
        FROM Bus b
        JOIN BusOperation bo ON b.bus_id = bo.bus_id
        JOIN Maintenance m ON bo.operation_id = m.operation_id
        WHERE m.next_due_date <= CURRENT_DATE + p_days_ahead
        ORDER BY m.next_due_date;
    
    -- Count total maintenance items using implicit cursor (FOR loop)
    FOR v_count IN (
        SELECT COUNT(*)
        FROM Bus b
        JOIN BusOperation bo ON b.bus_id = bo.bus_id
        JOIN Maintenance m ON bo.operation_id = m.operation_id
        WHERE m.next_due_date <= CURRENT_DATE + p_days_ahead
    ) LOOP
        -- Display count information using RAISE NOTICE
        RAISE NOTICE 'Found % maintenance items within % days', v_count, p_days_ahead;
    END LOOP;
    
    -- Return the opened cursor to caller
    RETURN maintenance_cursor;
    
EXCEPTION
    -- Handle any errors that occur during function execution
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in maintenance summary: %', SQLERRM;
END;
$$;

-- ========================================
-- Purpose: Processes various types of bus operations (FUEL, MAINTENANCE, INSPECTION)
-- Parameters: p_bus_id - bus identifier, p_operation_type - type of operation,
--            p_cost - operation cost, p_operation_id - INOUT parameter for operation ID
-- ========================================
CREATE OR REPLACE PROCEDURE process_bus_operation(
    p_bus_id INT,
    p_operation_type VARCHAR(20),
    p_cost NUMERIC,
    INOUT p_operation_id INT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    -- Record to store bus information
    v_bus_record RECORD;
    -- Record to store operation information for loops
    v_operation_record RECORD;
    v_total_cost NUMERIC := 0;
    v_count INT := 0;
BEGIN
    -- Validate bus exists and get bus information using STRICT
    BEGIN
        SELECT bus_id, plate_number, bus_status INTO STRICT v_bus_record
        FROM Bus WHERE bus_id = p_bus_id;
    EXCEPTION
        -- Handle case when no bus is found
        WHEN NO_DATA_FOUND THEN
            RAISE EXCEPTION 'Bus % not found', p_bus_id;
    END;
    
    -- Validate bus status using IF statement
    IF v_bus_record.bus_status != 'Active' THEN
        RAISE EXCEPTION 'Bus % is not active', p_bus_id;
    END IF;
    
    -- Generate new operation ID if not provided (INOUT parameter handling)
    IF p_operation_id IS NULL THEN
        SELECT COALESCE(MAX(operation_id), 0) + 1 INTO p_operation_id FROM BusOperation;
    END IF;
    
    -- Insert new bus operation record (DML operation)
    INSERT INTO BusOperation (operation_id, operation_date, operation_cost, bus_id)
    VALUES (p_operation_id, CURRENT_DATE, p_cost, p_bus_id);
    
    -- Process different operation types using CASE statement
    CASE p_operation_type
        WHEN 'FUEL' THEN
            -- Insert fuel log record
            INSERT INTO FuelLog (start_fuel_amount_liters, station_name, fuel_added_liters, operation_id)
            VALUES (10.0, 'Default Station', 50.0, p_operation_id);
            RAISE NOTICE 'Fuel operation completed for bus %', v_bus_record.plate_number;
            
        WHEN 'MAINTENANCE' THEN
            -- Insert maintenance record with future due date
            INSERT INTO Maintenance (maintenance_type, who_maintained, next_due_date, operation_id)
            VALUES ('General Service', 'Technician', CURRENT_DATE + 90, p_operation_id);
            RAISE NOTICE 'Maintenance scheduled for bus %', v_bus_record.plate_number;
            
        WHEN 'INSPECTION' THEN
            -- Insert inspection record
            INSERT INTO Inspection (inspection_type, inspection_result, inspector_name, operation_id)
            VALUES ('Safety Check', 'Pass', 'Inspector', p_operation_id);
            RAISE NOTICE 'Inspection completed for bus %', v_bus_record.plate_number;
            
        ELSE
            -- Handle invalid operation types
            RAISE EXCEPTION 'Invalid operation type: %', p_operation_type;
    END CASE;
    
    -- Calculate monthly cost summary using FOR loop with explicit cursor
    FOR v_operation_record IN (
        SELECT operation_cost 
        FROM BusOperation 
        WHERE bus_id = p_bus_id 
        AND EXTRACT(MONTH FROM operation_date) = EXTRACT(MONTH FROM CURRENT_DATE)
    ) LOOP
        v_count := v_count + 1;
        v_total_cost := v_total_cost + v_operation_record.operation_cost;
    END LOOP;
    
    -- Display monthly summary information
    RAISE NOTICE 'Monthly summary for bus %: % operations, total cost: $%', 
        p_bus_id, v_count, v_total_cost;
    
EXCEPTION
    -- Handle any errors during procedure execution
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error processing operation: %', SQLERRM;
END;
$$;

-- ========================================
-- Purpose: Validates bus operations before insertion
-- Validates: negative costs, calculates monthly totals, alerts for high costs
-- ========================================
CREATE OR REPLACE FUNCTION validate_bus_operation()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    -- Variable to store bus plate number
    v_bus_plate VARCHAR(15);
    -- Variable to store monthly cost total
    v_monthly_cost NUMERIC;
BEGIN
    -- Check if this is an INSERT operation
    IF TG_OP = 'INSERT' THEN
        -- Get bus plate number for the operation
        SELECT plate_number INTO v_bus_plate FROM Bus WHERE bus_id = NEW.bus_id;
        
        -- Validate operation cost is not negative using IF statement
        IF NEW.operation_cost < 0 THEN
            RAISE EXCEPTION 'Cost cannot be negative: %', NEW.operation_cost;
        END IF;
        
        -- Calculate monthly total cost for this bus
        SELECT COALESCE(SUM(operation_cost), 0) INTO v_monthly_cost
        FROM BusOperation 
        WHERE bus_id = NEW.bus_id 
        AND EXTRACT(MONTH FROM operation_date) = EXTRACT(MONTH FROM NEW.operation_date);
        
        -- Alert for high cost operations using IF statement
        IF NEW.operation_cost > 500 THEN
            RAISE WARNING 'High cost operation: $% for bus %', NEW.operation_cost, v_bus_plate;
        END IF;
        
        -- Log operation details
        RAISE NOTICE 'Operation added: Bus % cost $%, monthly total: $%', 
            v_bus_plate, NEW.operation_cost, v_monthly_cost;
    END IF;
    
    -- Return the new or old record based on operation type
    RETURN COALESCE(NEW, OLD);
    
EXCEPTION
    -- Handle validation errors
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Validation error: %', SQLERRM;
END;
$$;

-- Create trigger that fires before INSERT operations on BusOperation table
DROP TRIGGER IF EXISTS operation_validator ON BusOperation;
CREATE TRIGGER operation_validator
    BEFORE INSERT ON BusOperation
    FOR EACH ROW EXECUTE FUNCTION validate_bus_operation();

-- ========================================
-- Purpose: Demonstrates complete bus operations workflow
-- Steps: 1) Check maintenance schedule, 2) Process operations, 3) Display summary
-- ========================================
DO $$
DECLARE
    -- REF CURSOR variable to hold maintenance data
    maintenance_ref REFCURSOR;
    -- Record variable to store maintenance information
    v_maintenance_record RECORD;
    -- Variable to store operation ID
    v_operation_id INT;
    v_counter INT := 0;
    -- Two-dimensional array containing operation data
    v_operations TEXT[][] := ARRAY[
        ['1', 'FUEL', '150.00'],
        ['2', 'MAINTENANCE', '300.00'],
        ['1', 'INSPECTION', '75.00']
    ];
    -- Variable to hold individual operation array
    v_op TEXT[];
BEGIN
    -- Display system startup message
    RAISE NOTICE '=== BUS OPERATIONS SYSTEM STARTED ===';
    
    -- Step 1: Check maintenance schedule using function that returns REF CURSOR
    RAISE NOTICE 'Step 1: Checking maintenance schedule...';
    SELECT get_maintenance_summary(30) INTO maintenance_ref;
    
    -- Process maintenance cursor using explicit cursor operations
    LOOP
        FETCH maintenance_ref INTO v_maintenance_record;
        EXIT WHEN NOT FOUND;
        
        -- Display maintenance information for each bus
        RAISE NOTICE 'Bus %: % - % (%)', 
            v_maintenance_record.bus_id,
            v_maintenance_record.plate_number,
            v_maintenance_record.maintenance_type,
            v_maintenance_record.priority;
    END LOOP;
    
    -- Close cursor safely with exception handling
    BEGIN
        CLOSE maintenance_ref;
    EXCEPTION
        WHEN OTHERS THEN
            NULL; -- Ignore if cursor is already closed
    END;
    
    -- Step 2: Process operations using FOREACH loop with array
    RAISE NOTICE 'Step 2: Processing operations...';
    FOREACH v_op SLICE 1 IN ARRAY v_operations LOOP
        -- Generate unique operation ID using counter
        v_counter := v_counter + 1;
        v_operation_id := 2000 + v_counter;
        
        -- Call procedure to process each operation with exception handling
        BEGIN
            CALL process_bus_operation(
                p_bus_id => v_op[1]::INT,
                p_operation_type => v_op[2],
                p_cost => v_op[3]::NUMERIC,
                p_operation_id => v_operation_id
            );
        EXCEPTION
            WHEN OTHERS THEN
                RAISE NOTICE 'Error processing operation: %', SQLERRM;
        END;
    END LOOP;
    
    -- Step 3: Display system summary using implicit cursor (FOR loop)
    RAISE NOTICE 'Step 3: System summary';
    FOR v_maintenance_record IN (
        SELECT 
            b.bus_id, 
            b.plate_number,
            COUNT(bo.operation_id) as ops,
            SUM(bo.operation_cost) as total
        FROM Bus b
        LEFT JOIN BusOperation bo ON b.bus_id = bo.bus_id
        WHERE bo.operation_date >= CURRENT_DATE - 30
        GROUP BY b.bus_id, b.plate_number
        HAVING COUNT(bo.operation_id) > 0
        LIMIT 3
    ) LOOP
        -- Display summary for each bus with recent operations
        RAISE NOTICE 'Bus %: % operations, $% total',
            v_maintenance_record.plate_number,
            v_maintenance_record.ops,
            v_maintenance_record.total;
    END LOOP;
    
    -- Display system completion message
    RAISE NOTICE '=== BUS OPERATIONS SYSTEM COMPLETED ===';
    
EXCEPTION
    -- Handle any system-level errors
    WHEN OTHERS THEN
        -- Try to close cursor safely
        BEGIN
            IF maintenance_ref IS NOT NULL THEN
                CLOSE maintenance_ref;
            END IF;
        EXCEPTION
            WHEN OTHERS THEN
                NULL; -- Ignore cursor close errors
        END;
        RAISE EXCEPTION 'System error: %', SQLERRM;
END;
$$;