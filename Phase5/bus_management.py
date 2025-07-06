import tkinter as tk
from tkinter import ttk, messagebox
from database_connection import db_connection

class BusManagementWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("ניהול אוטובוסים")
        self.window.geometry("1000x700")
        self.window.configure(bg='#ecf0f1')
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_widgets()
        self.load_buses()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"1000x700+{x}+{y}")
    
    def create_widgets(self):
        """Create bus management interface"""
        # Title
        title_label = tk.Label(
            self.window, 
            text="ניהול אוטובוסים", 
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
        tk.Label(left_frame, text="מזהה אוטובוס:", font=("Arial", 12), bg='#bdc3c7').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.bus_id_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.bus_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="מספר לוחית:", font=("Arial", 12), bg='#bdc3c7').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.plate_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.plate_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="דגם:", font=("Arial", 12), bg='#bdc3c7').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.model_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.model_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="קיבולת:", font=("Arial", 12), bg='#bdc3c7').grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.capacity_entry = tk.Entry(left_frame, font=("Arial", 12), width=20)
        self.capacity_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(left_frame, text="סטטוס:", font=("Arial", 12), bg='#bdc3c7').grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.status_var = tk.StringVar(value="Active")
        status_combo = ttk.Combobox(left_frame, textvariable=self.status_var, values=["Active", "Inactive"], width=17)
        status_combo.grid(row=4, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(left_frame, bg='#bdc3c7')
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="הוסף", bg='#27ae60', fg='white', font=("Arial", 12), command=self.add_bus, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="עדכן", bg='#f39c12', fg='white', font=("Arial", 12), command=self.update_bus, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="מחק", bg='#e74c3c', fg='white', font=("Arial", 12), command=self.delete_bus, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="נקה", bg='#95a5a6', fg='white', font=("Arial", 12), command=self.clear_form, width=10).pack(side='left', padx=5)
        
        # Right frame for table
        right_frame = tk.Frame(main_frame, bg='#ecf0f1')
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Treeview for displaying buses
        columns = ("ID", "Plate", "Model", "Capacity", "Status")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        self.tree.heading("ID", text="מזהה")
        self.tree.heading("Plate", text="לוחית")
        self.tree.heading("Model", text="דגם")
        self.tree.heading("Capacity", text="קיבולת")
        self.tree.heading("Status", text="סטטוס")
        
        self.tree.column("ID", width=80)
        self.tree.column("Plate", width=120)
        self.tree.column("Model", width=150)
        self.tree.column("Capacity", width=100)
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
            command=self.load_buses
        )
        refresh_btn.pack(pady=10)
    
    def load_buses(self):
        """Load buses from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Query buses
        buses = db_connection.execute_query("SELECT bus_id, plate_number, model, capacity, bus_status FROM Bus ORDER BY bus_id")
        
        if buses:
            for bus in buses:
                # Add color coding based on status
                tag = "active" if bus[4] == "Active" else "inactive"
                self.tree.insert("", "end", values=bus, tags=(tag,))
            
            # Configure tags for colors
            self.tree.tag_configure("active", background="#d5f4e6")
            self.tree.tag_configure("inactive", background="#fadbd8")
    
    def on_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            # Populate form with selected values
            self.bus_id_entry.delete(0, tk.END)
            self.bus_id_entry.insert(0, values[0])
            
            self.plate_entry.delete(0, tk.END)
            self.plate_entry.insert(0, values[1])
            
            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, values[2])
            
            self.capacity_entry.delete(0, tk.END)
            self.capacity_entry.insert(0, values[3])
            
            self.status_var.set(values[4])
    
    def add_bus(self):
        """Add new bus"""
        try:
            bus_id = int(self.bus_id_entry.get())
            plate = self.plate_entry.get().strip()
            model = self.model_entry.get().strip()
            capacity = int(self.capacity_entry.get())
            status = self.status_var.get()
            
            if not all([plate, model]):
                messagebox.showerror("שגיאה", "יש למלא את כל השדות החובה")
                return
            
            query = """INSERT INTO Bus (bus_id, plate_number, model, capacity, bus_status) 
                      VALUES (%s, %s, %s, %s, %s)"""
            
            if db_connection.execute_non_query(query, (bus_id, plate, model, capacity, status)):
                messagebox.showinfo("הצלחה", "האוטובוס נוסף בהצלחה")
                self.clear_form()
                self.load_buses()
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש להזין ערכים תקינים")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהוספת האוטובוס: {e}")
    
    def update_bus(self):
        """Update existing bus"""
        try:
            bus_id = int(self.bus_id_entry.get())
            plate = self.plate_entry.get().strip()
            model = self.model_entry.get().strip()
            capacity = int(self.capacity_entry.get())
            status = self.status_var.get()
            
            if not all([plate, model]):
                messagebox.showerror("שגיאה", "יש למלא את כל השדות החובה")
                return
            
            query = """UPDATE Bus SET plate_number=%s, model=%s, capacity=%s, bus_status=%s 
                      WHERE bus_id=%s"""
            
            if db_connection.execute_non_query(query, (plate, model, capacity, status, bus_id)):
                messagebox.showinfo("הצלחה", "האוטובוס עודכן בהצלחה")
                self.clear_form()
                self.load_buses()
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש להזין ערכים תקינים")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בעדכון האוטובוס: {e}")
    
    def delete_bus(self):
        """Delete selected bus"""
        try:
            bus_id = int(self.bus_id_entry.get())
            
            if messagebox.askyesno("אישור מחיקה", f"האם אתה בטוח שברצונך למחוק את האוטובוס {bus_id}?"):
                query = "DELETE FROM Bus WHERE bus_id=%s"
                
                if db_connection.execute_non_query(query, (bus_id,)):
                    messagebox.showinfo("הצלחה", "האוטובוס נמחק בהצלחה")
                    self.clear_form()
                    self.load_buses()
        
        except ValueError:
            messagebox.showerror("שגיאה", "יש לבחור אוטובוס למחיקה")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה במחיקת האוטובוס: {e}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.bus_id_entry.delete(0, tk.END)
        self.plate_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        self.status_var.set("Active")
