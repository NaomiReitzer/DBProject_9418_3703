-- ========================================
-- Function: get_driver_schedules
-- Purpose: Returns REF CURSOR with driver schedule information
-- Parameters: p_week_offset - weeks from current week (0 = current week)
-- Returns: REFCURSOR with weekly schedule data
-- ========================================
CREATE OR REPLACE FUNCTION get_driver_schedules(p_week_offset INT DEFAULT 0) 
RETURNS REFCURSOR
LANGUAGE plpgsql
AS $$
DECLARE
    schedule_cursor REFCURSOR := 'schedule_cur';
    v_week_start DATE;
    v_total_schedules INT := 0;
BEGIN
    -- Calculate week start date
    v_week_start := CURRENT_DATE + (p_week_offset * 7) - EXTRACT(DOW FROM CURRENT_DATE)::INT;
    
    -- Open explicit cursor for schedule data
    OPEN schedule_cursor FOR
        SELECT 
            d.driver_id,
            d.first_name || ' ' || d.last_name AS driver_name,
            COUNT(s.shift_id) AS shifts_count,
            SUM(EXTRACT(EPOCH FROM (s.end_time - s.start_time)) / 3600) AS total_hours,
            STRING_AGG(DISTINCT b.plate_number, ', ') AS buses_assigned,
            CASE 
                WHEN COUNT(s.shift_id) = 0 THEN 'NO_SHIFTS'
                WHEN COUNT(s.shift_id) <= 3 THEN 'LIGHT_WEEK'
                WHEN COUNT(s.shift_id) <= 5 THEN 'NORMAL_WEEK'
                ELSE 'HEAVY_WEEK'
            END AS workload_status
        FROM Driver d
        LEFT JOIN Shift s ON d.driver_id = s.driver_id 
            AND s.shift_date BETWEEN v_week_start AND v_week_start + 6
        LEFT JOIN Bus b ON s.bus_id = b.bus_id
        WHERE d.driver_status = 'Active'
        GROUP BY d.driver_id, d.first_name, d.last_name
        ORDER BY total_hours DESC NULLS LAST;
    
    -- Count total schedules using implicit cursor
    FOR v_total_schedules IN (
        SELECT COUNT(DISTINCT d.driver_id)
        FROM Driver d
        WHERE d.driver_status = 'Active'
    ) LOOP
        RAISE NOTICE 'Active drivers with schedules: %', v_total_schedules;
    END LOOP;
    
    RETURN schedule_cursor;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error retrieving schedules: %', SQLERRM;
END;
$$;

