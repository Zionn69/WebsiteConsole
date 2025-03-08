from user_database import UserDatabase
import os

def fix_login_issue():
    print("Fixing login issue...")
    
    # Check if users.json exists and delete it for a fresh start
    if os.path.exists("users.json"):
        print("Removing existing users.json file...")
        os.remove("users.json")
    
    # Create a new user database
    db = UserDatabase()
    
    # Create a test user
    test_username = "test"
    test_password = "test"
    
    success, message = db.register_user(test_username, test_password)
    print(f"Creating test user: {success}, {message}")
    
    # Verify the user can log in
    success, message = db.authenticate_user(test_username, test_password)
    print(f"Verifying login: {success}, {message}")
    
    # Print the database contents
    print("\nDatabase contents:")
    for user, data in db.users.items():
        print(f"User: {user}")
        print(f"  Password hash: {data['password']}")
        print(f"  Salt: {data['salt']}")
        print(f"  Created at: {data['created_at']}")
        print()
    
    print("\nTest completed. You should now be able to log in with:")
    print(f"Username: {test_username}")
    print(f"Password: {test_password}")

if __name__ == "__main__":
    fix_login_issue() 