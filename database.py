import os
import re
import datetime
from decimal import Decimal
import secrets

# Determine DB Driver
DB_TYPE = os.getenv('DB_TYPE', 'AUTO') # AUTO, MYSQL, SQLITE
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'smart_parking_db')

_active_driver = None
_mysql_pool = None

def get_active_driver():
    global _active_driver
    if _active_driver is not None:
        return _active_driver

    if DB_TYPE == 'MYSQL':
        _active_driver = 'MYSQL'
        return _active_driver
    elif DB_TYPE == 'SQLITE':
        _active_driver = 'SQLITE'
        return _active_driver

    # In AUTO mode, probe MySQL first
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            connection_timeout=2
        )
        conn.close()
        _active_driver = 'MYSQL'
    except Exception:
        _active_driver = 'SQLITE'
    return _active_driver

def set_active_driver(driver_name):
    global _active_driver
    _active_driver = driver_name

def get_db_connection():
    driver = get_active_driver()
    if driver == 'MYSQL':
        global _mysql_pool
        import mysql.connector
        from mysql.connector import pooling
        if _mysql_pool is None:
            _mysql_pool = pooling.MySQLConnectionPool(
                pool_name="smart_parking_pool",
                pool_size=5,
                pool_reset_session=True,
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                autocommit=False
            )
        try:
            return _mysql_pool.get_connection()
        except Exception:
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
        import shutil
        data_dir = os.getenv('DATA_DIR', os.path.dirname(__file__))
        os.makedirs(data_dir, exist_ok=True)
        db_path = os.path.join(data_dir, 'smart_parking.db')
        local_db = os.path.join(os.path.dirname(__file__), 'smart_parking.db')
        if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
            if os.path.exists(local_db) and os.path.getsize(local_db) > 0 and db_path != local_db:
                try:
                    shutil.copy2(local_db, db_path)
                except Exception:
                    pass
            if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
                try:
                    import setup_local_db
                    setup_local_db.setup_sqlite(db_path)
                except Exception as e:
                    print("Notice: Auto db setup:", e)
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        # Enable foreign key support in SQLite
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

def execute_query(query, params=None, fetch_one=False, fetch_all=True, commit=False):
    """
    Executes a SQL query safely and returns dict or list of dicts.
    Handles parameter syntax (%s vs ?) automatically for portability.
    """
    driver = get_active_driver()
    conn = get_db_connection()
    
    # Adapt %s parameter placeholder if running on SQLite
    adapted_query = query
    if driver == 'SQLITE':
        # Replace MySQL specific date/timestamp functions and intervals for SQLite compatibility
        # Replace DATE_SUB(NOW(), INTERVAL X DAY) -> datetime('now', 'localtime', '-X days')
        adapted_query = re.sub(
            r"DATE_SUB\s*\(\s*NOW\(\)\s*,\s*INTERVAL\s+(\d+)\s+DAY\s*\)",
            r"datetime('now', 'localtime', '-\1 days')",
            adapted_query,
            flags=re.IGNORECASE
        )
        adapted_query = re.sub(
            r"DATE_SUB\s*\(\s*NOW\(\)\s*,\s*INTERVAL\s+(\d+)\s+HOUR\s*\)",
            r"datetime('now', 'localtime', '-\1 hours')",
            adapted_query,
            flags=re.IGNORECASE
        )
        adapted_query = adapted_query.replace('CURRENT_DATE', "date('now', 'localtime')")
        adapted_query = adapted_query.replace('NOW()', "datetime('now', 'localtime')")
        # Replace %s with ? for sqlite3
        adapted_query = adapted_query.replace('%s', '?')
        cursor = conn.cursor()
    else:
        cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(adapted_query, params or ())
        if commit:
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        if fetch_one:
            row = cursor.fetchone()
            if row and driver == 'SQLITE':
                return dict(row)
            return row
        if fetch_all:
            rows = cursor.fetchall()
            if rows and driver == 'SQLITE':
                return [dict(r) for r in rows]
            return rows
        return None
    except Exception as e:
        if commit:
            try:
                conn.rollback()
            except Exception:
                pass
        raise e
    finally:
        cursor.close()
        conn.close()