-- ========================================
-- Procedure: assign_weekly_shifts
-- Purpose: Assigns shifts to drivers for upcoming week
-- Parameters: INOUT p_assignments_made - number of assignments created,
--            p_target_week_offset - which week to assign (default next week)
-- ========================================
CREATE OR REPLACE PROCEDURE assign_weekly_shifts(
    INOUT p_assignments_made INT DEFAULT 0,
    p_target_week_offset INT DEFAULT 1
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_driver_record RECORD;
    v_shift_id INT;
    v_week_start DATE;
    v_current_day DATE;
    v_shift_times TIME[][] := ARRAY[
        ['06:00:00', '14:00:00'],
        ['14:00:00', '22:00:00'],
        ['22:00:00', '06:00:00']
    ];
    v_time_slot TIME[];
    v_assigned_drivers TEXT[] := ARRAY[]::TEXT[];
    
    -- Cursor for available drivers
    driver_cursor CURSOR FOR
        SELECT driver_id, first_name, last_name, driver_status
        FROM Driver
        WHERE driver_status = 'Active'
        ORDER BY driver_id;
BEGIN
    -- Calculate target week start
    v_week_start := CURRENT_DATE + (p_target_week_offset * 7) - EXTRACT(DOW FROM CURRENT_DATE)::INT;
    
    RAISE NOTICE 'Assigning shifts for week starting: %', v_week_start;
    
    -- Process each active driver
    FOR v_driver_record IN driver_cursor LOOP
        BEGIN
            -- Assign shifts for weekdays (Monday to Friday)
            FOR day_offset IN 0..4 LOOP
                v_current_day := v_week_start + day_offset;
                
                -- Skip if driver already has shift on this day
                IF NOT EXISTS (
                    SELECT 1 FROM Shift 
                    WHERE driver_id = v_driver_record.driver_id 
                    AND shift_date = v_current_day
                ) THEN
                    
                    -- Select time slot using FOREACH loop
                    FOREACH v_time_slot SLICE 1 IN ARRAY v_shift_times LOOP
                        -- Check if this time slot is available
                        IF NOT EXISTS (
                            SELECT 1 FROM Shift s
                            JOIN Bus b ON s.bus_id = b.bus_id
                            WHERE s.shift_date = v_current_day
                            AND s.start_time = v_time_slot[1]
                            AND b.bus_status = 'Active'
                            AND s.driver_id != v_driver_record.driver_id
                        ) THEN
                            
                            -- Generate new shift ID
                            SELECT COALESCE(MAX(shift_id), 0) + 1 INTO v_shift_id FROM Shift;
                            
                            -- Insert new shift (DML operation)
                            INSERT INTO Shift (
                                shift_id, shift_date, start_time, end_time, 
                                driver_id, bus_id
                            ) VALUES (
                                v_shift_id, v_current_day, v_time_slot[1], v_time_slot[2],
                                v_driver_record.driver_id, 1  -- Default bus assignment
                            );
                            
                            p_assignments_made := p_assignments_made + 1;
                            EXIT; -- Move to next day
                        END IF;
                    END LOOP;
                END IF;
            END LOOP;
            
            -- Add driver to assigned list
            v_assigned_drivers := array_append(v_assigned_drivers,
                v_driver_record.first_name || ' ' || v_driver_record.last_name);
            
        EXCEPTION
            WHEN OTHERS THEN
                RAISE NOTICE 'Error assigning shifts to driver %: %',
                    v_driver_record.driver_id, SQLERRM;
                CONTINUE;
        END;
        
        -- Limit for demonstration
        EXIT WHEN p_assignments_made >= 15;
    END LOOP;
    
    -- Display summary
    RAISE NOTICE 'Shift assignment completed. Total assignments: %', p_assignments_made;
    IF array_length(v_assigned_drivers, 1) > 0 THEN
        RAISE NOTICE 'Drivers assigned: %', array_to_string(v_assigned_drivers, ', ');
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in shift assignment procedure: %', SQLERRM;
END;
$$;

-- ========================================
-- Trigger: schedule_conflict_checker
-- Purpose: Prevents scheduling conflicts and validates shift assignments
-- ========================================
CREATE OR REPLACE FUNCTION check_schedule_conflicts()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_driver_name TEXT;
    v_conflict_count INT;
    v_shift_duration INTERVAL;
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        -- Get driver name
        SELECT first_name || ' ' || last_name INTO v_driver_name
        FROM Driver WHERE driver_id = NEW.driver_id;
        
        -- Validate shift times using IF statement
        IF NEW.end_time IS NOT NULL AND NEW.end_time <= NEW.start_time THEN
            RAISE EXCEPTION 'Invalid shift times for driver %: End time must be after start time',
                v_driver_name;
        END IF;
        
        -- Check for scheduling conflicts
        SELECT COUNT(*) INTO v_conflict_count
        FROM Shift
        WHERE driver_id = NEW.driver_id
        AND shift_date = NEW.shift_date
        AND shift_id != COALESCE(NEW.shift_id, -1)
        AND (
            (NEW.start_time >= start_time AND NEW.start_time < COALESCE(end_time, '23:59:59'))
            OR (COALESCE(NEW.end_time, '23:59:59') > start_time)
        );
        
        -- Reject conflicting assignments
        IF v_conflict_count > 0 THEN
            RAISE EXCEPTION 'Schedule conflict: Driver % already has % overlapping shift(s) on %',
                v_driver_name, v_conflict_count, NEW.shift_date;
        END IF;
        
        -- Calculate and validate shift duration
        IF NEW.end_time IS NOT NULL THEN
            v_shift_duration := NEW.end_time - NEW.start_time;
            IF EXTRACT(EPOCH FROM v_shift_duration) / 3600 > 10 THEN
                RAISE EXCEPTION 'Shift too long for driver %: % hours (max 10 hours)',
                    v_driver_name, ROUND(EXTRACT(EPOCH FROM v_shift_duration) / 3600, 1);
            END IF;
        END IF;
        
        -- Log successful assignment
        RAISE NOTICE 'Shift assigned: % on % from % to %',
            v_driver_name, NEW.shift_date, NEW.start_time, 
            COALESCE(NEW.end_time::TEXT, 'TBD');
        
        RETURN NEW;
    END IF;
    
    RETURN NULL;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Schedule validation error: %', SQLERRM;
END;
$$;

-- Create trigger
DROP TRIGGER IF EXISTS schedule_conflict_checker ON Shift;
CREATE TRIGGER schedule_conflict_checker
    BEFORE INSERT OR UPDATE ON Shift
    FOR EACH ROW EXECUTE FUNCTION check_schedule_conflicts();

-- ========================================
-- Main Program: Driver Schedule Management System
-- Purpose: Demonstrates schedule management workflow
-- Steps: 1) View current schedules, 2) Assign new shifts, 3) Summary report
-- ========================================
DO $$
DECLARE
    -- REF CURSOR for schedule data
    schedule_ref REFCURSOR;
    v_schedule_record RECORD;
    
    -- Variables for shift assignment
    v_assignments_made INT := 0;
    v_total_drivers INT;
    v_heavy_workload_count INT := 0;
    v_no_shifts_count INT := 0;
    
    -- Counter for display limit
    v_display_count INT := 0;
