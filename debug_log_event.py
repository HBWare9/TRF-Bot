#!/usr/bin/env python3
"""
Debug script for the !log_event command
This script helps identify common issues with the command
"""

import os
import psycopg2

def check_environment():
    """Check if required environment variables are set"""
    print("=== Environment Check ===")
    
    database_url = os.getenv("DATABASE_URL")
    bot_token = os.getenv("TOKEN")
    
    if not database_url:
        print("❌ DATABASE_URL environment variable is missing!")
        return False
    else:
        print("✅ DATABASE_URL is set")
    
    if not bot_token:
        print("❌ TOKEN environment variable is missing!")
        return False
    else:
        print("✅ TOKEN is set")
    
    return True

def check_database_connection():
    """Test database connection"""
    print("\n=== Database Connection Check ===")
    
    try:
        DATABASE_URL = os.getenv("DATABASE_URL")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Test the connection
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result[0] == 1:
            print("✅ Database connection successful")
            
            # Check if Users table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'users'
                );
            """)
            table_exists = cursor.fetchone()[0]
            
            if table_exists:
                print("✅ Users table exists")
            else:
                print("❌ Users table does not exist")
                return False
                
            conn.close()
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_role_configuration():
    """Check role configuration in bot.py"""
    print("\n=== Role Configuration Check ===")
    
    try:
        with open("/workspaces/TRF-Bot/bot.py", "r") as f:
            content = f.read()
        
        # Check if allowed_role_ids is defined
        if "allowed_role_ids" in content:
            print("✅ allowed_role_ids is defined")
        else:
            print("❌ allowed_role_ids is not defined")
            return False
            
        # Check if the permission function exists
        if "def user_has_any_allowed_role" in content:
            print("✅ user_has_any_allowed_role function exists")
        else:
            print("❌ user_has_any_allowed_role function is missing")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error reading bot.py: {e}")
        return False

def main():
    print("TRF-Bot !log_event Debug Script")
    print("================================")
    
    env_ok = check_environment()
    db_ok = check_database_connection()
    role_ok = check_role_configuration()
    
    print("\n=== Summary ===")
    if env_ok and db_ok and role_ok:
        print("✅ All checks passed! The bot should work correctly.")
        print("\nIf !log_event is still not working, check:")
        print("1. Your Discord user has one of the allowed roles")
        print("2. The bot has proper permissions in the Discord server")
        print("3. Check the console output when running the bot for error messages")
    else:
        print("❌ Some checks failed. Please fix the issues above.")

if __name__ == "__main__":
    main()
