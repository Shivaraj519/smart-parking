import os
import re
import datetime
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash

DB_TYPE = os.getenv('DB_TYPE', 'MYSQL') # MYSQL by default

# MySQL Config
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'smart_parking_db')

_mysql_pool = None

def get_mysql_pool():
    global _mysql_pool
    if _mysql_pool is None:
        import mysql.connector
        from mysql.connector import pooling
        _mysql_pool = pooling.MySQLConnectionPool(
            pool_name="parking_pool",
            pool_size=5,
            pool_reset_session=True,
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            autocommit=False
        )
    return _mysql_pool

def get_db_connection():
    if DB_TYPE == 'MYSQL':
        try:
            pool = get_mysql_pool()
            return pool.get_connection()
        except Exception:
            import mysql.connector
            return mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                autocommit=False
            )
    else:
        import sqlite3
        conn = sqlite3.connect('smart_parking.db')
        conn.row_factory = sqlite3.Row
        return conn

def execute_query(query, params=None, fetch_one=False, fetch_all=True, commit=False):
    """
    Executes a SQL query safely and returns dict or list of dicts.
    """
    conn = get_db_connection()
    if DB_TYPE == 'MYSQL':
        cursor = conn.cursor(dictionary=True)
    else:
        cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        if commit:
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        if fetch_one:
            row = cursor.fetchone()
            if row and DB_TYPE != 'MYSQL':
                return dict(row)
            return row
        if fetch_all:
            rows = cursor.fetchall()
            if rows and DB_TYPE != 'MYSQL':
                return [dict(r) for r in rows]
            return rows
        return None
    except Exception as e:
        if commit:
            conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def execute_transaction(callbacks):
    """
    Executes multiple query callbacks within an ACID transaction.
    """
    conn = get_db_connection()
    if DB_TYPE == 'MYSQL':
        cursor = conn.cursor(dictionary=True)
    else:
        cursor = conn.cursor()
    try:
        result = None
        for cb in callbacks:
            result = cb(cursor)
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
