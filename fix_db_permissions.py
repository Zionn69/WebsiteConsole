import os
import sys
import json
import shutil
from datetime import datetime

def check_and_fix_database():
    """Check and fix the user database permissions and integrity."""
    print("\n=== USER DATABASE REPAIR UTILITY ===\n")
    
    db_file = "users.json"
    backup_file = f"users_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Check if database file exists
    if not os.path.exists(db_file):
        print(f"Database file {db_file} does not exist. Creating a new one.")
        with open(db_file, 'w') as f:
            json.dump({}, f, indent=4)
        print(f"Created empty database file: {db_file}")
        return True
    
    # Check file permissions
    try:
        # Create a backup first
        shutil.copy2(db_file, backup_file)
        print(f"Created backup: {backup_file}")
        
        # Check if file is readable
        with open(db_file, 'r') as f:
            try:
                data = json.load(f)
                print(f"Database has {len(data)} user(s):")
                for username in data:
                    print(f"  - {username}")
            except json.JSONDecodeError:
                print("Database file is corrupted. Creating a new one.")
                with open(db_file, 'w') as f:
                    json.dump({}, f, indent=4)
                print(f"Created fresh database file: {db_file}")
                return True
        
        # Check if file is writable
        with open(db_file, 'a') as f:
            pass
        print("Database file is writable.")
        
        # Fix permissions
        try:
            os.chmod(db_file, 0o666)  # Make readable and writable by all users
            print("Set read/write permissions for all users.")
        except Exception as e:
            print(f"Could not change permissions: {e}")
        
        print("\nDatabase file is OK and accessible.")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nTry running this script with administrator privileges.")
        return False

if __name__ == "__main__":
    print(f"Using Python: {sys.executable}")
    if check_and_fix_database():
        print("\nDatabase repair completed successfully.")
        
        # Ask if user wants to try running the main application
        try:
            answer = input("\nDo you want to run the application now? (y/n): ")
            if answer.lower() in ('y', 'yes'):
                print("\nStarting application...")
                import subprocess
                subprocess.Popen([sys.executable, "menu_gui.py"])
        except:
            pass
    else:
        print("\nDatabase repair failed.") 