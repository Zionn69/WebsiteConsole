from user_database import UserDatabase

def test_user_database():
    # Create a test database
    db = UserDatabase("test_users.json")
    
    # Test user registration
    username = "testuser"
    password = "testpassword"
    
    # Register a new user
    success, message = db.register_user(username, password)
    print(f"Registration: {success}, {message}")
    
    # Try to authenticate with correct credentials
    success, message = db.authenticate_user(username, password)
    print(f"Authentication (correct): {success}, {message}")
    
    # Try to authenticate with incorrect password
    success, message = db.authenticate_user(username, "wrongpassword")
    print(f"Authentication (wrong password): {success}, {message}")
    
    # Try to authenticate with non-existent user
    success, message = db.authenticate_user("nonexistentuser", "anypassword")
    print(f"Authentication (wrong username): {success}, {message}")
    
    # Print the database contents
    print("\nDatabase contents:")
    for user, data in db.users.items():
        print(f"User: {user}")
        print(f"  Password hash: {data['password']}")
        print(f"  Salt: {data['salt']}")
        print(f"  Created at: {data['created_at']}")
        print()

if __name__ == "__main__":
    test_user_database() 