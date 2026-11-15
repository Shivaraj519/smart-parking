import sqlite3
import re

def setup_sqlite():
    conn = sqlite3.connect('smart_parking.db')
    cursor = conn.cursor()

    with open('schema_sqlite_compat.sql', 'r', encoding='utf-8') as f:
        schema = f.read()

    # Strip line comments
    clean_schema = re.sub(r'--.*?\n', '\n', schema)
    for stmt in clean_schema.split(';'):
        stmt = stmt.strip()
        if stmt and not stmt.startswith('CREATE OR REPLACE VIEW'):
            try:
                cursor.execute(stmt)
            except Exception as e:
                print('Schema notice:', e, 'in', stmt[:50].replace('\n', ' '))
    conn.commit()

    # Views
    conn.execute('''CREATE VIEW IF NOT EXISTS view_available_slots_summary AS
    SELECT 
        pa.area_id,
        pa.area_name,
        pa.location_address,
        ps.supported_vehicle_type,
        COUNT(ps.slot_id) AS total_slots,
        SUM(CASE WHEN ps.slot_status = 'AVAILABLE' THEN 1 ELSE 0 END) AS available_slots,
        SUM(CASE WHEN ps.slot_status = 'RESERVED' THEN 1 ELSE 0 END) AS reserved_slots,
        SUM(CASE WHEN ps.slot_status = 'OCCUPIED' THEN 1 ELSE 0 END) AS occupied_slots,
        pr.base_hourly_rate
    FROM Parking_Areas pa
    JOIN Parking_Slots ps ON pa.area_id = ps.area_id
    LEFT JOIN Pricing pr ON pa.area_id = pr.area_id AND ps.supported_vehicle_type = pr.vehicle_type
    WHERE pa.operating_status = 'OPEN'
    GROUP BY pa.area_id, pa.area_name, pa.location_address, ps.supported_vehicle_type, pr.base_hourly_rate;''')

    conn.execute('''CREATE VIEW IF NOT EXISTS view_payment_audit_trail AS
    SELECT 
        p.payment_id,
        p.transaction_reference,
        p.amount,
        p.payment_method,
        p.payment_status,
        p.paid_at,
        u.user_id,
        u.full_name AS customer_name,
        u.email AS customer_email,
        r.booking_code,
        s.session_id,
        s.entry_time,
        s.exit_time,
        s.duration_minutes
    FROM Payments p
    JOIN Users u ON p.user_id = u.user_id
    LEFT JOIN Reservations r ON p.reservation_id = r.reservation_id
    LEFT JOIN Parking_Sessions s ON p.session_id = s.session_id;''')

    conn.commit()

    # Load sample data
    with open('sample_data.sql', 'r', encoding='utf-8') as f:
        sample = f.read()

    sample = re.sub(r'USE .*?;', '', sample)
    sample = re.sub(r'DATE_SUB\(NOW\(\), INTERVAL (\d+) HOUR\)', "datetime('now', '-\\1 hours')", sample)
    sample = re.sub(r'DATE_ADD\(NOW\(\), INTERVAL (\d+) HOUR\)', "datetime('now', '+\\1 hours')", sample)
    sample = re.sub(r'DATE_SUB\(NOW\(\), INTERVAL (\d+) MINUTE\)', "datetime('now', '-\\1 minutes')", sample)
    sample = re.sub(r'DATE_SUB\(NOW\(\), INTERVAL (\d+) DAY\)', "datetime('now', '-\\1 days')", sample)
    sample = re.sub(r'DATE_SUB\(NOW\(\), INTERVAL (\d+) DAY - INTERVAL (\d+) HOUR\)', "datetime('now', '-\\1 days', '+\\2 hours')", sample)
    sample = re.sub(r'DATE_SUB\(NOW\(\), INTERVAL (\d+) DAY - INTERVAL (\d+) MINUTE\)', "datetime('now', '-\\1 days', '+\\2 minutes')", sample)
    sample = re.sub(r'NOW\(\)', "datetime('now')", sample)
    sample = sample.replace('TRUE', '1').replace('FALSE', '0')

    clean_sample = re.sub(r'--.*?\n', '\n', sample)
    for stmt in clean_sample.split(';'):
        stmt = stmt.strip()
        if stmt:
            try:
                cursor.execute(stmt)
            except Exception as e:
                print('Data notice:', e, 'in', stmt[:50].replace('\n', ' '))
    conn.commit()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cursor.fetchall()]
    print("Tables created in SQLite:", tables)
    cursor.execute("SELECT COUNT(*) FROM Users;")
    print("Users count:", cursor.fetchone()[0])
    cursor.execute("SELECT COUNT(*) FROM Vehicles;")
    print("Vehicles count:", cursor.fetchone()[0])
    cursor.execute("SELECT COUNT(*) FROM Parking_Slots;")
    print("Slots count:", cursor.fetchone()[0])
    cursor.execute("SELECT COUNT(*) FROM Reservations;")
    print("Reservations count:", cursor.fetchone()[0])
    cursor.close()
    conn.close()

if __name__ == '__main__':
    setup_sqlite()
