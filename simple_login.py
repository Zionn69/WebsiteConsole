import tkinter as tk
from tkinter import messagebox
import sys

class SimpleLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Set up the frame
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill="both")
        
        # Username label and entry
        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.pack(anchor="w", pady=(0, 5))
        
        self.username_entry = tk.Entry(self.frame, width=40)
        self.username_entry.pack(pady=(0, 15))
        self.username_entry.insert(0, "test")  # Pre-fill with test
        
        # Password label and entry
        self.password_label = tk.Label(self.frame, text="Password:")
        self.password_label.pack(anchor="w", pady=(0, 5))
        
        self.password_entry = tk.Entry(self.frame, width=40, show="•")
        self.password_entry.pack(pady=(0, 20))
        self.password_entry.insert(0, "test")  # Pre-fill with test
        
        # Login button
        self.login_button = tk.Button(self.frame, text="Login", command=self.login)
        self.login_button.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(self.frame, text="Enter credentials and click Login")
        self.status_label.pack(pady=10)
        
        # Center window
        self.center_window()
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Hardcoded test account
        if username == "test" and password == "test":
            self.status_label.config(text="Login successful!", fg="green")
            messagebox.showinfo("Success", f"Welcome, {username}!")
            
            # Open a main menu window
            self.open_main_menu(username)
        else:
            self.status_label.config(text="Login failed. Try again.", fg="red")
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def open_main_menu(self, username):
        # Create a simple main menu window
        menu_window = tk.Toplevel(self.root)
        menu_window.title(f"Main Menu - {username}")
        menu_window.geometry("600x400")
        
        # Add content to the main menu
        main_frame = tk.Frame(menu_window, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")
        
        welcome_label = tk.Label(
            main_frame, 
            text=f"Welcome, {username}!", 
            font=("Arial", 24)
        )
        welcome_label.pack(pady=20)
        
        message_label = tk.Label(
            main_frame,
            text="This is a simple demonstration of the main menu.",
            font=("Arial", 12)
        )
        message_label.pack(pady=10)
        
        close_button = tk.Button(
            main_frame,
            text="Close",
            command=menu_window.destroy
        )
        close_button.pack(pady=20)
        
        # Center the window
        menu_window.update_idletasks()
        width = menu_window.winfo_width()
        height = menu_window.winfo_height()
        x = (menu_window.winfo_screenwidth() // 2) - (width // 2)
        y = (menu_window.winfo_screenheight() // 2) - (height // 2)
        menu_window.geometry(f'{width}x{height}+{x}+{y}')

def main():
    root = tk.Tk()
    app = SimpleLoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    print(f"Using Python: {sys.executable}")
    main() 