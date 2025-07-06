import psycopg2
from psycopg2 import Error
import tkinter as tk
from tkinter import messagebox

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self, host="localhost", port="5432", database="mydatabase", user="naomi", password="naomi01"):
        """Establish connection to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
            return True
        except Error as e:
            messagebox.showerror("Connection Error", f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Execute SELECT query and return results"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            messagebox.showerror("Query Error", f"Error executing query: {e}")
            return None
    
    def execute_non_query(self, query, params=None):
        """Execute INSERT, UPDATE, DELETE queries"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            messagebox.showerror("Execute Error", f"Error executing operation: {e}")
            return False
    
    def call_procedure(self, procedure_name, params=None):
        """Call stored procedure"""
        try:
            if params:
                self.cursor.callproc(procedure_name, params)
            else:
                self.cursor.callproc(procedure_name)
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            messagebox.showerror("Procedure Error", f"Error calling procedure: {e}")
            return False
    
    def call_function(self, function_query):
        """Call stored function and return results"""
        try:
            self.cursor.execute(function_query)
            return self.cursor.fetchall()
        except Error as e:
            messagebox.showerror("Function Error", f"Error calling function: {e}")
            return None

# Global database connection instance
db_connection = DatabaseConnection()
