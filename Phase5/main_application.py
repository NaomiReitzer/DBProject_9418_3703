import tkinter as tk
from tkinter import ttk, messagebox
import sys
from database_connection import db_connection

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("מערכת ניהול אוטובוסים - תפריט ראשי")
        self.root.geometry("800x600")
        self.root.configure(bg='#34495e')
        
        # Center the window
        self.center_window()
        
        # Create UI
        self.create_widgets()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
    
    def create_widgets(self):
        """Create main application interface"""
        # Header frame
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Main title
        title_label = tk.Label(
            header_frame, 
            text="מערכת ניהול אוטובוסים", 
            font=("Arial", 28, "bold"),
            bg='#2c3e50', 
            fg='white'
        )
        title_label.pack(expand=True)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame, 
            text="ממשק גרפי לניהול צי אוטובוסים, נהגים ומשמרות", 
            font=("Arial", 12),
            bg='#2c3e50', 
            fg='#bdc3c7'
        )
        subtitle_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#34495e')
        content_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Menu buttons frame
        buttons_frame = tk.Frame(content_frame, bg='#34495e')
        buttons_frame.pack(expand=True)
        
        # Create styled buttons with icons and descriptions
        self.create_menu_button(
            buttons_frame, 
            "ניהול אוטובוסים", 
            "הוספה, עדכון ומחיקה של אוטובוסים בצי",
            '#3498db',
            self.open_bus_management,
            0, 0
        )
        
        self.create_menu_button(
            buttons_frame, 
            "ניהול נהגים", 
            "הוספה, עדכון ומחיקה של נהגים במערכת",
            '#e67e22',
            self.open_driver_management,
            0, 1
        )
        
        self.create_menu_button(
            buttons_frame, 
            "ניהול משמרות", 
            "תזמון והקצאת משמרות לנהגים ואוטובוסים",
            '#9b59b6',
            self.open_shift_management,
            1, 0
        )
        
        self.create_menu_button(
            buttons_frame, 
            "ניהול פעולות", 
            "רישום פעולות תחזוקה, דלק ובדיקות",
            '#27ae60',
            self.open_operation_management,
            1, 1
        )
        
        self.create_menu_button(
            buttons_frame, 
            "שאילתות ופרוצדורות", 
            "הפעלת פונקציות, פרוצדורות ושאילתות מתקדמות",
            '#e74c3c',
            self.open_query_procedures,
            2, 0
        )
        
        # Status and control frame
        control_frame = tk.Frame(content_frame, bg='#34495e')
        control_frame.pack(fill='x', pady=20)
        
        # Database status
        self.status_label = tk.Label(
            control_frame, 
            text="מחובר לבסיס הנתונים", 
            font=("Arial", 12),
            bg='#34495e', 
            fg='#27ae60'
        )
        self.status_label.pack()
        
        # Exit button
        exit_button = tk.Button(
            control_frame,
            text="יציאה מהמערכת",
            font=("Arial", 14, "bold"),
            bg='#95a5a6',
            fg='white',
            command=self.on_closing,
            width=20,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        exit_button.pack(pady=20)
    
    def create_menu_button(self, parent, title, description, color, command, row, col):
        """Create a styled menu button with title and description"""
        # Button frame
        button_frame = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=3)
        button_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Title label
        title_label = tk.Label(
            button_frame,
            text=title,
            font=("Arial", 16, "bold"),
            bg=color,
            fg='white',
            wraplength=200
        )
        title_label.pack(pady=10)
        
        # Description label
        desc_label = tk.Label(
            button_frame,
            text=description,
            font=("Arial", 10),
            bg=color,
            fg='white',
            wraplength=180,
            justify='center'
        )
        desc_label.pack(pady=5)
        
        # Click button
        click_button = tk.Button(
            button_frame,
            text="לחץ להכנס",
            font=("Arial", 12, "bold"),
            bg='white',
            fg=color,
            command=command,
            relief=tk.RAISED,
            bd=2
        )
        click_button.pack(pady=10)
        
        # Make the entire frame clickable
        def on_frame_click(event):
            command()
        
        button_frame.bind("<Button-1>", on_frame_click)
        title_label.bind("<Button-1>", on_frame_click)
        desc_label.bind("<Button-1>", on_frame_click)
        
        # Add hover effects
        def on_enter(event):
            button_frame.configure(relief=tk.SUNKEN)
        
        def on_leave(event):
            button_frame.configure(relief=tk.RAISED)
        
        button_frame.bind("<Enter>", on_enter)
        button_frame.bind("<Leave>", on_leave)
        title_label.bind("<Enter>", on_enter)
        title_label.bind("<Leave>", on_leave)
        desc_label.bind("<Enter>", on_enter)
        desc_label.bind("<Leave>", on_leave)
    
    def open_bus_management(self):
        """Open bus management window"""
        try:
            from bus_management import BusManagementWindow
            BusManagementWindow(self.root)
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בפתיחת חלון ניהול אוטובוסים: {e}")
    
    def open_driver_management(self):
        """Open driver management window"""
        try:
            from driver_management import DriverManagementWindow
            DriverManagementWindow(self.root)
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בפתיחת חלון ניהול נהגים: {e}")
    
    def open_shift_management(self):
        """Open shift management window"""
        try:
            from shift_management import ShiftManagementWindow
            ShiftManagementWindow(self.root)
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בפתיחת חלון ניהול משמרות: {e}")
    
    def open_operation_management(self):
        """Open bus operation management window"""
        try:
            from bus_operation_management import BusOperationManagementWindow
            BusOperationManagementWindow(self.root)
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בפתיחת חלון ניהול פעולות: {e}")
    
    def open_query_procedures(self):
        """Open query and procedures window"""
        try:
            from query_procedure_window import QueryProcedureWindow
            QueryProcedureWindow()
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בפתיחת חלון שאילתות ופרוצדורות: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("יציאה", "האם אתה בטוח שברצונך לצאת מהמערכת?"):
            # Disconnect from database
            db_connection.disconnect()
            self.root.destroy()
            sys.exit()
    
    def run(self):
        """Start the main application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.run()
