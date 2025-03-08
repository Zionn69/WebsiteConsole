import json
import os
import hashlib
import random
import string

class UserDatabase:
    def __init__(self, db_file="users.json"):
        """Initialize the user database with the specified file."""
        self.db_file = db_file
        self.users = {}
        self.load_database()
    
    def load_database(self):
        """Load the user database from the JSON file."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    self.users = json.load(f)
            except json.JSONDecodeError:
                # If the file is corrupted, start with an empty database
                self.users = {}
        else:
            # Create a new database file if it doesn't exist
            self.save_database()
    
    def save_database(self):
        """Save the user database to the JSON file."""
        with open(self.db_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def hash_password(self, password, salt=None):
        """Hash a password with a salt for secure storage."""
        if salt is None:
            # Generate a random salt if not provided
            salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        # Combine password and salt, then hash
        salted_password = (password + salt).encode('utf-8')
        hashed = hashlib.sha256(salted_password).hexdigest()
        
        return hashed, salt
    
    def register_user(self, username, password, email=""):
        """Register a new user with the given credentials."""
        # Check if username already exists
        if username in self.users:
            return False, "Username already exists"
        
        # Hash the password with a new salt
        hashed_password, salt = self.hash_password(password)
        
        # Store the user information
        self.users[username] = {
            "password": hashed_password,
            "salt": salt,
            "email": email,
            "created_at": import_time(),
            "role": "User"  # Default role for new users
        }
        
        # Save the updated database
        self.save_database()
        return True, "User registered successfully"
    
    def authenticate_user(self, username, password):
        """Authenticate a user with the given credentials."""
        # Check if username exists
        if username not in self.users:
            return False, "Invalid username or password"
        
        # Get the stored salt for this user
        salt = self.users[username]["salt"]
        
        # Hash the provided password with the stored salt
        hashed_password, _ = self.hash_password(password, salt)
        
        # Check if the hashed password matches the stored one
        if hashed_password == self.users[username]["password"]:
            return True, "Authentication successful"
        else:
            return False, "Invalid username or password"
    
    def update_password(self, username, old_password, new_password):
        """Update a user's password after verifying the old password."""
        # First authenticate with the old password
        auth_success, _ = self.authenticate_user(username, old_password)
        
        if not auth_success:
            return False, "Current password is incorrect"
        
        # Hash the new password
        hashed_password, salt = self.hash_password(new_password)
        
        # Update the stored password and salt
        self.users[username]["password"] = hashed_password
        self.users[username]["salt"] = salt
        
        # Save the updated database
        self.save_database()
        return True, "Password updated successfully"

    def change_username(self, old_username, new_username, password):
        """Change a user's username after verifying their password."""
        # Check if the new username already exists
        if new_username in self.users:
            return False, "Username already exists"
            
        # First authenticate with the current password
        auth_success, _ = self.authenticate_user(old_username, password)
        
        if not auth_success:
            return False, "Password is incorrect"
        
        # Get the user data
        user_data = self.users[old_username]
        
        # Add the user with the new username
        self.users[new_username] = user_data
        
        # Remove the old username
        del self.users[old_username]
        
        # Save the updated database
        self.save_database()
        return True, "Username updated successfully"
    
    def update_profile(self, username, profile_data):
        """Update a user's profile data."""
        # Check if username exists
        if username not in self.users:
            return False, "User does not exist"
        
        # Update profile data - only update provided fields
        for key, value in profile_data.items():
            if key not in ["password", "salt"]:  # Don't allow direct password updates
                self.users[username][key] = value
        
        # Save the updated database
        self.save_database()
        return True, "Profile updated successfully"
    
    def set_profile_picture(self, username, picture_path):
        """Set the path to a user's profile picture."""
        # Check if username exists
        if username not in self.users:
            return False, "User does not exist"
        
        # Update the profile picture path
        self.users[username]["profile_picture"] = picture_path
        
        # Save the updated database
        self.save_database()
        return True, "Profile picture updated successfully"

    def get_user_role(self, username):
        """Get the role of a user."""
        if username not in self.users:
            return None
        
        # Return the role if it exists, otherwise return "User" as default
        return self.users[username].get("role", "User")
        
    def set_user_role(self, username, role):
        """Set the role of a user."""
        if username not in self.users:
            return False, "User does not exist"
        
        # Valid roles
        valid_roles = ["Admin", "VIP", "User", "Guest"]
        
        if role not in valid_roles:
            return False, f"Invalid role. Valid roles are: {', '.join(valid_roles)}"
        
        # Update the role
        self.users[username]["role"] = role
        
        # Save the updated database
        self.save_database()
        return True, f"Role for {username} updated to {role}"

# Helper function to get current time
def import_time():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S") 