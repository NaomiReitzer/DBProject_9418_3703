import tkinter as tk
from tkinter import ttk, messagebox
from database_connection import db_connection

class DriverManagementWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("ניהול נהגים")
        self.window.geometry("1000x700")
        self.window.configure(bg='#ecf0f1')
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_widgets()
        self.load_drivers()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"1000x700+{x}+{y}")
    
    def create_widgets(self):
        """Create driver management interface"""
        # Title
        title_label = tk.Label(
            self.window, 
            text="ניהול נהגים", 
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
        tk.Label(left_frame, text="מזהה נהג:", font=("Arial", 12), bg='#bdc3c7').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.driver_id_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.driver_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="תעודת זהות:", font=("Arial", 12), bg='#bdc3c7').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.id_number_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.id_number_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="שם פרטי:", font=("Arial", 12), bg='#bdc3c7').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.first_name_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.first_name_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="שם משפחה:", font=("Arial", 12), bg='#bdc3c7').grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.last_name_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.last_name_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="טלפון:", font=("Arial", 12), bg='#bdc3c7').grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.phone_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.phone_entry.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="סטטוס:", font=("Arial", 12), bg='#bdc3c7').grid(row=5, column=0, sticky='e', padx=5, pady=5)
        self.status_var = tk.StringVar(value="Active")
        status_combo = ttk.Combobox(left_frame, textvariable=self.status_var, values=["Active", "Inactive", "On Leave"], width=17)
        status_combo.grid(row=5, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(left_frame, bg='#bdc3c7')
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="הוסף", bg='#27ae60', fg='white', font=("Arial", 12), command=self.add_driver, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="עדכן", bg='#f39c12', fg='white', font=("Arial", 12), command=self.update_driver, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="מחק", bg='#e74c3c', fg='white', font=("Arial", 12), command=self.delete_driver, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="נקה", bg='#95a5a6', fg='white', font=("Arial", 12), command=self.clear_form, width=10).pack(side='left', padx=5)
        
        # Right frame for table
        right_frame = tk.Frame(main_frame, bg='#ecf0f1')
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Treeview for displaying drivers
        columns = ("ID", "ID_Number", "First_Name", "Last_Name", "Phone", "Status")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        self.tree.heading("ID", text="מזהה")
        self.tree.heading("ID_Number", text="ת.ז.")
        self.tree.heading("First_Name", text="שם פרטי")
        self.tree.heading("Last_Name", text="שם משפחה")
        self.tree.heading("Phone", text="טלפון")
        self.tree.heading("Status", text="סטטוס")
        
        self.tree.column("ID", width=60)
        self.tree.column("ID_Number", width=100)
        self.tree.column("First_Name", width=100)
        self.tree.column("Last_Name", width=100)
        self.tree.column("Phone", width=100)
        self.tree.column("Status", width=100)
        
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
            command=self.load_drivers
        )
        refresh_btn.pack(pady=10)
    
    def load_drivers(self):
        """Load drivers from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Query drivers
        drivers = db_connection.execute_query("SELECT driver_id, id_number, first_name, last_name, phone, driver_status FROM Driver ORDER BY driver_id")
        
        if drivers:
            for driver in drivers:
                # Add color coding based on status
                if driver[5] == "Active":
                    tag = "active"
                elif driver[5] == "Inactive":
                    tag = "inactive"
                else:
                    tag = "leave"
                
                self.tree.insert("", "end", values=driver, tags=(tag,))
            
            # Configure tags for colors
            self.tree.tag_configure("active", background="#d5f4e6")
            self.tree.tag_configure("inactive", background="#fadbd8")
            self.tree.tag_configure("leave", background="#fff3cd")
    
    def on_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            # Populate form with selected values
            self.driver_id_entry.delete(0, tk.END)
            self.driver_id_entry.insert(0, values[0])
            
            self.id_number_entry.delete(0, tk.END)
            self.id_number_entry.insert(0, values[1])
            
            self.first_name_entry.delete(0, tk.END)
            self.first_name_entry.insert(0, values[2])
            
            self.last_name_entry.delete(0, tk.END)
            self.last_name_entry.insert(0, values[3])
            
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, values[4] if values[4] else "")
            
            self.status_var.set(values[5])
    
    def add_driver(self):
        """Add new driver"""
        try:
            driver_id = int(self.driver_id_entry.get())
            id_number = self.id_number_entry.get().strip()
            first_name = self.first_name_entry.get().strip()
            last_name = self.last_name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            status = self.status_var.get()
            
            if not all([id_number, first_name, last_name]):
                messagebox.showerror("שגיאה", "יש למלא את כל השדות החובה")
                return
            
            query = """INSERT INTO Driver (driver_id, id_number, first_name, last_name, phone, driver_status) 
                      VALUES (%s, %s, %s, %s, %s, %s)"""
            
            if db_connection.execute_non_query(query, (driver_id, id_number, first_name, last_name, phone or None, status)):
                messagebox.showinfo("הצלחה", "הנהג נוסף בהצלחה")
                self.clear_form()
                self.load_drivers()
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש להזין ערכים תקינים")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהוספת הנהג: {e}")
    
    def update_driver(self):
        """Update existing driver"""
        try:
            driver_id = int(self.driver_id_entry.get())
            id_number = self.id_number_entry.get().strip()
            first_name = self.first_name_entry.get().strip()
            last_name = self.last_name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            status = self.status_var.get()
            
            if not all([id_number, first_name, last_name]):
                messagebox.showerror("שגיאה", "יש למלא את כל השדות החובה")
                return
            
            query = """UPDATE Driver SET id_number=%s, first_name=%s, last_name=%s, phone=%s, driver_status=%s 
                      WHERE driver_id=%s"""
            
            if db_connection.execute_non_query(query, (id_number, first_name, last_name, phone or None, status, driver_id)):
                messagebox.showinfo("הצלחה", "הנהג עודכן בהצלחה")
                self.clear_form()
                self.load_drivers()
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש להזין ערכים תקינים")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בעדכון הנהג: {e}")
    
    def delete_driver(self):
        """Delete selected driver"""
        try:
            driver_id = int(self.driver_id_entry.get())
            
            if messagebox.askyesno("אישור מחיקה", f"האם אתה בטוח שברצונך למחוק את הנהג {driver_id}?"):
                query = "DELETE FROM Driver WHERE driver_id=%s"
                
                if db_connection.execute_non_query(query, (driver_id,)):
                    messagebox.showinfo("הצלחה", "הנהג נמחק בהצלחה")
                    self.clear_form()
                    self.load_drivers()
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש לבחור נהג למחיקה")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה במחיקת הנהג: {e}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.driver_id_entry.delete(0, tk.END)
        self.id_number_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.status_var.set("Active")
