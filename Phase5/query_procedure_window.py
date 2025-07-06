#!/usr/bin/env python3
"""
Query and Procedure Execution Window

This module provides a window for executing database stored procedures and functions.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, date
import psycopg2
from database_connection import db_connection

class QueryProcedureWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("פרוצדורות ושאילתות")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f0f0f0')
        
        # Make window modal
        self.window.transient()
        self.window.grab_set()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main title
        title_frame = tk.Frame(self.window, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=5, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="Database Procedures & Queries\nפרוצדורות ושאילתות בסיס נתונים",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_functions_tab()
        self.create_procedures_tab()
        self.create_queries_tab()
        
        # Results area
        self.create_results_area()
        
    def create_functions_tab(self):
        """Create functions tab"""
        functions_frame = ttk.Frame(self.notebook)
        self.notebook.add(functions_frame, text="Functions / פונקציות")
        
        # Function 1: Maintenance Summary
        func1_frame = tk.LabelFrame(functions_frame, text="1. 🔧 Maintenance Summary / סיכום תחזוקה קרובה", font=('Arial', 10, 'bold'))
        func1_frame.pack(fill='x', padx=10, pady=5)
        
        # Add description
        desc1_label = tk.Label(
            func1_frame, 
            text="מציג אוטובוסים הזקוקים לתחזוקה בתקופה מסוימת\nShows buses requiring maintenance in a specific period",
            font=('Arial', 8),
            fg='#666666',
            justify='left'
        )
        desc1_label.pack(anchor='w', padx=5, pady=2)
        
        tk.Label(func1_frame, text="Days ahead / ימים קדימה:").pack(anchor='w', padx=5)
        self.days_ahead_var = tk.StringVar(value="30")
        days_entry = tk.Entry(func1_frame, textvariable=self.days_ahead_var, width=10)
        days_entry.pack(anchor='w', padx=5, pady=2)
        
        tk.Button(
            func1_frame,
            text="🔍 Execute Maintenance Summary / הפעל סיכום תחזוקה",
            command=self.execute_maintenance_summary,
            bg='#3498db',
            fg='white',
            font=('Arial', 9, 'bold')
        ).pack(pady=5)
        
        # Function 2: Monthly Costs
        func2_frame = tk.LabelFrame(functions_frame, text="2. 💰 Monthly Bus Costs / עלויות חודשיות לכל אוטובוס", font=('Arial', 10, 'bold'))
        func2_frame.pack(fill='x', padx=10, pady=5)
        
        # Add description
        desc2_label = tk.Label(
            func2_frame, 
            text="מציג עלויות חודשיות מפורטות לכל אוטובוס בשנה נתונה\nShows detailed monthly costs for each bus in a given year",
            font=('Arial', 8),
            fg='#666666',
            justify='left'
        )
        desc2_label.pack(anchor='w', padx=5, pady=2)
        
        tk.Label(func2_frame, text="Year / שנה:").pack(anchor='w', padx=5)
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        year_entry = tk.Entry(func2_frame, textvariable=self.year_var, width=10)
        year_entry.pack(anchor='w', padx=5, pady=2)
        
        tk.Button(
            func2_frame,
            text="📊 Execute Monthly Costs / הפעל עלויות חודשיות",
            command=self.execute_monthly_costs,
            bg='#3498db',
            fg='white',
            font=('Arial', 9, 'bold')
        ).pack(pady=5)
        
    def create_procedures_tab(self):
        """Create procedures tab"""
        procedures_frame = ttk.Frame(self.notebook)
        self.notebook.add(procedures_frame, text="Procedures / פרוצדורות")
        
        # Procedure 1: Bus Operation
        proc1_frame = tk.LabelFrame(procedures_frame, text="1. 🚌 Process Bus Operation / עיבוד פעולת אוטובוס", font=('Arial', 10, 'bold'))
        proc1_frame.pack(fill='x', padx=10, pady=5)
        
        # Add description
        desc1_label = tk.Label(
            proc1_frame, 
            text="מוסיף פעולה חדשה לאוטובוס (תדלוק, תחזוקה, בדיקה) ומעדכן רשומות\nAdds a new operation to a bus (fuel, maintenance, inspection) and updates records",
            font=('Arial', 8),
            fg='#666666',
            justify='left'
        )
        desc1_label.pack(anchor='w', padx=5, pady=2)
        
        # Bus ID
        tk.Label(proc1_frame, text="Bus ID / מזהה אוטובוס:").pack(anchor='w', padx=5)
        self.proc_bus_id_var = tk.StringVar(value="1")
        tk.Entry(proc1_frame, textvariable=self.proc_bus_id_var, width=10).pack(anchor='w', padx=5, pady=2)
        
        # Operation Type
        tk.Label(proc1_frame, text="Operation Type / סוג פעולה:").pack(anchor='w', padx=5)
        self.operation_type_var = tk.StringVar(value="FUEL")
        operation_combo = ttk.Combobox(proc1_frame, textvariable=self.operation_type_var, 
                                     values=["FUEL", "MAINTENANCE", "INSPECTION"], width=15)
        operation_combo.pack(anchor='w', padx=5, pady=2)
        
        # Cost
        tk.Label(proc1_frame, text="Cost / עלות:").pack(anchor='w', padx=5)
        self.proc_cost_var = tk.StringVar(value="100.00")
        tk.Entry(proc1_frame, textvariable=self.proc_cost_var, width=10).pack(anchor='w', padx=5, pady=2)
        
        tk.Button(
            proc1_frame,
            text="⚙️ Execute Bus Operation / הפעל פעולת אוטובוס",
            command=self.execute_bus_operation,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 9, 'bold')
        ).pack(pady=5)
        
        # Procedure 2: Weekly Shifts
        proc2_frame = tk.LabelFrame(procedures_frame, text="2. 📅 Assign Weekly Shifts / הקצאת משמרות שבועיות", font=('Arial', 10, 'bold'))
        proc2_frame.pack(fill='x', padx=10, pady=5)
        
        # Add description
        desc2_label = tk.Label(
            proc2_frame, 
            text="מקצה משמרות עבודה לנהגים לשבוע מסוים באופן אוטומטי\nAutomatically assigns work shifts to drivers for a specific week",
            font=('Arial', 8),
            fg='#666666',
            justify='left'
        )
        desc2_label.pack(anchor='w', padx=5, pady=2)
        
        tk.Label(proc2_frame, text="Week Offset / היסט שבועות (0=השבוע הנוכחי):").pack(anchor='w', padx=5)
        self.week_offset_var = tk.StringVar(value="1")
        tk.Entry(proc2_frame, textvariable=self.week_offset_var, width=10).pack(anchor='w', padx=5, pady=2)
        
        tk.Button(
            proc2_frame,
            text="📋 Execute Shift Assignment / הפעל הקצאת משמרות",
            command=self.execute_shift_assignment,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 9, 'bold')
        ).pack(pady=5)
        
    def create_queries_tab(self):
        """Create queries tab"""
        queries_frame = ttk.Frame(self.notebook)
        self.notebook.add(queries_frame, text="Queries / שאילתות")
        
        # Query 1: Yearly Costs
        query1_frame = tk.LabelFrame(queries_frame, text="1. 💵 Yearly Bus Costs / עלויות אוטובוסים שנתיות", font=('Arial', 10, 'bold'))
        query1_frame.pack(fill='x', padx=10, pady=5)
        
        # Add description
        desc1_label = tk.Label(
            query1_frame, 
            text="מציג סיכום עלויות שנתיות לכל אוטובוס, ממויין לפי עלות\nShows annual cost summary for each bus, sorted by cost",
            font=('Arial', 8),
            fg='#666666',
            justify='left'
        )
        desc1_label.pack(anchor='w', padx=5, pady=2)
        
        tk.Label(query1_frame, text="Year / שנה:").pack(anchor='w', padx=5)
        self.query_year_var = tk.StringVar(value=str(datetime.now().year))
        tk.Entry(query1_frame, textvariable=self.query_year_var, width=10).pack(anchor='w', padx=5, pady=2)
        
        tk.Button(
            query1_frame,
            text="📊 Execute Yearly Costs Query / הפעל שאילתת עלויות שנתיות",
            command=self.execute_yearly_costs_query,
            bg='#27ae60',
            fg='white',
            font=('Arial', 9, 'bold')
        ).pack(pady=5)
        
        # Query 2: Expiring Insurance
        query2_frame = tk.LabelFrame(queries_frame, text="2. 🛡️ Expiring Insurance / ביטוחים פגי תוקף", font=('Arial', 10, 'bold'))
        query2_frame.pack(fill='x', padx=10, pady=5)
        
        # Add description
        desc2_label = tk.Label(
            query2_frame, 
            text="מציג ביטוחים שפוגים החודש הנוכחי לצורך חידוש\nShows insurance policies expiring this month for renewal",
            font=('Arial', 8),
            fg='#666666',
            justify='left'
        )
        desc2_label.pack(anchor='w', padx=5, pady=2)
        
        tk.Button(
            query2_frame,
            text="🔍 Execute Expiring Insurance Query / הפעל שאילתת ביטוחים פגי תוקף",
            command=self.execute_expiring_insurance_query,
            bg='#27ae60',
            fg='white',
            font=('Arial', 9, 'bold')
        ).pack(pady=5)
        
        # Query 3: Top Fuel Additions
        query3_frame = tk.LabelFrame(queries_frame, text="3. ⛽ Top Fuel Additions / התדלוקים הגבוהים ביותר", font=('Arial', 10, 'bold'))
        query3_frame.pack(fill='x', padx=10, pady=5)
        
        # Add description
        desc3_label = tk.Label(
            query3_frame, 
            text="מציג את התדלוקים הגבוהים ביותר לפי כמות הדלק\nShows the highest fuel additions by fuel quantity",
            font=('Arial', 8),
            fg='#666666',
            justify='left'
        )
        desc3_label.pack(anchor='w', padx=5, pady=2)
        
        tk.Label(query3_frame, text="Limit / מגבלה:").pack(anchor='w', padx=5)
        self.fuel_limit_var = tk.StringVar(value="5")
        tk.Entry(query3_frame, textvariable=self.fuel_limit_var, width=10).pack(anchor='w', padx=5, pady=2)
        
        tk.Button(
            query3_frame,
            text="⛽ Execute Top Fuel Query / הפעל שאילתת תדלוקים גבוהים",
            command=self.execute_top_fuel_query,
            bg='#27ae60',
            fg='white',
            font=('Arial', 9, 'bold')
        ).pack(pady=5)
        
    def create_results_area(self):
        """Create results display area"""
        results_frame = tk.LabelFrame(self.window, text="Results / תוצאות", font=('Arial', 12, 'bold'))
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create text widget with scrollbar
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=15,
            font=('Consolas', 10),  # Changed to Consolas for better alignment
            wrap=tk.WORD,
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        self.results_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Clear button
        clear_button = tk.Button(
            results_frame,
            text="Clear Results / נקה תוצאות",
            command=self.clear_results,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 9, 'bold')
        )
        clear_button.pack(pady=5)
        
    def clear_results(self):
        """Clear the results area"""
        self.results_text.delete(1.0, tk.END)
        
    def display_results(self, title, data, is_cursor=False, column_headers=None):
        """Display results in the text area with better formatting"""
        self.results_text.insert(tk.END, f"\n{'='*80}\n")
        self.results_text.insert(tk.END, f"📊 {title}\n")
        self.results_text.insert(tk.END, f"{'='*80}\n")
        
        if not data:
            self.results_text.insert(tk.END, "❌ לא נמצאו נתונים / No data found\n")
            self.results_text.insert(tk.END, f"{'='*80}\n")
            self.results_text.see(tk.END)
            return
        
        # Add column headers if provided
        if column_headers:
            header_line = " | ".join(f"{header:<18}" for header in column_headers)
            self.results_text.insert(tk.END, f"{header_line}\n")
            self.results_text.insert(tk.END, f"{'-'*len(header_line)}\n")
        
        # Display data with better formatting
        for i, row in enumerate(data, 1):
            if isinstance(row, tuple):
                # Format each column with appropriate width and alignment
                formatted_items = []
                for item in row:
                    if isinstance(item, float):
                        formatted_items.append(f"{item:>18.2f}")
                    elif isinstance(item, (int, str)) and str(item).replace('.','').isdigit():
                        formatted_items.append(f"{item:>18}")
                    else:
                        formatted_items.append(f"{str(item):<18}")
                
                formatted_row = " | ".join(formatted_items)
                self.results_text.insert(tk.END, f"{formatted_row}\n")
            else:
                self.results_text.insert(tk.END, f"{i:3d}. {row}\n")
                
        self.results_text.insert(tk.END, f"\n✅ סה\"כ שורות: {len(data)} / Total rows: {len(data)}\n")
        self.results_text.insert(tk.END, f"{'='*80}\n")
        self.results_text.see(tk.END)
        
    def execute_maintenance_summary(self):
        """Execute maintenance summary function"""
        try:
            days_ahead = int(self.days_ahead_var.get())
            
            if not db_connection.connect():
                messagebox.showerror("Error", "Cannot connect to database")
                return
                
            cursor = db_connection.connection.cursor()
            
            # Call the function
            cursor.execute("SELECT get_upcoming_maintenance_summary(%s)", (days_ahead,))
            cursor_name = cursor.fetchone()[0]
            
            # Fetch from the returned cursor
            cursor.execute(f"FETCH ALL FROM {cursor_name}")
            results = cursor.fetchall()
            
            cursor.close()
            
            headers = ["Bus ID", "Plate Number", "Maintenance Type", "Due Date", "Priority"]
            self.display_results(
                f"🔧 סיכום תחזוקה - {days_ahead} ימים קדימה / Maintenance Summary - Next {days_ahead} Days", 
                results, 
                column_headers=headers
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error executing maintenance summary: {str(e)}")
            
    def execute_monthly_costs(self):
        """Execute monthly costs function"""
        try:
            year = int(self.year_var.get())
            
            if not db_connection.connect():
                messagebox.showerror("Error", "Cannot connect to database")
                return
                
            cursor = db_connection.connection.cursor()
            cursor.execute("SELECT * FROM get_monthly_bus_costs(%s)", (year,))
            results = cursor.fetchall()
            
            cursor.close()
            
            headers = ["Bus ID", "Plate Number", "Month", "Total Cost", "Operations"]
            self.display_results(
                f"💰 עלויות חודשיות {year} / Monthly Bus Costs for {year}", 
                results,
                column_headers=headers
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error executing monthly costs: {str(e)}")
            
    def execute_bus_operation(self):
        """Execute bus operation procedure"""
        try:
            bus_id = int(self.proc_bus_id_var.get())
            operation_type = self.operation_type_var.get()
            cost = float(self.proc_cost_var.get())
            
            if not db_connection.connect():
                messagebox.showerror("Error", "Cannot connect to database")
                return
                
            cursor = db_connection.connection.cursor()
            
            # Call the procedure
            cursor.execute(
                "CALL process_bus_operation_extended(%s, %s, %s, %s)",
                (bus_id, operation_type, cost, None)
            )
            
            db_connection.connection.commit()
            cursor.close()
            
            operation_desc = {
                'FUEL': 'תדלוק / Fuel',
                'MAINTENANCE': 'תחזוקה / Maintenance', 
                'INSPECTION': 'בדיקה / Inspection'
            }
            
            result_data = [
                (bus_id, operation_desc.get(operation_type, operation_type), f"${cost:.2f}", "✅ הושלם / Completed")
            ]
            
            headers = ["Bus ID", "Operation Type", "Cost", "Status"]
            self.display_results(
                "🚌 עיבוד פעולת אוטובוס / Bus Operation Processed",
                result_data,
                column_headers=headers
            )
            messagebox.showinfo("Success", f"✅ פעולת {operation_desc.get(operation_type, operation_type)} הושלמה בהצלחה!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error executing bus operation: {str(e)}")
            
    def execute_shift_assignment(self):
        """Execute shift assignment procedure"""
        try:
            week_offset = int(self.week_offset_var.get())
            
            if not db_connection.connect():
                messagebox.showerror("Error", "Cannot connect to database")
                return
                
            cursor = db_connection.connection.cursor()
            
            # Call the procedure
            cursor.execute(
                "CALL assign_weekly_shifts_enhanced(%s, %s)",
                (0, week_offset)
            )
            
            db_connection.connection.commit()
            cursor.close()
            
            week_desc = "השבוע הנוכחי" if week_offset == 0 else f"שבוע +{week_offset}"
            result_data = [
                (week_offset, week_desc, "✅ הושלם / Completed", "משמרות הוקצו / Shifts Assigned")
            ]
            
            headers = ["Week Offset", "Description", "Status", "Action"]
            self.display_results(
                "📅 הקצאת משמרות שבועיות / Weekly Shift Assignment",
                result_data,
                column_headers=headers
            )
            messagebox.showinfo("Success", f"✅ הקצאת משמרות ל{week_desc} הושלמה בהצלחה!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error executing shift assignment: {str(e)}")
            
    def execute_yearly_costs_query(self):
        """Execute yearly costs query"""
        try:
            year = int(self.query_year_var.get())
            
            if not db_connection.connect():
                messagebox.showerror("Error", "Cannot connect to database")
                return
                
            cursor = db_connection.connection.cursor()
            cursor.execute("SELECT * FROM query_yearly_bus_costs(%s)", (year,))
            results = cursor.fetchall()
            
            cursor.close()
            
            headers = ["Bus ID", "Plate Number", "Total Cost ($)", "Operations Count"]
            self.display_results(
                f"💵 עלויות שנתיות {year} / Yearly Bus Costs for {year}", 
                results,
                column_headers=headers
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error executing yearly costs query: {str(e)}")
            
    def execute_expiring_insurance_query(self):
        """Execute expiring insurance query"""
        try:
            if not db_connection.connect():
                messagebox.showerror("Error", "Cannot connect to database")
                return
                
            cursor = db_connection.connection.cursor()
            cursor.execute("SELECT * FROM query_expiring_insurance()")
            results = cursor.fetchall()
            
            cursor.close()
            
            headers = ["Insurance ID", "Bus ID", "Plate Number", "Start Date", "End Date", "Days Left"]
            self.display_results(
                "🛡️ ביטוחים פגי תוקף החודש / Expiring Insurance This Month", 
                results,
                column_headers=headers
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error executing expiring insurance query: {str(e)}")
            
    def execute_top_fuel_query(self):
        """Execute top fuel additions query"""
        try:
            limit = int(self.fuel_limit_var.get())
            
            if not db_connection.connect():
                messagebox.showerror("Error", "Cannot connect to database")
                return
                
            cursor = db_connection.connection.cursor()
            cursor.execute("SELECT * FROM query_top_fuel_additions(%s)", (limit,))
            results = cursor.fetchall()
            
            cursor.close()
            
            headers = ["Bus ID", "Plate Number", "Gas Station", "Fuel Added (L)", "Date"]
            self.display_results(
                f"⛽ {limit} התדלוקים הגבוהים ביותר / Top {limit} Fuel Additions", 
                results,
                column_headers=headers
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error executing top fuel query: {str(e)}")

def main():
    """Main function for testing"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    app = QueryProcedureWindow()
    root.mainloop()

if __name__ == "__main__":
    main()
