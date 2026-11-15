import os
import sys
import mysql.connector
from mysql.connector import Error

def init_database(host="localhost", port=3306, user="root", password=""):
    print(f"Connecting to MySQL Server at {host}:{port} with user '{user}'...")
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            autocommit=True
        )
        cursor = conn.cursor()
        print("Connected! Initializing database schema...")

        # Read schema.sql
        with open('schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        # Split schema by statements (delimited by DELIMITER or standard ;)
        # We can execute commands safely
        # Note: DELIMITER $$ is MySQL client syntax; in python, execute block procedures directly
        print("Executing schema setup...")
        execute_sql_script(conn, schema_sql)
        print("Schema created successfully!")

        # Read sample_data.sql
        with open('sample_data.sql', 'r', encoding='utf-8') as f:
            sample_sql = f.read()

        print("Populating 20+ users, 25+ vehicles, areas, slots, and transactions...")
        execute_sql_script(conn, sample_sql)
        print("Sample data populated successfully!")

        cursor.close()
        conn.close()
        print("\n=== DATABASE INITIALIZATION COMPLETED SUCCESSFULLY! ===")
        return True
    except Error as e:
        print(f"\n[ERROR] MySQL Initialization failed: {e}")
        return False

def execute_sql_script(conn, full_script):
    cursor = conn.cursor()
    # Normalize script handling DELIMITER $$
    parts = full_script.split("DELIMITER $$")
    
    # First part standard SQL
    standard_sql = parts[0]
    for stmt in standard_sql.split(";"):
        stmt = stmt.strip()
        if stmt and not stmt.startswith("--") and not stmt.startswith("/*"):
            try:
                cursor.execute(stmt)
            except Exception as e:
                # ignore drop warnings
                if "Unknown database" not in str(e) and "DROP" not in stmt:
                    print(f"Warning on stmt: {stmt[:60]}... -> {e}")

    # Subsequent parts with procedures and triggers
    for part in parts[1:]:
        subparts = part.split("DELIMITER ;")
        proc_block = subparts[0]
        # Split individual routines by $$
        for routine in proc_block.split("$$"):
            routine = routine.strip()
            if routine and not routine.startswith("--"):
                try:
                    cursor.execute(routine)
                except Exception as e:
                    print(f"Warning on procedure/trigger: {routine[:60]}... -> {e}")
        
        # After DELIMITER ; if there is remaining standard SQL
        if len(subparts) > 1:
            remaining = subparts[1]
            for stmt in remaining.split(";"):
                stmt = stmt.strip()
                if stmt and not stmt.startswith("--"):
                    try:
                        cursor.execute(stmt)
                    except Exception as e:
                        print(f"Warning on remaining: {stmt[:60]}... -> {e}")
    cursor.close()

if __name__ == "__main__":
    pwd = sys.argv[1] if len(sys.argv) > 1 else os.getenv("DB_PASSWORD", "")
    usr = sys.argv[2] if len(sys.argv) > 2 else os.getenv("DB_USER", "root")
    init_database(user=usr, password=pwd)
