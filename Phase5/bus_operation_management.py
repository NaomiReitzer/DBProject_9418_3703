import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from database_connection import db_connection

class BusOperationManagementWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("ניהול פעולות אוטובוס")
        self.window.geometry("1200x800")
        self.window.configure(bg='#ecf0f1')
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_widgets()
        self.load_operations()
        self.load_buses()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.window.winfo_screenheight() // 2) - (800 // 2)
        self.window.geometry(f"1200x800+{x}+{y}")
    
    def create_widgets(self):
        """Create bus operation management interface"""
        # Title
        title_label = tk.Label(
            self.window, 
            text="ניהול פעולות אוטובוס", 
            font=("Arial", 20, "bold"),
            bg='#ecf0f1', 
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Main frame
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left frame for form
        left_frame = tk.Frame(main_frame, bg='#bdc3c7', padx=20, pady=20)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Form fields
        tk.Label(left_frame, text="מזהה פעולה:", font=("Arial", 12), bg='#bdc3c7').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.operation_id_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.operation_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="תאריך פעולה:", font=("Arial", 12), bg='#bdc3c7').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.date_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="עלות פעולה:", font=("Arial", 12), bg='#bdc3c7').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.cost_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.cost_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="אוטובוס:", font=("Arial", 12), bg='#bdc3c7').grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.bus_var = tk.StringVar()
        self.bus_combo = ttk.Combobox(left_frame, textvariable=self.bus_var, width=17, state="readonly")
        self.bus_combo.grid(row=3, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(left_frame, bg='#bdc3c7')
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="הוסף", bg='#27ae60', fg='white', font=("Arial", 12), command=self.add_operation, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="עדכן", bg='#f39c12', fg='white', font=("Arial", 12), command=self.update_operation, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="מחק", bg='#e74c3c', fg='white', font=("Arial", 12), command=self.delete_operation, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="נקה", bg='#95a5a6', fg='white', font=("Arial", 12), command=self.clear_form, width=10).pack(side='left', padx=5)
        
        # Operation details frame
        details_frame = tk.LabelFrame(left_frame, text="פרטי פעולה נוספים", bg='#bdc3c7', fg='#2c3e50', font=("Arial", 12, "bold"))
        details_frame.grid(row=5, column=0, columnspan=2, pady=20, sticky='ew')
        
        # Tabs for different operation types
        self.notebook = ttk.Notebook(details_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Fuel tab
        fuel_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(fuel_frame, text="דלק")
        
        tk.Label(fuel_frame, text="כמות דלק התחלתית:", bg='#ecf0f1').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.start_fuel_entry = tk.Entry(fuel_frame, width=15)
        self.start_fuel_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(fuel_frame, text="תחנת דלק:", bg='#ecf0f1').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.station_entry = tk.Entry(fuel_frame, width=15)
        self.station_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(fuel_frame, text="כמות דלק שנוספה:", bg='#ecf0f1').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.fuel_added_entry = tk.Entry(fuel_frame, width=15)
        self.fuel_added_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Button(fuel_frame, text="הוסף רישום דלק", bg='#3498db', fg='white', command=self.add_fuel_log).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Maintenance tab
        maintenance_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(maintenance_frame, text="תחזוקה")
        
        tk.Label(maintenance_frame, text="סוג תחזוקה:", bg='#ecf0f1').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.maintenance_type_entry = tk.Entry(maintenance_frame, width=15)
        self.maintenance_type_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(maintenance_frame, text="מי ביצע:", bg='#ecf0f1').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.maintainer_entry = tk.Entry(maintenance_frame, width=15)
        self.maintainer_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(maintenance_frame, text="תאריך תחזוקה הבא:", bg='#ecf0f1').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.next_due_entry = tk.Entry(maintenance_frame, width=15)
        self.next_due_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Button(maintenance_frame, text="הוסף תחזוקה", bg='#3498db', fg='white', command=self.add_maintenance).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Inspection tab
        inspection_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(inspection_frame, text="בדיקה")
        
        tk.Label(inspection_frame, text="סוג בדיקה:", bg='#ecf0f1').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.inspection_type_entry = tk.Entry(inspection_frame, width=15)
        self.inspection_type_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(inspection_frame, text="תוצאת בדיקה:", bg='#ecf0f1').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.inspection_result_var = tk.StringVar(value="Pass")
        inspection_combo = ttk.Combobox(inspection_frame, textvariable=self.inspection_result_var, values=["Pass", "Fail"], width=12)
        inspection_combo.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(inspection_frame, text="שם הבודק:", bg='#ecf0f1').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.inspector_entry = tk.Entry(inspection_frame, width=15)
        self.inspector_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Button(inspection_frame, text="הוסף בדיקה", bg='#3498db', fg='white', command=self.add_inspection).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Right frame for table
        right_frame = tk.Frame(main_frame, bg='#ecf0f1')
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Treeview for displaying operations
        columns = ("ID", "Date", "Cost", "Bus")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=30)
        
        # Configure columns
        self.tree.heading("ID", text="מזהה")
        self.tree.heading("Date", text="תאריך")
        self.tree.heading("Cost", text="עלות")
        self.tree.heading("Bus", text="אוטובוס")
        
        self.tree.column("ID", width=80)
        self.tree.column("Date", width=100)
        self.tree.column("Cost", width=100)
        self.tree.column("Bus", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Refresh button
        refresh_btn = tk.Button(
            right_frame, 
            text="רענן", 
            bg='#3498db', 
            fg='white', 
            font=("Arial", 12),
            command=self.load_operations
        )
        refresh_btn.pack(pady=10)
    
    def load_buses(self):
        """Load buses for combobox"""
        buses = db_connection.execute_query("SELECT bus_id, plate_number FROM Bus ORDER BY bus_id")
        
        if buses:
            bus_list = [f"{bus[0]} - {bus[1]}" for bus in buses]
            self.bus_combo['values'] = bus_list
    
    def load_operations(self):
        """Load operations from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Query operations with bus details
        query = """
        SELECT bo.operation_id, bo.operation_date, bo.operation_cost, b.plate_number
        FROM BusOperation bo
        JOIN Bus b ON bo.bus_id = b.bus_id
        ORDER BY bo.operation_date DESC, bo.operation_id
        """
        
        operations = db_connection.execute_query(query)
        
        if operations:
            for operation in operations:
                # Color code based on cost
                cost = float(operation[2])
                
                if cost > 500:
                    tag = "high_cost"
                elif cost > 200:
                    tag = "medium_cost"
                else:
                    tag = "low_cost"
                
                self.tree.insert("", "end", values=operation, tags=(tag,))
            
            # Configure tags for colors
            self.tree.tag_configure("high_cost", background="#fadbd8")
            self.tree.tag_configure("medium_cost", background="#fff3cd")
            self.tree.tag_configure("low_cost", background="#d5f4e6")
    
    def on_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            # Get full operation details
            operation_id = values[0]
            operation_details = db_connection.execute_query(
                "SELECT operation_id, operation_date, operation_cost, bus_id FROM BusOperation WHERE operation_id = %s",
                (operation_id,)
            )
            
            if operation_details:
                operation = operation_details[0]
                
                # Populate form with selected values
                self.operation_id_entry.delete(0, tk.END)
                self.operation_id_entry.insert(0, operation[0])
                
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, operation[1])
                
                self.cost_entry.delete(0, tk.END)
                self.cost_entry.insert(0, operation[2])
                
                # Set bus combo value
                for i, value in enumerate(self.bus_combo['values']):
                    if value.startswith(str(operation[3])):
                        self.bus_combo.current(i)
                        break
    
    def add_operation(self):
        """Add new operation"""
        try:
            operation_id = int(self.operation_id_entry.get())
            operation_date = self.date_entry.get()
            operation_cost = float(self.cost_entry.get())
            
            # Extract bus ID from combo selection
            bus_selection = self.bus_var.get()
            
            if not all([operation_date, str(operation_cost), bus_selection]):
                messagebox.showerror("שגיאה", "יש למלא את כל השדות החובה")
                return
            
            bus_id = int(bus_selection.split(' - ')[0])
            
            query = """INSERT INTO BusOperation (operation_id, operation_date, operation_cost, bus_id) 
                      VALUES (%s, %s, %s, %s)"""
            
            if db_connection.execute_non_query(query, (operation_id, operation_date, operation_cost, bus_id)):
                messagebox.showinfo("הצלחה", "הפעולה נוספה בהצלחה")
                self.clear_form()
                self.load_operations()
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש להזין ערכים תקינים")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהוספת הפעולה: {e}")
    
    def update_operation(self):
        """Update existing operation"""
        try:
            operation_id = int(self.operation_id_entry.get())
            operation_date = self.date_entry.get()
            operation_cost = float(self.cost_entry.get())
            
            # Extract bus ID from combo selection
            bus_selection = self.bus_var.get()
            
            if not all([operation_date, str(operation_cost), bus_selection]):
                messagebox.showerror("שגיאה", "יש למלא את כל השדות החובה")
                return
            
            bus_id = int(bus_selection.split(' - ')[0])
            
            query = """UPDATE BusOperation SET operation_date=%s, operation_cost=%s, bus_id=%s 
                      WHERE operation_id=%s"""
            
            if db_connection.execute_non_query(query, (operation_date, operation_cost, bus_id, operation_id)):
                messagebox.showinfo("הצלחה", "הפעולה עודכנה בהצלחה")
                self.clear_form()
                self.load_operations()
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש להזין ערכים תקינים")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בעדכון הפעולה: {e}")
    
    def delete_operation(self):
        """Delete selected operation"""
        try:
            operation_id = int(self.operation_id_entry.get())
            
            if messagebox.askyesno("אישור מחיקה", f"האם אתה בטוח שברצונך למחוק את הפעולה {operation_id}?"):
                query = "DELETE FROM BusOperation WHERE operation_id=%s"
                
                if db_connection.execute_non_query(query, (operation_id,)):
                    messagebox.showinfo("הצלחה", "הפעולה נמחקה בהצלחה")
                    self.clear_form()
                    self.load_operations()
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש לבחור פעולה למחיקה")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה במחיקת הפעולה: {e}")
    
    def add_fuel_log(self):
        """Add fuel log for current operation"""
        try:
            operation_id = int(self.operation_id_entry.get())
            start_fuel = float(self.start_fuel_entry.get())
            station = self.station_entry.get().strip()
            fuel_added = float(self.fuel_added_entry.get())
            
            if not all([str(start_fuel), station, str(fuel_added)]):
                messagebox.showerror("שגיאה", "יש למלא את כל שדות הדלק")
                return
            
            query = """INSERT INTO FuelLog (start_fuel_amount_liters, station_name, fuel_added_liters, operation_id) 
                      VALUES (%s, %s, %s, %s)"""
            
            if db_connection.execute_non_query(query, (start_fuel, station, fuel_added, operation_id)):
                messagebox.showinfo("הצלחה", "רישום הדלק נוסף בהצלחה")
                # Clear fuel fields
                self.start_fuel_entry.delete(0, tk.END)
                self.station_entry.delete(0, tk.END)
                self.fuel_added_entry.delete(0, tk.END)
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש להזין ערכים תקינים עבור הדלק")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהוספת רישום הדלק: {e}")
    
    def add_maintenance(self):
        """Add maintenance record for current operation"""
        try:
            operation_id = int(self.operation_id_entry.get())
            maintenance_type = self.maintenance_type_entry.get().strip()
            maintainer = self.maintainer_entry.get().strip()
            next_due = self.next_due_entry.get()
            
            if not all([maintenance_type, maintainer, next_due]):
                messagebox.showerror("שגיאה", "יש למלא את כל שדות התחזוקה")
                return
            
            query = """INSERT INTO Maintenance (maintenance_type, who_maintained, next_due_date, operation_id) 
                      VALUES (%s, %s, %s, %s)"""
            
            if db_connection.execute_non_query(query, (maintenance_type, maintainer, next_due, operation_id)):
                messagebox.showinfo("הצלחה", "רישום התחזוקה נוסף בהצלחה")
                # Clear maintenance fields
                self.maintenance_type_entry.delete(0, tk.END)
                self.maintainer_entry.delete(0, tk.END)
                self.next_due_entry.delete(0, tk.END)
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש להזין ערכים תקינים עבור התחזוקה")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהוספת רישום התחזוקה: {e}")
    
    def add_inspection(self):
        """Add inspection record for current operation"""
        try:
            operation_id = int(self.operation_id_entry.get())
            inspection_type = self.inspection_type_entry.get().strip()
            inspection_result = self.inspection_result_var.get()
            inspector = self.inspector_entry.get().strip()
            
            if not all([inspection_type, inspector]):
                messagebox.showerror("שגיאה", "יש למלא את כל שדות הבדיקה")
                return
            
            query = """INSERT INTO Inspection (inspection_type, inspection_result, inspector_name, operation_id) 
                      VALUES (%s, %s, %s, %s)"""
            
            if db_connection.execute_non_query(query, (inspection_type, inspection_result, inspector, operation_id)):
                messagebox.showinfo("הצלחה", "רישום הבדיקה נוסף בהצלחה")
                # Clear inspection fields
                self.inspection_type_entry.delete(0, tk.END)
                self.inspector_entry.delete(0, tk.END)
                self.inspection_result_var.set("Pass")
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש להזין ערכים תקינים עבור הבדיקה")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהוספת רישום הבדיקה: {e}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.operation_id_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.cost_entry.delete(0, tk.END)
        self.bus_var.set("")
        
        # Clear detail fields
        self.start_fuel_entry.delete(0, tk.END)
        self.station_entry.delete(0, tk.END)
        self.fuel_added_entry.delete(0, tk.END)
        self.maintenance_type_entry.delete(0, tk.END)
        self.maintainer_entry.delete(0, tk.END)
        self.next_due_entry.delete(0, tk.END)
        self.inspection_type_entry.delete(0, tk.END)
        self.inspector_entry.delete(0, tk.END)
        self.inspection_result_var.set("Pass")
