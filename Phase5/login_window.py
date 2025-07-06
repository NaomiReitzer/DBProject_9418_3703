import tkinter as tk
from tkinter import ttk, messagebox
from database_connection import db_connection

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("מערכת ניהול אוטובוסים - התחברות")
        self.root.geometry("500x400")
        self.root.configure(bg='#2c3e50')
        
        # Center the window
        self.center_window()
        
        # Create UI
        self.create_widgets()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"500x400+{x}+{y}")
    
    def create_widgets(self):
        """Create login interface widgets"""
        # Main title
        title_label = tk.Label(
            self.root, 
            text="מערכת ניהול אוטובוסים", 
            font=("Arial", 24, "bold"),
            bg='#2c3e50', 
            fg='white'
        )
        title_label.pack(pady=30)
        
        # Login frame
        login_frame = tk.Frame(self.root, bg='#34495e', padx=20, pady=20)
        login_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        # Database connection fields
        tk.Label(login_frame, text="שרת:", font=("Arial", 12), bg='#34495e', fg='white').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.host_entry = tk.Entry(login_frame, font=("Arial", 12), width=20)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(login_frame, text="פורט:", font=("Arial", 12), bg='#34495e', fg='white').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.port_entry = tk.Entry(login_frame, font=("Arial", 12), width=20)
        self.port_entry.insert(0, "5432")
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(login_frame, text="בסיס נתונים:", font=("Arial", 12), bg='#34495e', fg='white').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.database_entry = tk.Entry(login_frame, font=("Arial", 12), width=20)
        self.database_entry.insert(0, "mydatabase")
        self.database_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(login_frame, text="שם משתמש:", font=("Arial", 12), bg='#34495e', fg='white').grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.user_entry = tk.Entry(login_frame, font=("Arial", 12), width=20)
        self.user_entry.insert(0, "naomi")
        self.user_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(login_frame, text="סיסמה:", font=("Arial", 12), bg='#34495e', fg='white').grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), width=20, show="*")
        self.password_entry.insert(0, "naomi01")
        self.password_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Login button
        login_btn = tk.Button(
            login_frame, 
            text="התחבר", 
            font=("Arial", 14, "bold"),
            bg='#3498db', 
            fg='white',
            command=self.login,
            width=15,
            relief=tk.RAISED,
            bd=2
        )
        login_btn.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
        
        # Status label
        self.status_label = tk.Label(
            self.root, 
            text="", 
            font=("Arial", 10),
            bg='#2c3e50', 
            fg='#e74c3c'
        )
        self.status_label.pack(pady=10)
    
    def login(self):
        """Attempt to connect to database and open main application"""
        self.status_label.config(text="מתחבר...")
        self.root.update()
        
        # Get connection parameters
        host = self.host_entry.get().strip()
        port = self.port_entry.get().strip()
        database = self.database_entry.get().strip()
        user = self.user_entry.get().strip()
        password = self.password_entry.get()
        
        # Validate inputs
        if not all([host, port, database, user, password]):
            self.status_label.config(text="יש למלא את כל השדות")
            return
        
        # Attempt connection
        if db_connection.connect(host, port, database, user, password):
            self.status_label.config(text="התחברות בוצעה בהצלחה!", fg='#27ae60')
            self.root.update()
            
            # Close login window and open main application
            self.root.after(1000, self.open_main_app)
        else:
            self.status_label.config(text="שגיאה בהתחברות לבסיס הנתונים", fg='#e74c3c')
    
    def open_main_app(self):
        """Open main application window"""
        self.root.destroy()
        from main_application import MainApplication
        app = MainApplication()
        app.run()
    
    def run(self):
        """Start the login window"""
        self.root.mainloop()

if __name__ == "__main__":
    login = LoginWindow()
    login.run()
