import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import webbrowser
import time
from math import sin, cos, pi
import turtle
import json
import os
import urllib.request
from io import BytesIO
import sys
import random
from threading import Thread, Lock
import hashlib
import string
import math  # Add this import for player token positioning
import subprocess
from PIL import Image, ImageDraw, ImageTk

# Check if PIL is available
PIL_AVAILABLE = True
try:
    from PIL import Image, ImageTk
except ImportError:
    PIL_AVAILABLE = False
    print("PIL not available. Some features will be disabled.")

# Add Ursina imports at the top of the file
# from ursina import Ursina, Button, Sky, FirstPersonController, Entity, color, scene, camera, raycast, destroy

print(f"Using Python: {sys.executable}")

# Import the user database class with error handling
try:
    from user_database import UserDatabase
    print("UserDatabase successfully imported")
except ImportError as e:
    print(f"Error importing UserDatabase: {e}")
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from user_database import UserDatabase
        print("UserDatabase imported using absolute path")
    except ImportError as e:
        print(f"Failed to import UserDatabase: {e}")
        messagebox.showerror("Import Error", "Could not import UserDatabase module. Please make sure user_database.py is in the same directory as menu_gui.py.")
        sys.exit(1)

# Add the lock for thread synchronization
lyrics_lock = Lock()

def save_credentials(username, password):
    credentials = {
        "username": username,
        "password": password
    }
    with open("credentials.json", "w") as f:
        json.dump(credentials, f)

def load_credentials():
    try:
        with open("credentials.json", "r") as f:
            return json.load(f)
    except:
        return None

# Add the lyrics animation functions
def animate_text(text, delay=0.1, text_widget=None):
    if text_widget:
        # GUI version - animate in a text widget
        for char in text:
            text_widget.insert(tk.END, char)
            text_widget.see(tk.END)
            text_widget.update()
            time.sleep(delay)
        text_widget.insert(tk.END, "\n")
    else:
        # Console version
        with lyrics_lock:
            for char in text:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)
            print()

def sing_lyric(lyric, delay, speed, text_widget=None):
    time.sleep(delay)
    animate_text(lyric, speed, text_widget)

def sing_song(text_widget=None):
    lyrics = [
        ("\nKarna kamu cantik", 0.09),
        ("Kan kuberi segalanya apa yang kupunya", 0.09),
        ("Dan hatimu baik", 0.10),
        ("Sempurnalah duniaku saat kau di sisiku\n", 0.10),
        ("Bukan karna make up di wajahmu", 0.09),
        ("Atau lipstik merah itu", 0.09),
        ("Lembut hati tutur kata", 0.08),
        ("Terciptalah cinta yang kupuja\n", 0.10),
    ]
    
    delays = [0.3, 3.4, 7.4, 10.5, 14.5, 18.0, 21.9, 24.4]
    
    threads = []
    for i in range(len(lyrics)):
        lyric, speed = lyrics[i]
        t = Thread(target=sing_lyric, args=(lyric, delays[i], speed, text_widget))
        threads.append(t)
        t.start()
    
    for thread in threads:
        thread.join()

class AnimatedBackground:
    def __init__(self, parent, width, height, colors):
        self.parent = parent
        self.width = width
        self.height = height
        self.colors = colors
        
        # Get the first color as the background color (darkest purple)
        bg_color = colors[0]
        
        # Create canvas that fills the entire parent window
        self.canvas = tk.Canvas(
            parent, 
            width=width, 
            height=height, 
            highlightthickness=0, 
            bg=bg_color  # Use theme color instead of black
        )
        # Use place with relwidth and relheight to ensure it fills the entire window
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create particles
        self.particles = []
        
        # Create 100 particles
        for _ in range(100):
            # Random position
            x = random.randint(0, width)
            y = random.randint(0, height)
            
            # Random size (small)
            size = random.randint(2, 4)
            
            # Random color from theme
            color = random.choice(colors)
            
            # Random speed (slow to medium)
            speed = random.uniform(1, 3)
            
            # Create the particle
            particle_id = self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=color, outline=color
            )
            
            # Store particle data
            self.particles.append({
                'id': particle_id,
                'x': x,
                'y': y,
                'size': size,
                'color': color,
                'speed': speed
            })
        
        # Start animation
        self.running = True
        self.after_id = None
        self.animate()
    
    def animate(self):
        if not self.running:
            return
            
        # Move each particle
        for particle in self.particles:
            # Move down
            particle['y'] += particle['speed']
            
            # If particle is off-screen, reset to top
            if particle['y'] > self.height + particle['size']:
                # Reset to random position at top
                particle['y'] = -particle['size']
                particle['x'] = random.randint(0, self.width)
                
                # Maybe change color
                if random.random() < 0.3:
                    particle['color'] = random.choice(self.colors)
                    self.canvas.itemconfig(particle['id'], fill=particle['color'], 
                                          outline=particle['color'])
            
            # Update particle position
            size = particle['size']
            self.canvas.coords(
                particle['id'],
                particle['x'] - size,
                particle['y'] - size,
                particle['x'] + size,
                particle['y'] + size
            )
        
        # Schedule next frame
        try:
            self.after_id = self.parent.after(30, self.animate)
        except:
            # If parent is destroyed, stop animation
            self.running = False
    
    def stop(self):
        """Stop the animation"""
        self.running = False
        if self.after_id:
            try:
                self.parent.after_cancel(self.after_id)
            except:
                pass  # Ignore errors if parent is already destroyed

class FlowerAnimation:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Flower Animation")
        self.window.geometry("800x600")
        
        # Create canvas for turtle
        self.canvas = tk.Canvas(self.window, width=800, height=600, bg="#000000")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create turtle screen
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor("#000000")
        
        # Create and configure turtle
        self.t = turtle.RawTurtle(self.screen)
        self.t.speed(0)
        self.t.hideturtle()
        
        # Bind window closing event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start animation
        self.animate()
    
    def animate(self):
        try:
            # Using hex color codes instead of color names
            palette = ["#FFFF00", "#FF0000", "#FFFF00", "#FF0000"]
            
            iterations = 120
            for step in range(iterations):
                if not self.window.winfo_exists():
                    break
                radius = 200 - step
                for shade in palette:
                    if not self.window.winfo_exists():
                        break
                    self.t.color(shade)
                    self.t.circle(radius, 100)
                    self.t.left(90)
                    self.t.circle(radius, 100)
                    self.t.right(60)
                    self.t.end_fill()
                    self.window.update()
        except:
            pass
    
    def on_closing(self):
        try:
            self.t.clear()
            self.t.hideturtle()
            self.screen.clear()
            self.window.destroy()
        except:
            self.window.destroy()