# ---------------------------------------------------------------------
# ACID TRANSACTION HELPER FOR SLOT RESERVATION
# ---------------------------------------------------------------------
def book_slot_transaction(user_id, vehicle_id, slot_id, start_time, end_time, payment_method):
    """
    Executes atomic reservation with lock verification and double-booking check.
    Works natively on MySQL using Stored Procedure or ACID transaction logic,
    and equally on SQLite fallback with strict transaction isolation.
    """
    driver = get_active_driver()

    if driver == 'MYSQL':
        # Invoke Stored Procedure sp_reserve_parking_slot
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Arguments: IN user_id, vehicle_id, slot_id, start_time, end_time, payment_method,
            # OUT res_id, booking_code, total_amount, status_message
            args = [user_id, vehicle_id, slot_id, start_time, end_time, payment_method, 0, '', 0.0, '']
            result_args = cursor.callproc('sp_reserve_parking_slot', args)
            conn.commit()
            res_id = result_args[6]
            booking_code = result_args[7]
            total_amount = float(result_args[8])
            status_msg = result_args[9]

            if res_id > 0:
                return {'success': True, 'reservation_id': res_id, 'booking_code': booking_code, 'amount': total_amount, 'message': status_msg}
            else:
                return {'success': False, 'message': status_msg}
        except Exception as e:
            conn.rollback()
            return {'success': False, 'message': str(e)}
        finally:
            cursor.close()
            conn.close()
    else:
        # Pure Python ACID Transaction implementation adhering to DBMS locking semantics
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            conn.execute("BEGIN IMMEDIATE TRANSACTION;")

            # 1. Validate vehicle
            cursor.execute("SELECT vehicle_type FROM Vehicles WHERE vehicle_id = ? AND user_id = ?", (vehicle_id, user_id))
            veh_row = cursor.fetchone()
            if not veh_row:
                conn.rollback()
                return {'success': False, 'message': 'Vehicle not registered or does not belong to user.'}
            veh_type = veh_row['vehicle_type']

            # 2. Validate Slot & Lock
            cursor.execute("SELECT area_id, slot_status, supported_vehicle_type FROM Parking_Slots WHERE slot_id = ?", (slot_id,))
            slot_row = cursor.fetchone()
            if not slot_row:
                conn.rollback()
                return {'success': False, 'message': 'Selected slot does not exist.'}

            if slot_row['slot_status'] == 'UNDER_MAINTENANCE':
                conn.rollback()
                return {'success': False, 'message': 'Slot is currently under maintenance.'}

            if slot_row['supported_vehicle_type'] != veh_type:
                conn.rollback()
                return {'success': False, 'message': f"Slot type ({slot_row['supported_vehicle_type']}) does not fit vehicle ({veh_type})."}

            # 3. Check for overlapping reservations
            overlap_sql = """
            SELECT COUNT(*) AS cnt FROM Reservations 
            WHERE slot_id = ? 
              AND booking_status IN ('CONFIRMED', 'CHECKED_IN')
              AND (
                  (? >= start_time AND ? < end_time) OR
                  (? > start_time AND ? <= end_time) OR
                  (? <= start_time AND ? >= end_time)
              )
            """
            cursor.execute(overlap_sql, (slot_id, start_time, start_time, end_time, end_time, start_time, end_time))
            if cursor.fetchone()['cnt'] > 0:
                conn.rollback()
                return {'success': False, 'message': 'Slot is already booked for the selected time window. Concurrency conflict resolved.'}

            # 4. Fetch Pricing
            cursor.execute("SELECT base_hourly_rate FROM Pricing WHERE area_id = ? AND vehicle_type = ?", (slot_row['area_id'], veh_type))
            price_row = cursor.fetchone()
            hourly_rate = float(price_row['base_hourly_rate']) if price_row else 30.0

            # Calculate duration hours
            t1 = datetime.datetime.fromisoformat(start_time.replace(' ', 'T'))
            t2 = datetime.datetime.fromisoformat(end_time.replace(' ', 'T'))
            duration_hours = max(1.0, (t2 - t1).total_seconds() / 3600.0)
            total_amount = round(duration_hours * hourly_rate, 2)

            # 5. Check wallet balance if paying via WALLET
            if payment_method == 'WALLET':
                cursor.execute("SELECT wallet_balance FROM Users WHERE user_id = ?", (user_id,))
                user_row = cursor.fetchone()
                wallet = float(user_row['wallet_balance'])
                if wallet < total_amount:
                    conn.rollback()
                    return {'success': False, 'message': f"Insufficient wallet balance. Required: ₹{total_amount:.2f}, Available: ₹{wallet:.2f}"}
                
                # Deduct wallet
                cursor.execute("UPDATE Users SET wallet_balance = wallet_balance - ? WHERE user_id = ?", (total_amount, user_id))

            # 6. Generate unique booking code
            booking_code = f"PK-{secrets.token_hex(3).upper()}"

            # 7. Insert Reservation
            cursor.execute("""
            INSERT INTO Reservations (user_id, vehicle_id, slot_id, start_time, end_time, estimated_cost, booking_status, booking_code)
            VALUES (?, ?, ?, ?, ?, ?, 'CONFIRMED', ?)
            """, (user_id, vehicle_id, slot_id, start_time, end_time, total_amount, booking_code))
            res_id = cursor.lastrowid

            # Update Slot status to RESERVED
            cursor.execute("UPDATE Parking_Slots SET slot_status = 'RESERVED' WHERE slot_id = ?", (slot_id,))

            # 8. Record Payment
            txn_ref = f"TXN-{secrets.token_hex(6).upper()}"
            cursor.execute("""
            INSERT INTO Payments (reservation_id, user_id, amount, payment_method, payment_status, transaction_reference)
            VALUES (?, ?, ?, ?, 'SUCCESS', ?)
            """, (res_id, user_id, total_amount, payment_method, txn_ref))

            conn.commit()
            return {'success': True, 'reservation_id': res_id, 'booking_code': booking_code, 'amount': total_amount, 'message': 'Reservation confirmed successfully!'}
        except Exception as e:
            conn.rollback()
            return {'success': False, 'message': f'Database transaction failed: {str(e)}'}
        finally:
            cursor.close()
            conn.close()

