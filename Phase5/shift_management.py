import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from database_connection import db_connection

class ShiftManagementWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("ניהול משמרות")
        self.window.geometry("1200x800")
        self.window.configure(bg='#ecf0f1')
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_widgets()
        self.load_shifts()
        self.load_drivers()
        self.load_buses()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.window.winfo_screenheight() // 2) - (800 // 2)
        self.window.geometry(f"1200x800+{x}+{y}")
    
    def create_widgets(self):
        """Create shift management interface"""
        # Title
        title_label = tk.Label(
            self.window, 
            text="ניהול משמרות", 
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
        tk.Label(left_frame, text="מזהה משמרת:", font=("Arial", 12), bg='#bdc3c7').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.shift_id_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.shift_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="תאריך משמרת:", font=("Arial", 12), bg='#bdc3c7').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.date_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="שעת התחלה:", font=("Arial", 12), bg='#bdc3c7').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.start_time_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.start_time_entry.insert(0, "06:00:00")
        self.start_time_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="שעת סיום:", font=("Arial", 12), bg='#bdc3c7').grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.end_time_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.end_time_entry.insert(0, "14:00:00")
        self.end_time_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="נהג:", font=("Arial", 12), bg='#bdc3c7').grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.driver_var = tk.StringVar()
        self.driver_combo = ttk.Combobox(left_frame, textvariable=self.driver_var, width=17, state="readonly")
        self.driver_combo.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="אוטובוס:", font=("Arial", 12), bg='#bdc3c7').grid(row=5, column=0, sticky='e', padx=5, pady=5)
        self.bus_var = tk.StringVar()
        self.bus_combo = ttk.Combobox(left_frame, textvariable=self.bus_var, width=17, state="readonly")
        self.bus_combo.grid(row=5, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(left_frame, bg='#bdc3c7')
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="הוסף", bg='#27ae60', fg='white', font=("Arial", 12), command=self.add_shift, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="עדכן", bg='#f39c12', fg='white', font=("Arial", 12), command=self.update_shift, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="מחק", bg='#e74c3c', fg='white', font=("Arial", 12), command=self.delete_shift, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="נקה", bg='#95a5a6', fg='white', font=("Arial", 12), command=self.clear_form, width=10).pack(side='left', padx=5)
        
        # Right frame for table
        right_frame = tk.Frame(main_frame, bg='#ecf0f1')
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Treeview for displaying shifts
        columns = ("ID", "Date", "Start", "End", "Driver", "Bus")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=25)
        
        # Configure columns
        self.tree.heading("ID", text="מזהה")
        self.tree.heading("Date", text="תאריך")
        self.tree.heading("Start", text="התחלה")
        self.tree.heading("End", text="סיום")
        self.tree.heading("Driver", text="נהג")
        self.tree.heading("Bus", text="אוטובוס")
        
        self.tree.column("ID", width=70)
        self.tree.column("Date", width=100)
        self.tree.column("Start", width=80)
        self.tree.column("End", width=80)
        self.tree.column("Driver", width=150)
        self.tree.column("Bus", width=100)
        
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
            command=self.load_shifts
        )
        refresh_btn.pack(pady=10)
    
    def load_drivers(self):
        """Load drivers for combobox"""
        drivers = db_connection.execute_query("SELECT driver_id, first_name, last_name FROM Driver WHERE driver_status = 'Active' ORDER BY first_name, last_name")
        
        if drivers:
            driver_list = [f"{driver[0]} - {driver[1]} {driver[2]}" for driver in drivers]
            self.driver_combo['values'] = driver_list
    
    def load_buses(self):
        """Load buses for combobox"""
        buses = db_connection.execute_query("SELECT bus_id, plate_number FROM Bus WHERE bus_status = 'Active' ORDER BY bus_id")
        
        if buses:
            bus_list = [f"{bus[0]} - {bus[1]}" for bus in buses]
            self.bus_combo['values'] = bus_list
    
    def load_shifts(self):
        """Load shifts from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Query shifts with driver and bus details
        query = """
        SELECT s.shift_id, s.shift_date, s.start_time, s.end_time,
               d.first_name || ' ' || d.last_name as driver_name,
               b.plate_number
        FROM Shift s
        JOIN Driver d ON s.driver_id = d.driver_id
        JOIN Bus b ON s.bus_id = b.bus_id
        ORDER BY s.shift_date DESC, s.start_time
        """
        
        shifts = db_connection.execute_query(query)
        
        if shifts:
            for shift in shifts:
                # Color code based on date
                shift_date = shift[1]
                today = date.today()
                
                if shift_date == today:
                    tag = "today"
                elif shift_date > today:
                    tag = "future"
                else:
                    tag = "past"
                
                self.tree.insert("", "end", values=shift, tags=(tag,))
            
            # Configure tags for colors
            self.tree.tag_configure("today", background="#d5f4e6")
            self.tree.tag_configure("future", background="#e3f2fd")
            self.tree.tag_configure("past", background="#fafafa")
    
    def on_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            # Get full shift details
            shift_id = values[0]
            shift_details = db_connection.execute_query(
                "SELECT shift_id, shift_date, start_time, end_time, driver_id, bus_id FROM Shift WHERE shift_id = %s",
                (shift_id,)
            )
            
            if shift_details:
                shift = shift_details[0]
                
                # Populate form with selected values
                self.shift_id_entry.delete(0, tk.END)
                self.shift_id_entry.insert(0, shift[0])
                
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, shift[1])
                
                self.start_time_entry.delete(0, tk.END)
                self.start_time_entry.insert(0, shift[2])
                
                self.end_time_entry.delete(0, tk.END)
                self.end_time_entry.insert(0, shift[3] if shift[3] else "")
                
                # Set driver and bus combo values
                for i, value in enumerate(self.driver_combo['values']):
                    if value.startswith(str(shift[4])):
                        self.driver_combo.current(i)
                        break
                
                for i, value in enumerate(self.bus_combo['values']):
                    if value.startswith(str(shift[5])):
                        self.bus_combo.current(i)
                        break
    
    def add_shift(self):
        """Add new shift"""
        try:
            shift_id = int(self.shift_id_entry.get())
            shift_date = self.date_entry.get()
            start_time = self.start_time_entry.get()
            end_time = self.end_time_entry.get()
            
            # Extract driver and bus IDs from combo selections
            driver_selection = self.driver_var.get()
            bus_selection = self.bus_var.get()
            
            if not all([shift_date, start_time, driver_selection, bus_selection]):
                messagebox.showerror("שגיאה", "יש למלא את כל השדות החובה")
                return
            
            driver_id = int(driver_selection.split(' - ')[0])
            bus_id = int(bus_selection.split(' - ')[0])
            
            query = """INSERT INTO Shift (shift_id, shift_date, start_time, end_time, driver_id, bus_id) 
                      VALUES (%s, %s, %s, %s, %s, %s)"""
            
            params = (shift_id, shift_date, start_time, end_time if end_time else None, driver_id, bus_id)
            
            if db_connection.execute_non_query(query, params):
                messagebox.showinfo("הצלחה", "המשמרת נוספה בהצלחה")
                self.clear_form()
                self.load_shifts()
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש להזין ערכים תקינים")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהוספת המשמרת: {e}")
    
    def update_shift(self):
        """Update existing shift"""
        try:
            shift_id = int(self.shift_id_entry.get())
            shift_date = self.date_entry.get()
            start_time = self.start_time_entry.get()
            end_time = self.end_time_entry.get()
            
            # Extract driver and bus IDs from combo selections
            driver_selection = self.driver_var.get()
            bus_selection = self.bus_var.get()
            
            if not all([shift_date, start_time, driver_selection, bus_selection]):
                messagebox.showerror("שגיאה", "יש למלא את כל השדות החובה")
                return
            
            driver_id = int(driver_selection.split(' - ')[0])
            bus_id = int(bus_selection.split(' - ')[0])
            
            query = """UPDATE Shift SET shift_date=%s, start_time=%s, end_time=%s, driver_id=%s, bus_id=%s 
                      WHERE shift_id=%s"""
            
            params = (shift_date, start_time, end_time if end_time else None, driver_id, bus_id, shift_id)
            
            if db_connection.execute_non_query(query, params):
                messagebox.showinfo("הצלחה", "המשמרת עודכנה בהצלחה")
                self.clear_form()
                self.load_shifts()
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש להזין ערכים תקינים")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בעדכון המשמרת: {e}")
    
    def delete_shift(self):
        """Delete selected shift"""
        try:
            shift_id = int(self.shift_id_entry.get())
            
            if messagebox.askyesno("אישור מחיקה", f"האם אתה בטוח שברצונך למחוק את המשמרת {shift_id}?"):
                query = "DELETE FROM Shift WHERE shift_id=%s"
                
                if db_connection.execute_non_query(query, (shift_id,)):
                    messagebox.showinfo("הצלחה", "המשמרת נמחקה בהצלחה")
                    self.clear_form()
                    self.load_shifts()
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש לבחור משמרת למחיקה")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה במחיקת המשמרת: {e}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.shift_id_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.start_time_entry.delete(0, tk.END)
        self.start_time_entry.insert(0, "06:00:00")
        self.end_time_entry.delete(0, tk.END)
        self.end_time_entry.insert(0, "14:00:00")
        self.driver_var.set("")
        self.bus_var.set("")