class RegisterWindow:
    def __init__(self, parent):
        """Initialize the registration window."""
        self.parent = parent
        self.root = tk.Toplevel(parent)
        self.root.title("Create Account")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Define theme colors
        self.bg_color = "#2B1B2C"  # Dark purple background
        self.accent_color = "#FF69B4"  # Pink accent
        self.text_color = "#FFFFFF"  # White text
        self.hover_color = "#FF1493"  # Deeper pink for hover
        self.entry_bg = "#3D2A3E"  # Slightly lighter purple for entry fields
        
        # Set window background
        self.root.configure(bg=self.bg_color)
        
        # Create animated background
        self.bg_colors = ["#2B1B2C", "#3D2A3E", "#FF69B4", "#FF1493"]
        self.background = AnimatedBackground(self.root, 400, 600, self.bg_colors)
        
        # Create a semi-transparent overlay
        self.overlay_frame = tk.Frame(self.root, bg=self.bg_color)
        self.overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create a stippled overlay for semi-transparency
        self.overlay_canvas = tk.Canvas(self.overlay_frame, highlightthickness=0, bg=self.bg_color)
        self.overlay_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay_canvas.create_rectangle(0, 0, 400, 600, fill=self.bg_color, stipple="gray50")
        
        # Create main frame
        self.main_frame = tk.Frame(self.overlay_frame, bg=self.bg_color, padx=20, pady=20)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', width=360, height=560)
        
        # Create title label
        self.title_label = tk.Label(
            self.main_frame,
            text="Create Account",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.title_label.pack(pady=(0, 20))
        
        # Create form frame
        self.form_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.form_frame.pack(fill=tk.X, pady=10)
        
        # Username field
        self.create_field_with_label("Username", "username_entry")
        
        # Email field
        self.create_field_with_label("Email (optional)", "email_entry")
        
        # Password field
        self.create_field_with_label("Password", "password_entry", show_password=True)
        
        # Confirm Password field
        self.create_field_with_label("Confirm Password", "confirm_entry", show_password=True)
        
        # Buttons frame
        self.buttons_frame = tk.Frame(self.form_frame, bg=self.bg_color)
        self.buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Register button
        self.register_button = tk.Button(
            self.buttons_frame,
            text="Create Account",
            font=("Arial", 12, "bold"),
            bg=self.accent_color,
            fg=self.text_color,
            width=15,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.register
        )
        self.register_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Add hover effect
        self.register_button.bind("<Enter>", lambda e: self.register_button.configure(bg=self.hover_color))
        self.register_button.bind("<Leave>", lambda e: self.register_button.configure(bg=self.accent_color))
        
        # Cancel button
        self.cancel_button = tk.Button(
            self.buttons_frame,
            text="Cancel",
            font=("Arial", 12),
            bg=self.entry_bg,
            fg=self.text_color,
            width=10,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.root.destroy
        )
        self.cancel_button.pack(side=tk.LEFT)
        
        # Add hover effect
        self.cancel_button.bind("<Enter>", lambda e: self.cancel_button.configure(bg="#4D3A4E"))
        self.cancel_button.bind("<Leave>", lambda e: self.cancel_button.configure(bg=self.entry_bg))
        
        # Initialize the user database
        self.user_db = UserDatabase()
        
        # Center the window relative to parent
        self.center_window()
        
        # Set this window as modal
        self.root.transient(parent)
        self.root.grab_set()
        
        # Bind Enter key to register function
        self.root.bind('<Return>', lambda event: self.register())
    
    def create_field_with_label(self, label_text, entry_name, show_password=False):
        """Create a labeled form field."""
        # Create a frame for this field
        field_frame = tk.Frame(self.form_frame, bg=self.bg_color)
        field_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create label
        label = tk.Label(
            field_frame,
            text=label_text,
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        label.pack(anchor='w')
        
        # Create entry
        entry = tk.Entry(
            field_frame,
            font=("Arial", 12),
            bg=self.entry_bg,
            fg=self.text_color,
            insertbackground=self.text_color,  # Cursor color
            width=30,
            relief="solid",
            highlightcolor=self.accent_color,
            highlightbackground=self.accent_color,
            highlightthickness=1
        )
        
        if show_password:
            entry.configure(show="•")
            
        entry.pack(fill=tk.X, pady=5)
        
        # Store the entry widget
        setattr(self, entry_name, entry)
    
    def center_window(self):
        """Center the window relative to the parent."""
        self.root.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def register(self):
        """Register a new user."""
        # Get form data
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        
        print(f"Attempting to register user: {username}")
        
        # Validate input
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Register the user
        try:
            # Create a fresh UserDatabase instance to ensure we're using the latest file
            self.user_db = UserDatabase()
            
            print(f"Current users in database: {list(self.user_db.users.keys())}")
            
            success, message = self.user_db.register_user(username, password, email)
            
            if success:
                print(f"User {username} registered successfully")
                print(f"Updated users in database: {list(self.user_db.users.keys())}")
                
                # Ensure the database is saved
                self.user_db.save_database()
                
                # Show success message and close registration window
                messagebox.showinfo("Success", "Account created successfully!\nYou can now log in with your new account.")
                self.root.destroy()
            else:
                print(f"Registration failed: {message}")
                messagebox.showerror("Registration Failed", message)
        except Exception as e:
            print(f"Error during registration: {str(e)}")
            messagebox.showerror("Registration Error", f"An error occurred: {str(e)}")

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("400x750")
        self.root.resizable(False, False)  # Disable resizing completely
        
        # Define theme colors
        self.bg_color = "#2B1B2C"  # Dark purple background
        self.accent_color = "#FF69B4"  # Pink accent
        self.text_color = "#FFFFFF"  # White text
        self.hover_color = "#FF1493"  # Deeper pink for hover
        self.entry_bg = "#3D2A3E"  # Slightly lighter purple for entry fields
        
        # Initialize login status and credentials
        self.success = False
        self.logged_in_username = ""
        
        # Center the window
        self.center_window()
        
        # Set window background to black for better animation visibility
        self.root.configure(bg="black")
        
        # Create animated background first (so it's at the bottom)
        self.bg_colors = ["#2B1B2C", "#3D2A3E", "#FF69B4", "#FF1493"]
        self.background = AnimatedBackground(self.root, 400, 750, self.bg_colors)
        
        # Create a semi-transparent overlay
        self.overlay_frame = tk.Frame(self.root, bg=self.bg_color)
        self.overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create a stippled overlay for semi-transparency
        self.overlay_canvas = tk.Canvas(self.overlay_frame, highlightthickness=0, bg=self.bg_color)
        self.overlay_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay_canvas.create_rectangle(0, 0, 400, 750, fill=self.bg_color, stipple="gray50")
        
        # Create content frame on top
        self.content_frame = tk.Frame(self.root)
        self.content_frame.place(relx=0.5, rely=0.5, anchor='center', width=360, height=700)
        self.content_frame.configure(bg=self.bg_color)
        
        # Create main frame
        self.main_frame = tk.Frame(self.content_frame, padx=20, pady=20, bg=self.bg_color)
        self.main_frame.pack(fill='both', expand=True)
        
        # Create top frame for image and logo
        self.top_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.top_frame.pack(fill='x', pady=(0, 20))
        
        # Load and display image in top frame
        self.load_image()
        
        # Create logo text with custom style in top frame
        self.logo_label = tk.Label(
            self.top_frame,
            text="Login Page",
            font=("Arial", 44, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.logo_label.pack(pady=(10, 0))
        
        # Create decorative line
        self.line = tk.Canvas(
            self.main_frame,
            height=2,
            bg=self.accent_color,
            highlightthickness=0
        )
        self.line.pack(fill='x', pady=(0, 20))
        
        # Create middle frame for login controls
        self.middle_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.middle_frame.pack(fill='x', pady=20)
        
        # Username with custom style
        self.username_frame = tk.Frame(self.middle_frame, bg=self.bg_color)
        self.username_frame.pack(pady=(0, 15), fill='x')
        
        self.username_label = tk.Label(
            self.username_frame,
            text="Username",
            font=("Arial", 12),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.username_label.pack(anchor='w')
        
        # Username Entry
        self.username_entry = tk.Entry(
            self.username_frame,
            width=30,
            font=("Arial", 12),
            bg=self.entry_bg,
            fg=self.text_color,
            insertbackground=self.text_color,  # Cursor color
            relief="solid",
            highlightcolor=self.accent_color,
            highlightbackground=self.accent_color,
            highlightthickness=1
        )
        self.username_entry.pack(fill='x', pady=5)
        
        # Password with custom style
        self.password_frame = tk.Frame(self.middle_frame, bg=self.bg_color)
        self.password_frame.pack(pady=(0, 15), fill='x')
        
        self.password_label = tk.Label(
            self.password_frame,
            text="Password",
            font=("Arial", 12),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.password_label.pack(anchor='w')
        
        # Password Entry
        self.password_entry = tk.Entry(
            self.password_frame,
            show="•",
            width=30,
            font=("Arial", 12),
            bg=self.entry_bg,
            fg=self.text_color,
            insertbackground=self.text_color,  # Cursor color
            relief="solid",
            highlightcolor=self.accent_color,
            highlightbackground=self.accent_color,
            highlightthickness=1
        )
        self.password_entry.pack(fill='x', pady=5)
        
        # Create bottom frame for remember me and login button
        self.bottom_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.bottom_frame.pack(fill='x', pady=(0, 20))
        
        # Remember Me checkbox with custom style
        self.remember_var = tk.BooleanVar()
        self.remember_checkbox = tk.Checkbutton(
            self.bottom_frame,
            text="Remember Me",
            variable=self.remember_var,
            bg=self.bg_color,
            fg=self.text_color,
            selectcolor=self.bg_color,
            activebackground=self.bg_color,
            activeforeground=self.text_color
        )
        self.remember_checkbox.pack(anchor='w', pady=(0, 15))
        
        # Button frame for login and register buttons
        self.button_frame = tk.Frame(self.bottom_frame, bg=self.bg_color)
        self.button_frame.pack(fill='x')
        
        # Login button with custom style
        self.login_button = tk.Button(
            self.button_frame,
            text="Login",
            command=self.login,
            font=("Arial", 12, "bold"),
            bg=self.accent_color,
            fg=self.text_color,
            width=15,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        self.login_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Add hover effect to login button
        self.login_button.bind("<Enter>", lambda e: self.login_button.configure(bg=self.hover_color))
        self.login_button.bind("<Leave>", lambda e: self.login_button.configure(bg=self.accent_color))
        
        # Register button
        self.register_button = tk.Button(
            self.button_frame,
            text="Create Account",
            command=self.open_register,
            font=("Arial", 12),
            bg=self.entry_bg,
            fg=self.text_color,
            width=15,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        self.register_button.pack(side=tk.LEFT)
        
        # Add hover effect to register button
        self.register_button.bind("<Enter>", lambda e: self.register_button.configure(bg="#4D3A4E"))
        self.register_button.bind("<Leave>", lambda e: self.register_button.configure(bg=self.entry_bg))
        
        # Add "Continue as Guest" button
        self.guest_button = tk.Button(
            self.main_frame,
            text="Continue as Guest",
            command=self.login_as_guest,
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.text_color,
            relief="flat",
            cursor="hand2",
            bd=1,
            highlightbackground=self.entry_bg,
            highlightthickness=1
        )
        self.guest_button.pack(pady=(0, 10))
        
        # Add hover effect to guest button
        self.guest_button.bind("<Enter>", lambda e: self.guest_button.configure(bg=self.entry_bg))
        self.guest_button.bind("<Leave>", lambda e: self.guest_button.configure(bg=self.bg_color))
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
        
        # Initialize the user database
        self.user_db = UserDatabase()
        
        # Load saved credentials if they exist
        self.load_saved_credentials()
    
    def open_register(self):
        """Open the registration window."""
        RegisterWindow(self.root)
    
    def load_image(self):
        if not PIL_AVAILABLE:
            self.create_placeholder_label("PIL not available")
            return
            
        try:
            # URL of the image
            image_url = "https://i.pinimg.com/736x/56/d3/bd/56d3bd4771320512c188a0814797e0cc.jpg"
            
            # Configure headers for the request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Create a request with headers
            req = urllib.request.Request(image_url, headers=headers)
            
            # Download and process the image
            with urllib.request.urlopen(req) as url:
                image_data = BytesIO(url.read())
                image = Image.open(image_data)
                
                # Resize image while maintaining aspect ratio
                image_width = 200
                aspect_ratio = image.height / image.width
                image_height = int(image_width * aspect_ratio)
                
                image = image.resize((image_width, image_height), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(image)
                
                # Create and display image label
                self.image_label = tk.Label(
                    self.top_frame,
                    image=self.photo,
                    bg=self.bg_color  # Changed to use theme color
                )
                self.image_label.pack(pady=(0, 10))
        except urllib.error.URLError as e:
            self.create_placeholder_label(f"Network error: Unable to download image")
        except Exception as e:
            self.create_placeholder_label(f"Error loading image: {str(e)}")
    
    def create_placeholder_label(self, message):
        self.image_label = tk.Label(
            self.top_frame,
            text=message,
            font=("Arial", 12),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.image_label.pack(pady=(0, 10))
    
    def load_saved_credentials(self):
        credentials = load_credentials()
        if credentials:
            self.username_entry.insert(0, credentials.get("username", ""))
            self.password_entry.insert(0, credentials.get("password", ""))
            self.remember_var.set(True)
    
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
        
        print(f"Attempting to log in user: {username}")
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Refresh the user database to ensure we have the latest data
        try:
            self.user_db = UserDatabase()
            print(f"Available users in database: {list(self.user_db.users.keys())}")
        except Exception as e:
            print(f"Error loading user database: {str(e)}")
        
        # For debugging, also try hardcoded credentials
        if username == "test" and password == "test":
            print("Using hardcoded test credentials")
            if self.remember_var.get():
                save_credentials(username, password)
            
            # Store the username for later use
            self.logged_in_username = username
            
            # Stop the animation before destroying the window
            if hasattr(self, 'background'):
                self.background.stop()
            
            self.success = True
            self.root.destroy()
            return
        
        # For backward compatibility with original credentials
        if username == "ZAMM" and password == "Nonya":
            print("Using original credentials")
            if self.remember_var.get():
                save_credentials(username, password)
            
            self.logged_in_username = username
            
            if hasattr(self, 'background'):
                self.background.stop()
            
            self.success = True
            self.root.destroy()
            return
        
        # Authenticate using the user database
        try:
            # Try with UserDatabase for registered accounts
            success, message = self.user_db.authenticate_user(username, password)
            
            if success:
                print(f"Login successful for user: {username}")
                if self.remember_var.get():
                    save_credentials(username, password)
                
                # Store the username for later use
                self.logged_in_username = username
                
                # Stop the animation before destroying the window
                if hasattr(self, 'background'):
                    self.background.stop()
                
                self.success = True
                self.root.destroy()
            else:
                print(f"Login failed: {message}")
                messagebox.showerror("Login Failed", message)
        except Exception as e:
            print(f"Login error: {str(e)}")
            messagebox.showerror("Login Error", f"An error occurred: {str(e)}")
    
    def login_as_guest(self):
        """Log in as a guest user with limited access."""
        print("Logging in as guest")
        
        # Store guest username
        self.logged_in_username = "Guest"
        
        # Stop the animation before destroying the window
        if hasattr(self, 'background'):
            self.background.stop()
        
        self.success = True
        self.root.destroy()
    
    def show(self):
        """Show the login window and return True if login was successful."""
        self.root.mainloop()
        return self.success

class LyricsAnimation:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Song Lyrics")
        self.window.geometry("600x400")
        self.window.resizable(False, False)
        
        # Set window background
        self.window.configure(bg="#2B1B2C")
        
        # Create a frame for the content
        self.frame = tk.Frame(self.window, bg="#2B1B2C", padx=20, pady=20)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a title label
        self.title_label = tk.Label(
            self.frame,
            text="♫ Karna Kamu Cantik - Lyla ♫",
            font=("Arial", 16, "bold"),
            fg="#FF69B4",
            bg="#2B1B2C"
        )
        self.title_label.pack(pady=(0, 20))
        
        # Create a text widget for displaying lyrics
        self.text_widget = tk.Text(
            self.frame,
            width=50,
            height=15,
            font=("Arial", 12),
            bg="#3D2A3E",
            fg="#FFFFFF",
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Create a close button
        self.close_button = tk.Button(
            self.frame,
            text="Close",
            command=self.on_closing,
            font=("Arial", 12, "bold"),
            bg="#FF69B4",
            fg="#FFFFFF",
            width=10,
            height=1,
            relief="flat",
            cursor="hand2"
        )
        self.close_button.pack(pady=(20, 0))
        
        # Add hover effect to close button
        self.close_button.bind("<Enter>", lambda e: self.close_button.configure(bg="#FF1493"))
        self.close_button.bind("<Leave>", lambda e: self.close_button.configure(bg="#FF69B4"))
        
        # Set protocol for window closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Flag to track if window is active
        self.is_active = True
        
        # Display a welcome message
        self.text_widget.insert(tk.END, "Playing song lyrics...\n\n")
        self.text_widget.see(tk.END)
        self.text_widget.update()
        
        # Start the animation
        self.scheduled_tasks = []
        self.start_animation()
    
    def start_animation(self):
        """Start the lyrics animation"""
        # Define the lyrics and their timing
        lyrics = [
            "Karna kamu cantik",
            "Kan kuberi segalanya apa yang kupunya",
            "Dan hatimu baik",
            "Sempurnalah duniaku saat kau di sisiku",
            "Bukan karna make up di wajahmu",
            "Atau lipstik merah itu",
            "Lembut hati tutur kata",
            "Terciptalah cinta yang kupuja"
        ]
        
        # Define the delays (in seconds) for when each lyric should appear
        delays = [0.3, 3.4, 7.4, 10.5, 14.5, 18.0, 21.9, 24.4]
        
        # Define the character display speed for each lyric
        speeds = [0.09, 0.09, 0.10, 0.10, 0.09, 0.09, 0.08, 0.10]
        
        # Schedule each lyric to appear at the right time
        for i in range(len(lyrics)):
            delay_ms = int(delays[i] * 1000)
            task_id = self.window.after(
                delay_ms, 
                lambda i=i: self.animate_lyric(lyrics[i], speeds[i])
            )
            self.scheduled_tasks.append(task_id)
    
    def animate_lyric(self, lyric, speed):
        """Animate a single lyric character by character"""
        if not self.is_active:
            return
            
        # Add a newline before the lyric
        self.text_widget.insert(tk.END, "\n")
        
        # Schedule each character to appear with the right timing
        for i in range(len(lyric)):
            char_delay_ms = int(speed * 1000 * (i + 1))
            task_id = self.window.after(
                char_delay_ms,
                lambda i=i: self.display_char(lyric[i])
            )
            self.scheduled_tasks.append(task_id)
        
        # Add a newline after the lyric (for some lyrics)
        if lyric in ["Sempurnalah duniaku saat kau di sisiku", "Terciptalah cinta yang kupuja"]:
            newline_delay = int(speed * 1000 * (len(lyric) + 1))
            task_id = self.window.after(
                newline_delay,
                lambda: self.text_widget.insert(tk.END, "\n")
            )
            self.scheduled_tasks.append(task_id)
    
    def display_char(self, char):
        """Display a single character"""
        if not self.is_active:
            return
            
        self.text_widget.insert(tk.END, char)
        self.text_widget.see(tk.END)
        self.text_widget.update()
    
    def on_closing(self):
        """Handle window closing"""
        self.is_active = False
        
        # Cancel all scheduled tasks
        for task_id in self.scheduled_tasks:
            self.window.after_cancel(task_id)
        
        self.window.destroy()

class FunMenu:
    def __init__(self, parent, username="Guest"):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Fun Menu")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        
        # Store username
        self.username = username
        
        # Define theme colors
        self.bg_color = "#2B1B2C"  # Dark purple background
        self.accent_color = "#FF69B4"  # Pink accent
        self.text_color = "#FFFFFF"  # White text
        self.hover_color = "#FF1493"  # Deeper pink for hover
        
        # Set window background
        self.window.configure(bg=self.bg_color)
        
        # Create animated background
        self.bg_colors = ["#2B1B2C", "#3D2A3E", "#FF69B4", "#FF1493"]
        self.background = AnimatedBackground(self.window, 600, 500, self.bg_colors)
        
        # Create a semi-transparent overlay
        self.overlay_frame = tk.Frame(self.window, bg=self.bg_color)
        self.overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Make overlay semi-transparent
        self.overlay_canvas = tk.Canvas(self.overlay_frame, highlightthickness=0, bg=self.bg_color)
        self.overlay_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay_canvas.create_rectangle(0, 0, 600, 500, fill=self.bg_color, stipple="gray50")
        
        # Create main frame
        self.main_frame = tk.Frame(self.window, bg=self.bg_color, padx=20, pady=20)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', width=560, height=460)
        
        # Create title label
        self.title_label = tk.Label(
            self.main_frame,
            text="Fun Menu",
            font=("Arial", 24, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.title_label.pack(pady=(0, 20))
        
        # Create welcome label
        self.welcome_label = tk.Label(
            self.main_frame,
            text=f"Welcome {username}!",
            font=("Arial", 16, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.welcome_label.pack(pady=(0, 30))
        
        # Create buttons frame
        self.buttons_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.buttons_frame.pack(pady=20)
        
        # Create buttons for fun options
        self.create_option_button("Flower Animation", self.show_flower_animation, 0, 0)
        self.create_option_button("Karna Kamu Cantik by Lyla", self.show_lyrics_animation, 0, 1)
        
        # Create owner social media label
        self.owner_label = tk.Label(
            self.main_frame,
            text="Owner Social Media",
            font=("Arial", 14, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.owner_label.pack(pady=(30, 10))
        
        # Create credit label
        self.credit_label = tk.Label(
            self.main_frame,
            text="@xamm9912 on TikTok",
            font=("Arial", 12),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.credit_label.pack()
        
        # Create close button
        self.close_button = tk.Button(
            self.main_frame,
            text="Close",
            command=self.on_closing,
            font=("Arial", 12, "bold"),
            bg=self.accent_color,
            fg=self.text_color,
            width=10,
            height=1,
            relief="flat",
            cursor="hand2"
        )
        self.close_button.pack(pady=(30, 0))
        
        # Add hover effect to close button
        self.close_button.bind("<Enter>", lambda e: self.close_button.configure(bg=self.hover_color))
        self.close_button.bind("<Leave>", lambda e: self.close_button.configure(bg=self.accent_color))
        
        # Set protocol for window closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Track animation windows
        self.animation_window = None
        self.lyrics_window = None
    
    def create_option_button(self, text, command, row, col):
        button = tk.Button(
            self.buttons_frame,
            text=text,
            command=command,
            font=("Arial", 12),
            bg=self.accent_color,
            fg=self.text_color,
            width=20,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        button.grid(row=row, column=col, padx=10, pady=10)
        
        # Add hover effect
        button.bind("<Enter>", lambda e: button.configure(bg=self.hover_color))
        button.bind("<Leave>", lambda e: button.configure(bg=self.accent_color))
    
    def show_flower_animation(self):
        # Check if animation window already exists
        if self.animation_window is None or not hasattr(self.animation_window, 'window') or not self.animation_window.window.winfo_exists():
            self.animation_window = FlowerAnimation(self.window)
        else:
            messagebox.showinfo("Animation", "Animation window is already open!")
    
    def show_lyrics_animation(self):
        # Check if lyrics window already exists
        if self.lyrics_window is None or not hasattr(self.lyrics_window, 'window') or not self.lyrics_window.window.winfo_exists():
            self.lyrics_window = LyricsAnimation(self.window)
        else:
            messagebox.showinfo("Lyrics", "Lyrics window is already open!")
    
    def on_closing(self):
        self.window.destroy()

class AccountSettings:
    def __init__(self, parent, username):
        self.parent = parent
        self.username = username
        self.root = tk.Toplevel(parent)
        self.root.title("Account Settings")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Colors
        self.bg_color = "#1a0033"
        self.text_color = "#ffffff"
        self.accent_color = "#ff66cc"
        
        self.root.configure(bg=self.bg_color)
        
        # User data (mockup for demonstration)
        self.user_data = {
            "test": {"password": "test123"},
            "zzz": {"password": "zzz123"},
            "Nonya": {"password": "nonya123"}
        }
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        self.title_label = tk.Label(
            self.main_frame,
            text="Account Settings",
            font=("Arial", 20, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.title_label.pack(pady=10)
        
        # Username change
        self.username_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.username_frame.pack(pady=10)
        
        tk.Label(
            self.username_frame,
            text="Change Username:",
            font=("Arial", 14),
            fg=self.text_color,
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=5)
        
        self.username_entry = tk.Entry(
            self.username_frame,
            font=("Arial", 12),
            bg=self.accent_color,
            fg=self.text_color
        )
        self.username_entry.pack(side=tk.LEFT, padx=5)
        
        # Password change
        self.password_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.password_frame.pack(pady=10)
        
        tk.Label(
            self.password_frame,
            text="Change Password:",
            font=("Arial", 14),
            fg=self.text_color,
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=5)
        
        self.password_entry = tk.Entry(
            self.password_frame,
            font=("Arial", 12),
            bg=self.accent_color,
            fg=self.text_color,
            show="*"
        )
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        # Profile picture change
        self.profile_pic_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.profile_pic_frame.pack(pady=10)
        
        tk.Label(
            self.profile_pic_frame,
            text="Profile Picture:",
            font=("Arial", 14),
            fg=self.text_color,
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=5)
        
        self.profile_pic_button = tk.Button(
            self.profile_pic_frame,
            text="Upload",
            font=("Arial", 12),
            bg=self.accent_color,
            fg=self.text_color,
            command=self.upload_profile_picture
        )
        self.profile_pic_button.pack(side=tk.LEFT, padx=5)
        
        # Role information
        self.role_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.role_frame.pack(pady=10)
        
        # Get user role from database
        try:
            from user_database import UserDatabase
            user_db = UserDatabase()
            user_role = user_db.get_user_role(username) or "User"
        except Exception as e:
            print(f"Error getting user role: {str(e)}")
            user_role = "User"
        
        tk.Label(
            self.role_frame,
            text="Account Role:",
            font=("Arial", 14),
            fg=self.text_color,
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=5)
        
        role_color = "#ff66cc"  # Default
        if user_role == "Admin":
            role_color = "#ff0000"  # Red for admin
        elif user_role == "VIP":
            role_color = "#ffd700"  # Gold for VIP
        
        self.role_label = tk.Label(
            self.role_frame,
            text=user_role,
            font=("Arial", 14, "bold"),
            fg=role_color,
            bg=self.bg_color
        )
        self.role_label.pack(side=tk.LEFT, padx=5)
        
        # Save button
        self.save_button = tk.Button(
            self.main_frame,
            text="Save Changes",
            font=("Arial", 14, "bold"),
            bg=self.accent_color,
            fg=self.text_color,
            command=self.save_changes
        )
        self.save_button.pack(pady=20)
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Set up window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def save_changes(self):
        """Save changes to user data"""
        new_username = self.username_entry.get()
        new_password = self.password_entry.get()
        
        if new_username:
            self.user_data[self.username]["username"] = new_username
        if new_password:
            self.user_data[self.username]["password"] = new_password
        
        messagebox.showinfo("Success", "Changes saved.")
    
    def upload_profile_picture(self):
        """Upload a new profile picture"""
        file_path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            self.user_data[self.username]["profile_picture"] = file_path
            messagebox.showinfo("Success", "Profile picture updated.")
    
    def on_closing(self):
        """Handle window close event"""
        self.root.destroy()

class GameMenu:
    def __init__(self, parent, username="Guest"):
        self.parent = parent
        self.root = tk.Toplevel(parent)
        self.root.title("Game Menu")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.username = username
        
        # Colors
        self.bg_color = "#1a0033"  # Dark purple background
        self.text_color = "#ffffff"  # White text
        self.accent_color = "#ff66cc"  # Pink accent
        self.section_bg = "#330066"  # Lighter purple for sections
        self.button_hover_bg = "#ff33cc"  # Bright pink for button hover
        
        self.root.configure(bg=self.bg_color)
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        self.title_label = tk.Label(
            self.main_frame,
            text="Game Menu",
            font=("Arial", 28, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.title_label.pack(pady=10)
        
        # Welcome message
        self.welcome_label = tk.Label(
            self.main_frame,
            text=f"Welcome {self.username}!",
            font=("Arial", 16),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.welcome_label.pack(pady=(5, 20))
        
        # Games section
        self.games_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        self.games_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.games_label = tk.Label(
            self.games_frame,
            text="Available Games",
            font=("Arial", 18, "bold"),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        self.games_label.pack(pady=(0, 20), anchor="w")
        
        # Games grid
        self.games_grid = tk.Frame(self.games_frame, bg="#2c3e50")
        self.games_grid.pack(expand=True, fill="both")
        
        # Create game options
        self.create_game_button("Snake Game", self.open_snake_game, 0, 0)
        self.create_game_button("Tic Tac Toe", self.open_tictactoe_game, 0, 1)
        self.create_game_button("Snakes & Ladders", self.open_snakes_ladders_game, 1, 0)
        self.create_game_button("Memory Game", self.open_memory_game, 1, 1)
        
        # Close button
        self.close_button = tk.Button(
            self.main_frame,
            text="Close",
            command=self.on_closing,
            font=("Arial", 14),
            bg="#e74c3c",
            fg="white",
            width=10
        )
        self.close_button.pack(pady=20)
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_game_button(self, text, command, row, col):
        button = tk.Button(
            self.games_grid,
            text=text,
            command=command,
            font=("Arial", 14),
            bg=self.accent_color,
            fg="#ecf0f1",
            width=15,
            height=3,
            relief="flat",
            cursor="hand2"
        )
        button.grid(row=row, column=col, padx=10, pady=10)
        
        # Add hover effect
        button.bind("<Enter>", lambda e: button.configure(bg=self.button_hover_bg))
        button.bind("<Leave>", lambda e: button.configure(bg=self.accent_color))
    
    def open_snake_game(self):
        messagebox.showinfo("Game", "Snake Game will be implemented soon!")
    
    def open_tictactoe_game(self):
        messagebox.showinfo("Game", "Tic Tac Toe will be implemented soon!")
    
    def open_snakes_ladders_game(self):
        messagebox.showinfo("Game", "Snakes & Ladders will be implemented soon!")
    
    def open_memory_game(self):
        messagebox.showinfo("Game", "Memory Game will be implemented soon!")
    
    def on_closing(self):
        self.root.destroy()

class RPGGame:
    def __init__(self, parent, player_name="Adventurer", game_type="fantasy"):
        """Initialize the RPG game."""
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title(f"VIP RPG Game - {game_type.capitalize()}")
        self.window.geometry("900x700")  # Increased window size
        self.window.minsize(900, 700)    # Set minimum window size
        self.window.configure(bg="#2c3e50")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center the window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Game variables
        self.player_name = player_name
        self.game_type = game_type
        
        # Set theme colors based on game type
        self.theme_colors = {
            "fantasy": {
                "bg": "#2c3e50",
                "accent": "#e74c3c",
                "text": "#ecf0f1",
                "title": "Fantasy RPG Adventure"
            },
            "scifi": {
                "bg": "#1a1a2e",
                "accent": "#9b59b6",
                "text": "#e0e0e0",
                "title": "Sci-Fi RPG Adventure"
            },
            "medieval": {
                "bg": "#2d4a22",
                "accent": "#2980b9",
                "text": "#f1c40f",
                "title": "Medieval RPG Adventure"
            },
            "zombie": {
                "bg": "#1e272e",
                "accent": "#27ae60",
                "text": "#d35400",
                "title": "Zombie Survival RPG"
            }
        }
        
        # Get theme colors for the selected game type
        theme = self.theme_colors.get(game_type, self.theme_colors["fantasy"])
        self.bg_color = theme["bg"]
        self.accent_color = theme["accent"]
        self.text_color = theme["text"]
        self.title_text = theme["title"]
        
        # Update window background
        self.window.configure(bg=self.bg_color)
        
        # Create a simple UI for now
        self.main_frame = tk.Frame(self.window, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = tk.Label(
            self.main_frame,
            text=self.title_text,
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.title_label.pack(pady=20)
        
        # Welcome message
        self.welcome_label = tk.Label(
            self.main_frame,
            text=f"Welcome, {player_name}!",
            font=("Helvetica", 18),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.welcome_label.pack(pady=10)
        
        # Game description based on type
        descriptions = {
            "fantasy": "Embark on an epic journey through mystical lands filled with magic, dragons, and ancient treasures. Your destiny awaits!",
            "scifi": "Explore distant galaxies, encounter alien civilizations, and uncover the secrets of advanced technology in this futuristic adventure.",
            "medieval": "Journey through a world of knights, castles, and kingdoms. Prove your valor in battle and rise to become a legendary hero.",
            "zombie": "Survive in a post-apocalyptic world overrun by the undead. Scavenge for resources, build defenses, and protect your fellow survivors."
        }
        
        description = descriptions.get(game_type, descriptions["fantasy"])
        
        self.description_label = tk.Label(
            self.main_frame,
            text=description,
            font=("Helvetica", 14),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=800,
            justify=tk.CENTER
        )
        self.description_label.pack(pady=20)
        
        # Coming soon message
        self.coming_soon_label = tk.Label(
            self.main_frame,
            text=f"This {game_type.capitalize()} RPG Adventure is coming soon!\nCheck back later for updates.",
            font=("Helvetica", 14),
            bg=self.bg_color,
            fg=self.accent_color,
            justify=tk.CENTER
        )
        self.coming_soon_label.pack(pady=50)
        
        # Close button
        self.close_button = tk.Button(
            self.main_frame,
            text="Close",
            command=self.on_closing,
            font=("Helvetica", 14),
            bg=self.accent_color,
            fg="white",
            width=10
        )
        self.close_button.pack(pady=20)
    
    def on_closing(self):
        """Handle window closing."""
        self.window.destroy()

class AdventureGame:
    def __init__(self, parent, player_name="Adventurer", game_type="treasure"):
        """Initialize the Adventure game."""
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title(f"VIP Adventure Game - {game_type.capitalize()}")
        self.window.geometry("900x700")  # Increased window size
        self.window.minsize(900, 700)    # Set minimum window size
        self.window.configure(bg="#2c3e50")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center the window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Game variables
        self.player_name = player_name
        self.game_type = game_type
        
        # Set theme colors based on game type
        self.theme_colors = {
            "treasure": {
                "bg": "#34495e",
                "accent": "#f39c12",
                "text": "#ecf0f1",
                "title": "Treasure Hunt Adventure"
            },
            "mystery": {
                "bg": "#2c3e50",
                "accent": "#16a085",
                "text": "#ecf0f1",
                "title": "Mystery Solver Adventure"
            }
        }
        
        # Get theme colors for the selected game type
        theme = self.theme_colors.get(game_type, self.theme_colors["treasure"])
        self.bg_color = theme["bg"]
        self.accent_color = theme["accent"]
        self.text_color = theme["text"]
        self.title_text = theme["title"]
        
        # Update window background
        self.window.configure(bg=self.bg_color)
        
        # Create a simple UI for now
        self.main_frame = tk.Frame(self.window, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = tk.Label(
            self.main_frame,
            text=self.title_text,
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.title_label.pack(pady=20)
        
        # Welcome message
        self.welcome_label = tk.Label(
            self.main_frame,
            text=f"Welcome, {player_name}!",
            font=("Helvetica", 18),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.welcome_label.pack(pady=10)
        
        # Game description based on type
        descriptions = {
            "treasure": "Embark on an exciting quest to find hidden treasures across the world. Solve puzzles, navigate treacherous terrain, and outsmart rival treasure hunters!",
            "mystery": "Put your detective skills to the test as you solve complex mysteries, uncover clues, and bring criminals to justice in this thrilling adventure."
        }
        
        description = descriptions.get(game_type, descriptions["treasure"])
        
        self.description_label = tk.Label(
            self.main_frame,
            text=description,
            font=("Helvetica", 14),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=800,
            justify=tk.CENTER
        )
        self.description_label.pack(pady=20)
        
        # Coming soon message
        self.coming_soon_label = tk.Label(
            self.main_frame,
            text=f"This {game_type.capitalize()} Adventure is coming soon!\nCheck back later for updates.",
            font=("Helvetica", 14),
            bg=self.bg_color,
            fg=self.accent_color,
            justify=tk.CENTER
        )
        self.coming_soon_label.pack(pady=50)
        
        # Close button
        self.close_button = tk.Button(
            self.main_frame,
            text="Close",
            command=self.on_closing,
            font=("Helvetica", 14),
            bg=self.accent_color,
            fg="white",
            width=10
        )
        self.close_button.pack(pady=20)
    
    def on_closing(self):
        """Handle window closing."""
        self.window.destroy()

class AIChatGame:
    def __init__(self, parent, user_name="User"):
        """Initialize the AI Chat Game."""
        self.parent = parent
        self.user_name = user_name
        
        # Create chat window
        self.window = tk.Toplevel(parent)
        self.window.title("AI Chat Assistant [BETA]")
        self.window.geometry("800x600")
        self.window.configure(bg="#2c3e50")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center the window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Chat history
        self.chat_history = []
        
        # AI Personality
        self.ai_name = "AURA"  # Advanced Universal Response Assistant
        self.ai_personality = "friendly, helpful, and a bit quirky"
        
        # Create UI
        self.create_ui()
        
        # Welcome message
        self.add_system_message("⚠️ This AI Chat Assistant is currently in BETA. Responses are generated using simple rules and may not always be relevant or accurate.")
        self.add_ai_message(f"Hello {self.user_name}! I'm {self.ai_name}, your AI assistant. I'm still learning and improving, but I'll do my best to chat with you! How can I help you today?")
    
    def create_ui(self):
        """Create the chat UI."""
        # Main frame
        self.main_frame = tk.Frame(self.window, bg="#2c3e50")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Development banner
        dev_frame = tk.Frame(self.main_frame, bg="#c0392b")
        dev_frame.pack(fill=tk.X, pady=(0, 10))
        
        dev_label = tk.Label(dev_frame, 
                           text="⚠️ UNDER DEVELOPMENT - This is a simplified AI chat assistant ⚠️", 
                           font=("Helvetica", 12, "bold"), 
                           bg="#c0392b", fg="white")
        dev_label.pack(pady=5)
        
        # Title frame
        title_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(title_frame, text=f"{self.ai_name} - AI Chat Assistant", 
                              font=("Helvetica", 24, "bold"), bg="#2c3e50", fg="#ecf0f1")
        title_label.pack(side=tk.LEFT, pady=(0, 10))
        
        # Chat area
        self.chat_frame = tk.Frame(self.main_frame, bg="#34495e", bd=2, relief=tk.RIDGE)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat display
        self.chat_display = tk.Text(self.chat_frame, height=20, width=70, bg="#2c3e50", fg="#ecf0f1",
                                  font=("Helvetica", 11), wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure tags
        self.chat_display.tag_configure("user", font=("Helvetica", 11, "bold"), foreground="#3498db")
        self.chat_display.tag_configure("user_message", font=("Helvetica", 11), foreground="#ecf0f1")
        self.chat_display.tag_configure("ai", font=("Helvetica", 11, "bold"), foreground="#e74c3c")
        self.chat_display.tag_configure("ai_message", font=("Helvetica", 11), foreground="#ecf0f1")
        self.chat_display.tag_configure("system", font=("Helvetica", 10, "italic"), foreground="#95a5a6")
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.chat_frame, command=self.chat_display.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        self.chat_display.config(yscrollcommand=scrollbar.set)
        
        # Input area
        self.input_frame = tk.Frame(self.main_frame, bg="#34495e", bd=2, relief=tk.RIDGE)
        self.input_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        # Message entry
        self.message_entry = tk.Text(self.input_frame, height=3, width=70, bg="#2c3e50", fg="#ecf0f1",
                                   font=("Helvetica", 11), wrap=tk.WORD)
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_on_enter)
        self.message_entry.focus_set()
        
        # Send button
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message,
                                   font=("Helvetica", 12), bg="#2ecc71", fg="white",
                                   width=10, height=1)
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Bottom controls
        self.control_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        self.control_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Clear chat button
        self.clear_button = tk.Button(self.control_frame, text="Clear Chat", command=self.clear_chat,
                                    font=("Helvetica", 11), bg="#e74c3c", fg="white")
        self.clear_button.pack(side=tk.LEFT, padx=10)
        
        # Save chat button
        self.save_button = tk.Button(self.control_frame, text="Save Chat", command=self.save_chat,
                                   font=("Helvetica", 11), bg="#3498db", fg="white")
        self.save_button.pack(side=tk.LEFT, padx=10)
        
        # Help button
        self.help_button = tk.Button(self.control_frame, text="Chat Tips", command=self.show_help,
                                   font=("Helvetica", 11), bg="#f39c12", fg="white")
        self.help_button.pack(side=tk.RIGHT, padx=10)
    
    def send_on_enter(self, event):
        """Send message when Enter key is pressed."""
        # Only send if Enter is pressed without Shift
        if event.state != 1:  # No Shift key
            self.send_message()
            return "break"  # Prevents default behavior (newline)
        return None  # Allow default behavior (newline) when Shift+Enter is pressed
    
    def send_message(self):
        """Send a message to the AI."""
        # Get user message
        user_message = self.message_entry.get("1.0", tk.END).strip()
        if not user_message:
            return
            
        # Clear input field
        self.message_entry.delete("1.0", tk.END)
        
        # Add user message to chat
        self.add_user_message(user_message)
        
        # Add to chat history
        self.chat_history.append({"role": "user", "content": user_message})
        
        # Generate AI response
        self.window.after(500, lambda: self.generate_and_display_response(user_message))
    
    def generate_and_display_response(self, user_message):
        """Generate and display AI response."""
        # Simple response generation
        response = self.generate_ai_response(user_message)
        
        # Add AI message to chat
        self.add_ai_message(response)
        
        # Add to chat history
        self.chat_history.append({"role": "assistant", "content": response})
    
    def generate_ai_response(self, user_message):
        """Generate an AI response based on user input."""
        user_message_lower = user_message.lower()
        
        # Greeting patterns
        if any(greeting in user_message_lower for greeting in ["hello", "hi", "hey", "greetings"]):
            greeting_responses = [
                f"Hello {self.user_name}! How can I help you today?",
                f"Hi there! It's nice to chat with you. How are you doing?",
                f"Hey {self.user_name}! What's on your mind today?",
                f"Greetings! How may I assist you?"
            ]
            response = random.choice(greeting_responses)
        
        # How are you patterns
        elif any(how_are_you in user_message_lower for how_are_you in ["how are you", "how you doing", "how's it going"]):
            mood_responses = [
                "I'm doing well, thank you for asking! How about you?",
                "I'm great! As an AI, I don't have feelings, but I appreciate you asking. How's your day going?",
                "I'm functioning perfectly! More importantly, how are you feeling today?",
                "All systems operational and ready to chat! How's your day been so far?"
            ]
            response = random.choice(mood_responses)
        
        # Who are you patterns
        elif any(who in user_message_lower for who in ["who are you", "what are you", "your name"]):
            identity_responses = [
                f"I'm {self.ai_name}, an AI chat assistant created to chat with you in this VIP game section. I'm still in development, but I'm doing my best to be helpful!",
                f"My name is {self.ai_name}, which stands for Advanced Universal Response Assistant. I'm a simple AI designed to chat with users like you!",
                f"I'm {self.ai_name}, a virtual assistant designed to have conversations. I'm pretty basic compared to advanced AIs, but I enjoy our chats!",
                f"I'm your AI companion, {self.ai_name}. I was created as part of this application to provide a fun chatting experience."
            ]
            response = random.choice(identity_responses)
        
        # Time patterns
        elif any(time in user_message_lower for time in ["time", "date", "day", "today"]):
            from datetime import datetime
            now = datetime.now()
            date_str = now.strftime("%A, %B %d, %Y")
            time_str = now.strftime("%I:%M %p")
            response = f"It's currently {time_str} on {date_str}."
        
        # Joke request
        elif any(joke in user_message_lower for joke in ["joke", "funny", "laugh", "humor"]):
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "I told my wife she was drawing her eyebrows too high. She looked surprised.",
                "What do you call a fake noodle? An impasta!",
                "How does a penguin build its house? Igloos it together!",
                "Why don't eggs tell jokes? They'd crack each other up!",
                "I'm reading a book on anti-gravity. It's impossible to put down!",
                "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
                "Why did the bicycle fall over? Because it was two-tired!",
                "What's orange and sounds like a parrot? A carrot!"
            ]
            response = f"Here's a joke for you: {random.choice(jokes)}"
        
        # Goodbye patterns
        elif any(bye in user_message_lower for bye in ["bye", "goodbye", "see you", "farewell"]):
            goodbye_responses = [
                f"Goodbye, {self.user_name}! Feel free to chat again anytime.",
                f"Farewell! It was nice chatting with you.",
                f"See you later! Have a great day!",
                f"Until next time, {self.user_name}! Take care."
            ]
            response = random.choice(goodbye_responses)
        
        # Thank you patterns
        elif any(thanks in user_message_lower for thanks in ["thank", "thanks", "appreciate"]):
            thanks_responses = [
                "You're welcome! I'm happy to help.",
                "No problem at all! Is there anything else you'd like to chat about?",
                "My pleasure! Feel free to ask if you need anything else.",
                "Glad I could be of assistance!"
            ]
            response = random.choice(thanks_responses)
        
        # Default response for anything else
        else:
            default_responses = [
                "That's interesting! Tell me more about that.",
                "I'm still learning, so I'm not sure how to respond to that. Could you try asking something else?",
                "I don't have a specific response for that yet. Is there something else you'd like to chat about?",
                f"I'm sorry, but I don't have enough information to provide a good response to that. I'm still in development!",
                "I'm not sure I understand. Could you rephrase that or ask something else?",
                "That's a good question! Unfortunately, I don't have a good answer for it yet."
            ]
            response = random.choice(default_responses)
        
        return response
    
    def add_user_message(self, message):
        """Add a user message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add a newline if there's already content
        if self.chat_display.get("1.0", tk.END).strip():
            self.chat_display.insert(tk.END, "\n\n")
        
        # Add user name with tag
        self.chat_display.insert(tk.END, f"{self.user_name}: ", "user")
        
        # Add message with tag
        self.chat_display.insert(tk.END, message, "user_message")
        
        # Scroll to the end
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def add_ai_message(self, message):
        """Add an AI message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add a newline if there's already content
        if self.chat_display.get("1.0", tk.END).strip():
            self.chat_display.insert(tk.END, "\n\n")
        
        # Add AI name with tag
        self.chat_display.insert(tk.END, f"{self.ai_name}: ", "ai")
        
        # Add message with tag
        self.chat_display.insert(tk.END, message, "ai_message")
        
        # Scroll to the end
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def add_system_message(self, message):
        """Add a system message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add a newline if there's already content
        if self.chat_display.get("1.0", tk.END).strip():
            self.chat_display.insert(tk.END, "\n\n")
        
        # Add message with system tag
        self.chat_display.insert(tk.END, message, "system")
        
        # Scroll to the end
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def clear_chat(self):
        """Clear the chat history."""
        if not self.chat_history:
            return
            
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat history?"):
            # Clear chat history
            self.chat_history = []
            
            # Clear chat display
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            
            # Add system message and welcome message
            self.add_system_message("⚠️ This AI Chat Assistant is currently in BETA. Responses are generated using simple rules and may not always be relevant or accurate.")
            self.add_ai_message(f"Chat cleared. How can I help you today, {self.user_name}?")
    
    def save_chat(self):
        """Save the chat history to a file."""
        if not self.chat_history:
            messagebox.showinfo("Save Chat", "There's no chat history to save.")
            return
            
        # Ask for file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Chat History"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"Chat with {self.ai_name} - {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for message in self.chat_history:
                    if message["role"] == "user":
                        file.write(f"{self.user_name}: {message['content']}\n")
                    else:
                        file.write(f"{self.ai_name}: {message['content']}\n")
                    file.write("\n")
                    
            messagebox.showinfo("Save Chat", f"Chat history saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save chat history: {str(e)}")
    
    def show_help(self):
        """Show chat tips and help information."""
        help_text = f"""
AI Chat Assistant - Tips & Information

ABOUT THIS CHAT ASSISTANT:
• This is a simple AI assistant named {self.ai_name}
• It uses basic pattern matching, not advanced AI
• Responses are pre-programmed and limited

TIPS FOR CHATTING:
• Keep messages short and clear
• Try topics like: greetings, jokes, games, time
• Use Shift+Enter for multi-line messages
• The AI has a friendly personality, but limited knowledge

COMMANDS YOU CAN TRY:
• "Hello" or "Hi" - Get a greeting
• "Tell me a joke" - Hear a random joke
• "What time is it?" - Check the current time
• "What can you do?" - Learn about capabilities
• "Goodbye" - End the conversation

This feature is under active development!
        """
        
        messagebox.showinfo("Chat Assistant Help", help_text)
    
    def on_closing(self):
        """Handle window closing."""
        self.window.destroy()

class MenuGUI:
    def __init__(self, root, username="Guest"):
        """Initialize the menu GUI."""
        self.window = root
        self.username = username
        self.window.title(f"ZAMM's Menu - Logged in as {username}")
        
        # Set up the font style
        self.default_font = ("Arial", 12)
        self.header_font = ("Arial", 16, "bold")
        
        # Define theme colors
        self.bg_color = "#2B1B2C"  # Dark purple background
        self.accent_color = "#FF69B4"  # Pink accent
        self.text_color = "#FFFFFF"  # White text
        self.hover_color = "#FF1493"  # Deeper pink for hover
        self.entry_bg = "#3D2A3E"  # Slightly lighter purple for entry fields
        self.disabled_bg = "#555555"  # Gray for disabled buttons
        
        # Initialize user database for profile info
        from user_database import UserDatabase
        self.user_db = UserDatabase()
        
        # Get user role
        if username != "Guest":
            self.user_role = self.user_db.get_user_role(username)
            
            # Set default roles for hardcoded users if they don't have a role
            if username == "ZAMM" and self.user_role == "User":
                self.user_db.set_user_role(username, "Admin")
                self.user_role = "Admin"
            elif username == "test" and self.user_role == "User":
                self.user_db.set_user_role(username, "VIP")
                self.user_role = "VIP"
            elif username == "Nonya" and self.user_role == "User":
                self.user_db.set_user_role(username, "VIP")
                self.user_role = "VIP"
        else:
            self.user_role = "Guest"
        
        # Track open windows
        self.flower_animation = None
        self.lyrics_animation = None
        self.fun_menu = None
        
        # Configure the window with a fixed size that fits all content
        self.window.geometry("800x700")  # Increased height to fit all content
        self.window.minsize(800, 700)    # Set minimum size to ensure all content is visible
        
        # Set window background
        self.window.configure(bg=self.bg_color)
        
        # Create animated background
        self.bg_colors = ["#2B1B2C", "#3D2A3E", "#FF69B4", "#FF1493"]
        self.background = AnimatedBackground(self.window, 800, 700, self.bg_colors)
        
        # Create a semi-transparent overlay
        self.overlay_frame = tk.Frame(self.window, bg=self.bg_color)
        self.overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Make overlay semi-transparent
        self.overlay_canvas = tk.Canvas(self.overlay_frame, highlightthickness=0, bg=self.bg_color)
        self.overlay_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        # Get window dimensions after it's created
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        self.overlay_canvas.create_rectangle(0, 0, width, height, fill=self.bg_color, stipple="gray50")
        
        # Create main frame
        self.main_frame = tk.Frame(self.overlay_frame, bg=self.bg_color, padx=20, pady=20)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9, relheight=0.9)
        
        # Create menu bar
        self.menu_bar = tk.Menu(self.window, bg=self.bg_color, fg=self.text_color, activebackground=self.accent_color, activeforeground=self.text_color)
        self.window.config(menu=self.menu_bar)
        
        # Create File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.bg_color, fg=self.text_color, activebackground=self.accent_color, activeforeground=self.text_color)
        self.file_menu.add_command(label="Exit", command=self.logout)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # Create Settings menu
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.bg_color, fg=self.text_color, activebackground=self.accent_color, activeforeground=self.text_color)
        self.settings_menu.add_command(label="Account Settings", command=self.open_account_settings)
        self.settings_menu.add_command(label="Logout", command=self.logout)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        
        # Create title label
        self.title_label = tk.Label(
            self.main_frame, 
            text="Main Menu", 
            font=("Arial", 36, "bold"), 
            bg=self.bg_color, 
            fg=self.accent_color
        )
        self.title_label.pack(pady=10)  # Reduced padding
        
        # Create a profile section
        self.profile_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.profile_frame.pack(pady=(0, 10))  # Reduced padding
        
        # Profile picture canvas (will be set up in load_profile_picture)
        self.profile_canvas = tk.Canvas(
            self.profile_frame, 
            width=80, 
            height=80, 
            bg=self.entry_bg,
            highlightthickness=1,
            highlightbackground=self.accent_color
        )
        self.profile_canvas.pack(side=tk.LEFT, padx=(0, 15))
        
        # Add default profile placeholder
        self.profile_canvas.create_text(
            40, 40,
            text=username[:1].upper(),
            fill=self.text_color,
            font=("Arial", 36, "bold")
        )
        
        # Welcome text frame
        self.welcome_frame = tk.Frame(self.profile_frame, bg=self.bg_color)
        self.welcome_frame.pack(side=tk.LEFT)
        
        # Create welcome message
        self.welcome_label = tk.Label(
            self.welcome_frame, 
            text=f"Welcome, {username}!", 
            font=("Arial", 18, "bold"), 
            bg=self.bg_color, 
            fg=self.accent_color
        )
        self.welcome_label.pack(anchor='w')
        
        # Add "Edit Profile" button
        self.edit_profile_button = tk.Button(
            self.welcome_frame,
            text="Edit Profile",
            font=("Arial", 10),
            bg=self.entry_bg,
            fg=self.text_color,
            relief="flat",
            cursor="hand2",
            command=self.open_account_settings
        )
        self.edit_profile_button.pack(anchor='w', pady=(5, 0))
        
        # Add hover effect
        self.edit_profile_button.bind("<Enter>", lambda e: self.edit_profile_button.configure(bg="#4D3A4E"))
        self.edit_profile_button.bind("<Leave>", lambda e: self.edit_profile_button.configure(bg=self.entry_bg))
        
        # Load the user's profile picture if it exists
        self.load_profile_picture()
        
        # Create decorative line
        self.line = tk.Canvas(
            self.main_frame,
            height=2,
            bg=self.accent_color,
            highlightthickness=0
        )
        self.line.pack(fill='x', pady=5)  # Reduced padding
        
        # Main Content Frame
        self.content_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.content_frame.pack(fill='both', expand=True)
        
        # Left side (buttons)
        self.left_side = tk.Frame(self.content_frame, bg=self.bg_color)
        self.left_side.pack(side=tk.LEFT, fill='both', expand=True)
        
        # Right side (social media)
        self.right_side = tk.Frame(self.content_frame, bg=self.bg_color)
        self.right_side.pack(side=tk.RIGHT, fill='both', expand=True)
        
        # Create section label for options
        self.options_label = tk.Label(
            self.left_side,
            text="Main Options",
            font=("Arial", 16, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.options_label.pack(pady=(0, 10))
        
        # Options Frame
        self.options_frame = tk.Frame(self.left_side, bg=self.bg_color)
        self.options_frame.pack(padx=10)
        
        # Create buttons with custom style - 2x4 grid layout
        self.create_option_button("My Website", self.open_website, 0, 0)
        self.create_option_button("My Steam", self.open_steam, 0, 1)
        self.create_option_button("My TikTok", self.open_tiktok, 1, 0)
        self.create_option_button("My YouTube", self.open_youtube, 1, 1)
        self.create_option_button("My Discord", self.open_discord, 2, 0)
        self.create_option_button("My GitHub", self.open_github, 2, 1)
        
        # Game Menu button - accessible to all users
        self.create_option_button("Game Menu", self.open_game_menu, 3, 0)
        
        # Fun Menu button - disabled for guest users
        if username.lower() == "guest":
            self.create_disabled_button("Fun Menu", 3, 1)
            # Add tooltip explaining why it's disabled
            self.create_tooltip(self.options_frame.winfo_children()[-1], "Login required to access Fun Menu")
        else:
            self.create_option_button("Fun Menu", self.open_fun_menu, 3, 1)
        
        # VIP Game button - only for VIP and Admin users
        if hasattr(self, 'user_role') and self.user_role in ["VIP", "Admin"]:
            self.create_option_button("VIP Game", self.open_vip_game, 4, 0)
        else:
            self.create_disabled_button("VIP Game", 4, 0)
            # Add tooltip explaining why it's disabled
            self.create_tooltip(self.options_frame.winfo_children()[-1], "VIP access required")
        
        self.create_option_button("Account", self.open_account_settings, 4, 1)
        
        # Owner social media section
        self.owner_label = tk.Label(
            self.right_side,
            text="Owner Social Media",
            font=("Arial", 16, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.owner_label.pack(pady=(0, 10))
        
        # TikTok info
        self.tiktok_frame = tk.Frame(self.right_side, bg=self.bg_color)
        self.tiktok_frame.pack(fill='x', pady=2)
        
        self.tiktok_label = tk.Label(
            self.tiktok_frame,
            text="TikTok:",
            font=("Arial", 12, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.tiktok_label.pack(side=tk.LEFT)
        
        self.tiktok_value = tk.Label(
            self.tiktok_frame,
            text="@xamm9912",
            font=("Arial", 12),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.tiktok_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # GitHub info
        self.github_frame = tk.Frame(self.right_side, bg=self.bg_color)
        self.github_frame.pack(fill='x', pady=2)
        
        self.github_label = tk.Label(
            self.github_frame,
            text="GitHub:",
            font=("Arial", 12, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.github_label.pack(side=tk.LEFT)
        
        self.github_value = tk.Label(
            self.github_frame,
            text="Zionn69",
            font=("Arial", 12),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.github_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Copyright info
        self.copyright_label = tk.Label(
            self.right_side,
            text="© 2024 ZAMM\nAll rights reserved.",
            font=("Arial", 10),
            fg=self.text_color,
            bg=self.bg_color,
            justify=tk.LEFT
        )
        self.copyright_label.pack(pady=(20, 0), anchor="w")
        
        # Status bar
        self.status_bar = tk.Label(
            self.window,
            text="Ready",
            anchor=tk.W,
            relief=tk.SUNKEN,
            bg=self.entry_bg,
            fg=self.text_color
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Show welcome message after a short delay
        self.window.after(500, self.show_welcome_message)

    def show_welcome_message(self):
        """Show a welcome message popup."""
        # Create a popup window
        popup = tk.Toplevel(self.window)
        popup.title("Welcome")
        popup.geometry("400x300")
        popup.resizable(False, False)
        popup.configure(bg=self.bg_color)
        
        # Make popup a transient window (always on top of main window)
        popup.transient(self.window)
        
        # Center the popup on the main window
        popup.update_idletasks()
        main_x = self.window.winfo_rootx()
        main_y = self.window.winfo_rooty()
        main_width = self.window.winfo_width()
        main_height = self.window.winfo_height()
        
        width = popup.winfo_width()
        height = popup.winfo_height()
        
        x = main_x + (main_width // 2) - (width // 2)
        y = main_y + (main_height // 2) - (height // 2)
        
        popup.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create a frame
        frame = tk.Frame(popup, bg=self.bg_color, padx=30, pady=30)
        frame.pack(fill='both', expand=True)
        
        # Welcome message - different for guest users
        if self.username.lower() == "guest":
            welcome_text = "Welcome, Guest User!"
            info_text = "Some features are limited in guest mode.\nLog in to access all features."
        else:
            welcome_text = f"Welcome back, {self.username}!"
            info_text = f"Account Role: {self.user_role}"
            
        welcome_label = tk.Label(
            frame,
            text=welcome_text,
            font=("Arial", 18, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        welcome_label.pack(pady=(20, 15))
        
        # Add info text for all users
        info_label = tk.Label(
            frame,
            text=info_text,
            font=("Arial", 12),
            fg=self.text_color,
            bg=self.bg_color
        )
        info_label.pack(pady=(0, 15))
        
        # Current time message
        from datetime import datetime
        time_now = datetime.now().strftime("%A, %B %d, %Y - %I:%M %p")
        time_label = tk.Label(
            frame,
            text=f"Logged in on: {time_now}",
            font=("Arial", 12),
            fg=self.text_color,
            bg=self.bg_color
        )
        time_label.pack(pady=(0, 30))
        
        # Close button
        close_button = tk.Button(
            frame,
            text="Let's Go!",
            font=("Arial", 12, "bold"),
            bg=self.accent_color,
            fg=self.text_color,
            relief="flat",
            cursor="hand2",
            command=popup.destroy
        )
        close_button.pack(pady=20)
        
        # Add hover effect
        close_button.bind("<Enter>", lambda e: close_button.configure(bg=self.hover_color))
        close_button.bind("<Leave>", lambda e: close_button.configure(bg=self.accent_color))
        
        # Auto close after 5 seconds
        popup.after(5000, popup.destroy)

    def show_about(self):
        """Show information about the application."""
        messagebox.showinfo(
            "About ZAMM's Menu",
            f"ZAMM's Menu Application\n\n"
            f"Logged in as: {self.username}\n"
            f"Account Role: {self.user_role}\n\n"
            f"Social Media:\n"
            f"• GitHub: Zionn69\n"
            f"• TikTok: @xamm9912\n"
            f"• YouTube: @zionvex\n\n"
            f"© 2024 ZAMM. All rights reserved."
        )

    def load_profile_picture(self):
        """Load and display the user's profile picture if it exists."""
        try:
            # Check if user has a profile picture
            if self.username in self.user_db.users and "profile_picture" in self.user_db.users[self.username]:
                profile_pic_path = self.user_db.users[self.username]["profile_picture"]
                
                if os.path.exists(profile_pic_path):
                    # Load and resize the image
                    image = Image.open(profile_pic_path)
                    image = image.resize((80, 80), Image.LANCZOS)
                    self.profile_photo = ImageTk.PhotoImage(image)
                    
                    # Clear canvas and display image
                    self.profile_canvas.delete("all")
                    self.profile_canvas.create_image(40, 40, image=self.profile_photo)
        except Exception as e:
            print(f"Error loading profile picture: {str(e)}")
    
    def create_option_button(self, text, command, row, col):
        button = tk.Button(
            self.options_frame,
            text=text,
            command=command,
            font=("Arial", 12),
            bg=self.accent_color,
            fg=self.text_color,
            width=13,  # Reduced width
            height=2,
            relief="flat",
            cursor="hand2"
        )
        button.grid(row=row, column=col, padx=5, pady=5)  # Reduced padding
        
        # Add hover effect
        button.bind("<Enter>", lambda e: button.configure(bg=self.hover_color))
        button.bind("<Leave>", lambda e: button.configure(bg=self.accent_color))
    
    def create_disabled_button(self, text, row, col):
        """Create a disabled button."""
        button = tk.Button(
            self.options_frame,
            text=text,
            font=("Arial", 12),
            bg=self.disabled_bg,
            fg=self.text_color,
            width=13,
            height=2,
            relief="flat",
            state=tk.DISABLED
        )
        button.grid(row=row, column=col, padx=5, pady=5)
        return button
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget."""
        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            # Create a toplevel window
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            # Create tooltip label
            label = tk.Label(
                self.tooltip, 
                text=text, 
                bg=self.entry_bg, 
                fg=self.text_color,
                padx=5, 
                pady=2,
                font=("Arial", 10)
            )
            label.pack(ipadx=1)
        
        def leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
        
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    
    def open_fun_menu(self):
        # Check if fun menu window already exists
        if self.fun_menu is None or not hasattr(self.fun_menu, 'window') or not self.fun_menu.window.winfo_exists():
            self.status_bar.config(text="Opening Fun Menu...")
            self.fun_menu = FunMenu(self.window, self.username)
        else:
            messagebox.showinfo("Fun Menu", "Fun Menu is already open!")
    
    def open_website(self):
        self.status_bar.config(text="Opening website...")
        webbrowser.open("https://www.google.com")  # Replace with your website URL
    
    def open_steam(self):
        self.status_bar.config(text="Opening Steam...")
        webbrowser.open("https://steamcommunity.com/id/zammsigma/")
    
    def open_tiktok(self):
        self.status_bar.config(text="Opening TikTok...")
        webbrowser.open("https://www.tiktok.com/@xamm9912")
    
    def open_youtube(self):
        self.status_bar.config(text="Opening YouTube...")
        webbrowser.open("https://www.youtube.com/@zionvex")
    
    def open_discord(self):
        self.status_bar.config(text="Opening Discord...")
        webbrowser.open("https://discordapp.com/users/1007974656030035969")
    
    def open_github(self):
        self.status_bar.config(text="Opening GitHub...")
        webbrowser.open("https://github.com/Zionn69")
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # Stop the animation before destroying the window
            if hasattr(self, 'background'):
                self.background.stop()
                
            self.window.destroy()
            main()
    
    def open_account_settings(self):
        """Open the account settings window."""
        self.status_bar.config(text="Opening Account Settings...")
        AccountSettings(self.window, self.username)
    
    def open_game_menu(self):
        """Open the game menu."""
        self.status_bar.config(text="Opening Game Menu...")
        GameMenu(self.window, self.username)
    
    def open_vip_game(self):
        """Open the VIP games menu."""
        if not hasattr(self, 'vip_window'):
            self.vip_window = tk.Toplevel(self.window)
            self.vip_window.title("VIP Games")
            self.vip_window.geometry("700x500")
            self.vip_window.configure(bg="#2d4a22")
            
            # Center the window
            self.vip_window.update_idletasks()
            width = self.vip_window.winfo_width()
            height = self.vip_window.winfo_height()
            x = (self.vip_window.winfo_screenwidth() // 2) - (width // 2)
            y = (self.vip_window.winfo_screenheight() // 2) - (height // 2)
            self.vip_window.geometry(f"{width}x{height}+{x}+{y}")
            
            # Create notebook for tabs
            notebook = ttk.Notebook(self.vip_window)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Games tab
            games_frame = tk.Frame(notebook, bg="#2d4a22")
            notebook.add(games_frame, text="Games")
            
            # Chat tab
            chat_frame = tk.Frame(notebook, bg="#2d4a22")
            notebook.add(chat_frame, text="Chat & Social")
            
            # Add Fantasy RPG button
            rpg_btn = tk.Button(
                games_frame,
                text="Fantasy RPG",
                command=lambda: self.open_rpg_game(self.vip_window, "fantasy"),
                font=("Luminari", 14),
                bg="#4a6a42",
                fg="#f1c40f",
                width=20
            )
            rpg_btn.pack(pady=10)
            
            # Add AI Chat button
            chat_btn = tk.Button(
                chat_frame,
                text="AI Chat Assistant",
                command=lambda: self.open_ai_chat(self.vip_window),
                font=("Luminari", 14),
                bg="#4a6a42",
                fg="#f1c40f",
                width=20
            )
            chat_btn.pack(pady=10)
            
            # Add VIP role check
            if not hasattr(self, 'user_role') or self.user_role not in ["VIP", "Admin"]:
                messagebox.showinfo("VIP Access Required", 
                                  "You need VIP or Admin role to access this feature.\n\n"
                                  "Please contact the administrator to upgrade your account.")
                self.vip_window.destroy()
                return
        else:
            self.vip_window.lift()
            self.vip_window.focus_force()
    
    def open_rpg_game(self, parent, game_type):
        """Open the RPG game."""
        from medieval_rpg import MedievalRPG
        MedievalRPG(parent, self.username)
    
    def open_ai_chat(self, parent):
        """Open the AI Chat Assistant."""
        AIChatGame(parent, self.username)

def main():
    """Main function to run the application."""
    try:
        # Create login window
        login = LoginWindow()
        
        # Show login window and wait for result
        login_result = login.show()
        
        if login_result:
            # Get the username that was used to log in
            username = login.logged_in_username
            
            if not username:  # Fallback if username wasn't stored
                username = "Guest"
            
            print(f"Login successful, launching main menu for user: {username}")
            
            # Create main menu window
            root = tk.Tk()
            app = MenuGUI(root, username=username)
            root.mainloop()
        else:
            print("Login was not successful - application closed")
    except Exception as e:
        print(f"Error in main function: {str(e)}")
        messagebox.showerror("Application Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()