# ---------------------------------------------------------------------
# VEHICLE CHECK-IN (ENTRY)
# ---------------------------------------------------------------------
def checkin_vehicle(booking_code):
    driver = get_active_driver()
    if driver == 'MYSQL':
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            args = [booking_code, 0, '']
            result_args = cursor.callproc('sp_process_vehicle_entry', args)
            conn.commit()
            session_id = result_args[1]
            status_msg = result_args[2]
            return {'success': session_id > 0, 'session_id': session_id, 'message': status_msg}
        except Exception as e:
            conn.rollback()
            return {'success': False, 'message': str(e)}
        finally:
            cursor.close()
            conn.close()
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            conn.execute("BEGIN IMMEDIATE TRANSACTION;")
            cursor.execute("SELECT reservation_id, slot_id, vehicle_id, booking_status FROM Reservations WHERE booking_code = ?", (booking_code,))
            res = cursor.fetchone()
            if not res:
                conn.rollback()
                return {'success': False, 'message': 'Invalid booking reference code.'}
            if res['booking_status'] != 'CONFIRMED':
                conn.rollback()
                return {'success': False, 'message': f"Booking is in status '{res['booking_status']}'. Cannot check in."}

            cursor.execute("""
            INSERT INTO Parking_Sessions (reservation_id, slot_id, vehicle_id, entry_time, session_status)
            VALUES (?, ?, ?, datetime('now', 'localtime'), 'ACTIVE')
            """, (res['reservation_id'], res['slot_id'], res['vehicle_id']))
            session_id = cursor.lastrowid

            cursor.execute("UPDATE Parking_Slots SET slot_status = 'OCCUPIED' WHERE slot_id = ?", (res['slot_id'],))
            cursor.execute("UPDATE Reservations SET booking_status = 'CHECKED_IN' WHERE reservation_id = ?", (res['reservation_id'],))

            conn.commit()
            return {'success': True, 'session_id': session_id, 'message': 'Vehicle entry logged. Slot marked OCCUPIED.'}
        except Exception as e:
            conn.rollback()
            return {'success': False, 'message': str(e)}
        finally:
            cursor.close()
            conn.close()

