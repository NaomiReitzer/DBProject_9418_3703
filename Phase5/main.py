#!/usr/bin/env python3
"""
Bus Management System - Main Entry Point

This is the main application launcher for the bus management system.
Run this file to start the application.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from login_window import LoginWindow
    
    def main():
        """Main function to start the application"""
        print("Starting Bus Management System...")
        
        # Start with login window
        login = LoginWindow()
        login.run()
    
    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all required packages are installed:")
    print("pip install psycopg2-binary tkinter")
    sys.exit(1)
except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1)
