import os
import json
import sys
from hashlib import sha256
import random
import string
import tkinter as tk
from tkinter import messagebox
import subprocess

# Ensure we're using the correct Python
PYTHON_EXE = sys.executable
print(f"Using Python: {PYTHON_EXE}")

def create_salt():
    """Create a random salt for password hashing."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def hash_password(password, salt):
    """Hash a password with a salt."""
    salted_password = (password + salt).encode('utf-8')
    return sha256(salted_password).hexdigest()

def repair_account_system():
    """Completely repair the account system and create a test account."""
    print("\n=== ACCOUNT SYSTEM REPAIR UTILITY ===\n")
    
    # 1. Check if users.json exists and backup if it does
    if os.path.exists("users.json"):
        print("Found existing users.json - creating backup...")
        try:
            # Read existing data
            with open("users.json", "r") as f:
                existing_data = f.read()
            
            # Create backup
            with open("users.json.bak", "w") as f:
                f.write(existing_data)
            print("Backup created as users.json.bak")
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")
    
    # 2. Create a fresh users.json with a test account
    test_username = "test"
    test_password = "test"
    salt = create_salt()
    hashed_password = hash_password(test_password, salt)
    
    # Create test user data
    users_data = {
        test_username: {
            "password": hashed_password,
            "salt": salt,
            "email": "test@example.com",
            "created_at": "2024-03-07 00:00:00"
        }
    }
    
    # Save to file
    try:
        with open("users.json", "w") as f:
            json.dump(users_data, f, indent=4)
        print(f"Created fresh users.json with test account:")
        print(f"  Username: {test_username}")
        print(f"  Password: {test_password}")
    except Exception as e:
        print(f"ERROR: Could not create users.json: {e}")
        return False
    
    # 3. Verify the file was created properly
    try:
        with open("users.json", "r") as f:
            verify_data = json.load(f)
        
        if test_username in verify_data:
            print("✓ Verification successful - users.json is valid")
        else:
            print("✗ Verification failed - user not found in created file")
            return False
    except Exception as e:
        print(f"✗ Verification failed - could not read users.json: {e}")
        return False
    
    print("\n=== ACCOUNT SYSTEM REPAIR COMPLETE ===")
    print("\nYou can now log in with:")
    print(f"  Username: {test_username}")
    print(f"  Password: {test_password}")
    
    # Ask if user wants to run the menu_gui.py
    try:
        answer = input("\nDo you want to run the application now? (y/n): ")
        if answer.lower() in ('y', 'yes'):
            print("\nStarting application...")
            subprocess.Popen([PYTHON_EXE, "menu_gui.py"])
    except Exception as e:
        print(f"Could not start application: {e}")
    
    return True

if __name__ == "__main__":
    repair_account_system() 