# ---------------------------------------------------------------------
# VEHICLE CHECK-OUT (EXIT)
# ---------------------------------------------------------------------
def checkout_vehicle(session_id, payment_method='WALLET'):
    driver = get_active_driver()
    if driver == 'MYSQL':
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            args = [session_id, payment_method, 0.0, 0, '']
            result_args = cursor.callproc('sp_process_vehicle_exit', args)
            conn.commit()
            return {
                'success': True,
                'final_amount': float(result_args[2]),
                'duration_mins': int(result_args[3]),
                'message': result_args[4]
            }
        except Exception as e:
            conn.rollback()
            return {'success': False, 'message': str(e)}
        finally:
            cursor.close()
            conn.close()
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            conn.execute("BEGIN IMMEDIATE TRANSACTION;")
            cursor.execute("""
            SELECT s.reservation_id, s.slot_id, s.vehicle_id, s.entry_time, sl.area_id, v.vehicle_type, v.user_id
            FROM Parking_Sessions s
            JOIN Parking_Slots sl ON s.slot_id = sl.slot_id
            JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
            WHERE s.session_id = ? AND s.session_status = 'ACTIVE'
            """, (session_id,))
            sess = cursor.fetchone()
            if not sess:
                conn.rollback()
                return {'success': False, 'message': 'Active parking session not found.'}

            # Calculate duration
            entry_dt = datetime.datetime.fromisoformat(sess['entry_time'].replace(' ', 'T'))
            now_dt = datetime.datetime.now()
            duration_mins = max(1, int((now_dt - entry_dt).total_seconds() / 60))

            cursor.execute("SELECT base_hourly_rate FROM Pricing WHERE area_id = ? AND vehicle_type = ?", (sess['area_id'], sess['vehicle_type']))
            pr_row = cursor.fetchone()
            rate = float(pr_row['base_hourly_rate']) if pr_row else 30.0

            billable_hours = max(1, (duration_mins + 59) // 60)
            final_amount = round(billable_hours * rate, 2)

            # Check paid initially
            initial_paid = 0.0
            if sess['reservation_id']:
                cursor.execute("SELECT COALESCE(SUM(amount), 0) AS total_paid FROM Payments WHERE reservation_id = ? AND payment_status = 'SUCCESS'", (sess['reservation_id'],))
                initial_paid = float(cursor.fetchone()['total_paid'])

            if final_amount > initial_paid:
                additional_due = final_amount - initial_paid
                cursor.execute("""
                INSERT INTO Payments (session_id, user_id, amount, payment_method, payment_status, transaction_reference)
                VALUES (?, ?, ?, ?, 'SUCCESS', ?)
                """, (session_id, sess['user_id'], additional_due, payment_method, f"TXN-OVERSTAY-{secrets.token_hex(4).upper()}"))

            cursor.execute("""
            UPDATE Parking_Sessions 
            SET session_status = 'COMPLETED', exit_time = datetime('now', 'localtime'), duration_minutes = ?, calculated_amount = ?
            WHERE session_id = ?
            """, (duration_mins, final_amount, session_id))

            cursor.execute("UPDATE Parking_Slots SET slot_status = 'AVAILABLE' WHERE slot_id = ?", (sess['slot_id'],))
            if sess['reservation_id']:
                cursor.execute("UPDATE Reservations SET booking_status = 'COMPLETED' WHERE reservation_id = ?", (sess['reservation_id'],))

            conn.commit()
            return {'success': True, 'final_amount': final_amount, 'duration_mins': duration_mins, 'message': f"Checkout successful! Duration: {duration_mins} mins. Total: ₹{final_amount:.2f}"}
        except Exception as e:
            conn.rollback()
            return {'success': False, 'message': str(e)}
        finally:
            cursor.close()
            conn.close()