BEGIN
    RAISE NOTICE '=======================================';
    RAISE NOTICE 'DRIVER SCHEDULE MANAGEMENT SYSTEM';
    RAISE NOTICE 'Started: %', CURRENT_TIMESTAMP;
    RAISE NOTICE '=======================================';
    
    -- Step 1: Review current week schedules using REF CURSOR
    RAISE NOTICE '';
    RAISE NOTICE 'STEP 1: Current Week Schedule Review';
    RAISE NOTICE '-----------------------------------';
    
    -- Get schedule data using function that returns REF CURSOR
    SELECT get_driver_schedules(0) INTO schedule_ref;
    
    -- Process schedule data using explicit cursor operations
    LOOP
        FETCH schedule_ref INTO v_schedule_record;
        EXIT WHEN NOT FOUND;
        
        v_display_count := v_display_count + 1;
        
        -- Count workload categories using CASE
        CASE v_schedule_record.workload_status
            WHEN 'HEAVY_WEEK' THEN v_heavy_workload_count := v_heavy_workload_count + 1;
            WHEN 'NO_SHIFTS' THEN v_no_shifts_count := v_no_shifts_count + 1;
            ELSE NULL;
        END CASE;
        
        -- Display schedule details
        RAISE NOTICE 'Driver: % | Shifts: % | Hours: % | Status: %',
            v_schedule_record.driver_name,
            v_schedule_record.shifts_count,
            COALESCE(ROUND(v_schedule_record.total_hours, 1), 0),
            v_schedule_record.workload_status;
        
        -- Limit output
        EXIT WHEN v_display_count >= 8;
    END LOOP;
    
    -- Close cursor safely
    BEGIN
        CLOSE schedule_ref;
    EXCEPTION
        WHEN OTHERS THEN NULL;
    END;
    
    -- Step 2: Assign shifts for next week using procedure
    RAISE NOTICE '';
    RAISE NOTICE 'STEP 2: Next Week Shift Assignment';
    RAISE NOTICE '---------------------------------';
    
    -- Call procedure with INOUT parameter
    CALL assign_weekly_shifts(
        p_assignments_made => v_assignments_made,
        p_target_week_offset => 1
    );
    
    -- Step 3: Generate summary report
    RAISE NOTICE '';
    RAISE NOTICE 'STEP 3: Schedule Management Summary';
    RAISE NOTICE '----------------------------------';
    
    -- Get total driver count
    SELECT COUNT(*) INTO v_total_drivers FROM Driver WHERE driver_status = 'Active';
    
    -- Display summary statistics
    RAISE NOTICE 'Total Active Drivers: %', v_total_drivers;
    RAISE NOTICE 'Heavy Workload Drivers: %', v_heavy_workload_count;
    RAISE NOTICE 'Drivers with No Shifts: %', v_no_shifts_count;
    RAISE NOTICE 'New Assignments Made: %', v_assignments_made;
    
    -- Provide recommendations using IF statements
    IF v_no_shifts_count > 0 THEN
        RAISE NOTICE 'RECOMMENDATION: % drivers need shift assignments', v_no_shifts_count;
    END IF;
    
    IF v_heavy_workload_count > v_total_drivers * 0.3 THEN
        RAISE NOTICE 'WARNING: High percentage of drivers with heavy workload';
    END IF;
    
    IF v_assignments_made < v_total_drivers * 2 THEN
        RAISE NOTICE 'NOTICE: Low assignment rate - consider adding more shifts';
    ELSE
        RAISE NOTICE 'SUCCESS: Good shift coverage achieved';
    END IF;
    
    RAISE NOTICE '';
    RAISE NOTICE '=======================================';
    RAISE NOTICE 'SCHEDULE MANAGEMENT COMPLETED';
    RAISE NOTICE '=======================================';
    
EXCEPTION
    WHEN OTHERS THEN
        -- Try to close cursor if open
        BEGIN
            IF schedule_ref IS NOT NULL THEN
                CLOSE schedule_ref;
            END IF;
        EXCEPTION
            WHEN OTHERS THEN NULL;
        END;
        RAISE EXCEPTION 'Critical error in Schedule Management System: %', SQLERRM;
END;
$$;