import os
import datetime
from decimal import Decimal
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for, 
    session, flash, jsonify, g
)
from werkzeug.security import generate_password_hash, check_password_hash
import database

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'smart-parking-dbms-secret-key-2026')
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=4)

# ---------------------------------------------------------------------
# AUTHENTICATION & ACCESS DECORATORS
# ---------------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please sign in to access driver services.', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_id'):
            flash('Administrator authentication required.', 'error')
            return redirect(url_for('admin_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def load_current_user_context():
    g.user = None
    g.admin = None
    if session.get('user_id'):
        user = database.execute_query(
            "SELECT user_id, full_name, email, phone_number, license_number, wallet_balance FROM Users WHERE user_id = %s",
            (session['user_id'],),
            fetch_one=True
        )
        if user:
            g.user = user
            session['wallet_balance'] = float(user['wallet_balance'])
    elif session.get('admin_id'):
        admin = database.execute_query(
            "SELECT admin_id, username, full_name, email, role FROM Admins WHERE admin_id = %s",
            (session['admin_id'],),
            fetch_one=True
        )
        if admin:
            g.admin = admin

# ---------------------------------------------------------------------
# PUBLIC ROUTES
# ---------------------------------------------------------------------
@app.route('/')
def index():
    # Fetch real statistics directly from MySQL
    tot_slots = database.execute_query("SELECT COUNT(*) AS c FROM Parking_Slots", fetch_one=True)['c']
    avail_slots = database.execute_query("SELECT COUNT(*) AS c FROM Parking_Slots WHERE slot_status = 'AVAILABLE'", fetch_one=True)['c']
    occ_slots = database.execute_query("SELECT COUNT(*) AS c FROM Parking_Slots WHERE slot_status = 'OCCUPIED'", fetch_one=True)['c']
    tot_users = database.execute_query("SELECT COUNT(*) AS c FROM Users", fetch_one=True)['c']
    tot_vehs = database.execute_query("SELECT COUNT(*) AS c FROM Vehicles", fetch_one=True)['c']
    tot_areas = database.execute_query("SELECT COUNT(*) AS c FROM Parking_Areas WHERE operating_status = 'OPEN'", fetch_one=True)['c']

    stats = {
        'total_slots': tot_slots,
        'available_slots': avail_slots,
        'occupied_slots': occ_slots,
        'registered_users': tot_users,
        'registered_vehicles': tot_vehs,
        'total_areas': tot_areas
    }

    # Fetch areas with available counts
    areas = database.execute_query("""
        SELECT pa.area_id, pa.area_name, pa.location_address, pa.total_capacity, pa.operating_status,
               (SELECT COUNT(*) FROM Parking_Slots ps WHERE ps.area_id = pa.area_id AND ps.slot_status = 'AVAILABLE') AS available_count
        FROM Parking_Areas pa
        WHERE pa.operating_status = 'OPEN'
        ORDER BY pa.area_name ASC;
    """)

    return render_template('index.html', stats=stats, areas=areas)

@app.route('/availability')
def parking_availability():
    area_id = request.args.get('area_id', '')
    veh_type = request.args.get('vehicle_type', '')
    status = request.args.get('status', '')

    query = """
    SELECT ps.slot_id, ps.slot_number, ps.floor_level, ps.supported_vehicle_type, 
           ps.slot_status, ps.is_ev_charging_equipped,
           pa.area_id, pa.area_name, pa.location_address,
           COALESCE(pr.base_hourly_rate, 30.00) AS base_hourly_rate
    FROM Parking_Slots ps
    INNER JOIN Parking_Areas pa ON ps.area_id = pa.area_id
    LEFT JOIN Pricing pr ON pa.area_id = pr.area_id AND ps.supported_vehicle_type = pr.vehicle_type
    WHERE pa.operating_status = 'OPEN'
    """
    params = []
    if area_id:
        query += " AND ps.area_id = %s"
        params.append(area_id)
    if veh_type:
        query += " AND ps.supported_vehicle_type = %s"
        params.append(veh_type)
    if status:
        query += " AND ps.slot_status = %s"
        params.append(status)

    query += " ORDER BY pa.area_name, ps.slot_number ASC;"

    slots = database.execute_query(query, params)
    areas = database.execute_query("SELECT area_id, area_name FROM Parking_Areas WHERE operating_status = 'OPEN' ORDER BY area_name ASC;")

    return render_template('parking_availability.html', 
                           slots=slots, 
                           areas=areas, 
                           selected_area=area_id, 
                           selected_type=veh_type, 
                           selected_status=status)

# ---------------------------------------------------------------------
# AUTHENTICATION: USER & ADMIN
# ---------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        pwd = request.form.get('password', '')

        user = database.execute_query(
            "SELECT * FROM Users WHERE email = %s",
            (email,),
            fetch_one=True
        )

        if user and check_password_hash(user['password_hash'], pwd):
            session.clear()
            session['user_id'] = user['user_id']
            session['user_name'] = user['full_name']
            session['wallet_balance'] = float(user['wallet_balance'])
            flash(f"Welcome back, {user['full_name']}!", 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid email or password. For demo, try aarav.patel@gmail.com / user123', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone_number', '').strip()
        license_num = request.form.get('license_number', '').strip()
        wallet = float(request.form.get('wallet_balance', 500.0))
        pwd = request.form.get('password', '')

        if not all([full_name, email, phone, license_num, pwd]):
            flash('All fields are required.', 'error')
            return render_template('register.html')

        pwd_hash = generate_password_hash(pwd)

        try:
            user_id = database.execute_query(
                """INSERT INTO Users (full_name, email, phone_number, password_hash, license_number, wallet_balance)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (full_name, email, phone, pwd_hash, license_num, wallet),
                commit=True
            )
            session.clear()
            session['user_id'] = user_id
            session['user_name'] = full_name
            session['wallet_balance'] = wallet
            flash('Registration successful! Welcome to ParkSmart.', 'success')
            return redirect(url_for('user_dashboard'))
        except Exception as e:
            flash(f'Registration failed (e.g. duplicate email or license): {str(e)}', 'error')

    return render_template('register.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        pwd = request.form.get('password', '')

        admin = database.execute_query(
            "SELECT * FROM Admins WHERE username = %s OR email = %s",
            (username, username),
            fetch_one=True
        )

        if admin and check_password_hash(admin['password_hash'], pwd):
            session.clear()
            session['admin_id'] = admin['admin_id']
            session['admin_name'] = admin['full_name']
            session['admin_role'] = admin['role']
            flash(f"Admin Authorization Granted. Welcome {admin['full_name']}.", 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials. Demo: admin / admin123', 'error')

    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been signed out.', 'success')
    return redirect(url_for('index'))

# ---------------------------------------------------------------------
# USER MODULE ROUTES
# ---------------------------------------------------------------------
@app.route('/user/dashboard')
@login_required
def user_dashboard():
    user = g.user
    vehicles = database.execute_query(
        "SELECT * FROM Vehicles WHERE user_id = %s ORDER BY created_at DESC",
        (user['user_id'],)
    )

    # Detailed join for user reservations
    reservations = database.execute_query("""
        SELECT r.reservation_id, r.booking_code, r.start_time, r.end_time, r.estimated_cost, r.booking_status,
               s.slot_number, pa.area_name, v.license_plate, v.vehicle_type, v.make_model
        FROM Reservations r
        JOIN Parking_Slots s ON r.slot_id = s.slot_id
        JOIN Parking_Areas pa ON s.area_id = pa.area_id
        JOIN Vehicles v ON r.vehicle_id = v.vehicle_id
        WHERE r.user_id = %s
        ORDER BY r.created_at DESC;
    """, (user['user_id'],))

    spent_row = database.execute_query(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM Payments WHERE user_id = %s AND payment_status = 'SUCCESS'",
        (user['user_id'],),
        fetch_one=True
    )
    total_spent = float(spent_row['total'])

    return render_template('user/dashboard.html', 
                           user=user, 
                           vehicles=vehicles, 
                           reservations=reservations, 
                           total_spent=total_spent)

@app.route('/user/vehicles')
@login_required
def user_vehicles():
    vehicles = database.execute_query(
        "SELECT * FROM Vehicles WHERE user_id = %s ORDER BY created_at DESC",
        (session['user_id'],)
    )
    return render_template('user/vehicles.html', vehicles=vehicles)

@app.route('/user/vehicles/add', methods=['POST'])
@login_required
def user_add_vehicle():
    plate = request.form.get('license_plate', '').strip().upper()
    v_type = request.form.get('vehicle_type', 'SEDAN')
    make_model = request.form.get('make_model', '').strip()
    color = request.form.get('color', '').strip()

    if not plate:
        flash('License plate is required.', 'error')
        return redirect(url_for('user_vehicles'))

    try:
        database.execute_query(
            "INSERT INTO Vehicles (user_id, license_plate, vehicle_type, make_model, color) VALUES (%s, %s, %s, %s, %s)",
            (session['user_id'], plate, v_type, make_model, color),
            commit=True
        )
        flash(f'Vehicle {plate} successfully registered!', 'success')
    except Exception as e:
        flash(f'Failed to add vehicle: {str(e)}', 'error')

    return redirect(url_for('user_vehicles'))

@app.route('/user/vehicles/delete/<int:vehicle_id>', methods=['POST'])
@login_required
def user_delete_vehicle(vehicle_id):
    try:
        database.execute_query(
            "DELETE FROM Vehicles WHERE vehicle_id = %s AND user_id = %s",
            (vehicle_id, session['user_id']),
            commit=True
        )
        flash('Vehicle removed successfully.', 'success')
    except Exception as e:
        flash(f'Cannot delete vehicle (active bookings or sessions reference it): {str(e)}', 'error')
    return redirect(url_for('user_vehicles'))

@app.route('/user/reserve', methods=['GET', 'POST'])
@login_required
def user_reserve_slot():
    if request.method == 'POST':
        slot_id = int(request.form.get('slot_id'))
        vehicle_id = int(request.form.get('vehicle_id'))
        start_time = request.form.get('start_time').replace('T', ' ') + ':00'
        end_time = request.form.get('end_time').replace('T', ' ') + ':00'
        pay_method = request.form.get('payment_method', 'WALLET')

        # Execute Concurrency-Controlled ACID Reservation
        res = database.book_slot_transaction(
            user_id=session['user_id'],
            vehicle_id=vehicle_id,
            slot_id=slot_id,
            start_time=start_time,
            end_time=end_time,
            payment_method=pay_method
        )

        if res['success']:
            flash(res['message'], 'success')
            return redirect(url_for('user_booking_confirmation', reservation_id=res['reservation_id']))
        else:
            flash(res['message'], 'error')
            return redirect(url_for('user_reserve_slot', slot_id=slot_id))

    # GET Request
    slot_id = request.args.get('slot_id')
    if not slot_id:
        flash('Please select a parking slot to book.', 'error')
        return redirect(url_for('parking_availability'))

    slot = database.execute_query("""
        SELECT ps.slot_id, ps.slot_number, ps.floor_level, ps.supported_vehicle_type, ps.slot_status, ps.is_ev_charging_equipped,
               pa.area_id, pa.area_name, pa.location_address,
               COALESCE(pr.base_hourly_rate, 30.00) AS base_hourly_rate
        FROM Parking_Slots ps
        JOIN Parking_Areas pa ON ps.area_id = pa.area_id
        LEFT JOIN Pricing pr ON pa.area_id = pr.area_id AND ps.supported_vehicle_type = pr.vehicle_type
        WHERE ps.slot_id = %s;
    """, (slot_id,), fetch_one=True)

    if not slot:
        flash('Slot bay not found.', 'error')
        return redirect(url_for('parking_availability'))

    vehicles = database.execute_query("SELECT * FROM Vehicles WHERE user_id = %s", (session['user_id'],))
    
    # Prepopulate default time window (now to now + 2 hours)
    now = datetime.datetime.now()
    default_start = now.strftime('%Y-%m-%dT%H:%M')
    default_end = (now + datetime.timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M')

    return render_template('user/reserve.html', 
                           slot=slot, 
                           vehicles=vehicles, 
                           user=g.user,
                           default_start=default_start,
                           default_end=default_end)

@app.route('/user/confirmation/<int:reservation_id>')
@login_required
def user_booking_confirmation(reservation_id):
    res = database.execute_query("""
        SELECT r.*, s.slot_number, s.floor_level, pa.area_name, v.license_plate, v.vehicle_type
        FROM Reservations r
        JOIN Parking_Slots s ON r.slot_id = s.slot_id
        JOIN Parking_Areas pa ON s.area_id = pa.area_id
        JOIN Vehicles v ON r.vehicle_id = v.vehicle_id
        WHERE r.reservation_id = %s AND r.user_id = %s;
    """, (reservation_id, session['user_id']), fetch_one=True)

    if not res:
        flash('Reservation details not found.', 'error')
        return redirect(url_for('user_dashboard'))

    payment = database.execute_query(
        "SELECT * FROM Payments WHERE reservation_id = %s LIMIT 1",
        (reservation_id,),
        fetch_one=True
    )

    return render_template('user/confirmation.html', res=res, payment=payment)

@app.route('/user/reservations')
@login_required
def user_booking_history():
    reservations = database.execute_query("""
        SELECT r.*, s.slot_number, pa.area_name, v.license_plate
        FROM Reservations r
        JOIN Parking_Slots s ON r.slot_id = s.slot_id
        JOIN Parking_Areas pa ON s.area_id = pa.area_id
        JOIN Vehicles v ON r.vehicle_id = v.vehicle_id
        WHERE r.user_id = %s
        ORDER BY r.created_at DESC;
    """, (session['user_id'],))
    return render_template('user/history.html', reservations=reservations)

@app.route('/user/reservations/cancel/<int:reservation_id>', methods=['POST'])
@login_required
def user_cancel_reservation(reservation_id):
    # Verify reservation ownership
    res = database.execute_query(
        "SELECT * FROM Reservations WHERE reservation_id = %s AND user_id = %s",
        (reservation_id, session['user_id']),
        fetch_one=True
    )
    if not res:
        flash('Reservation not found.', 'error')
        return redirect(url_for('user_dashboard'))

    if res['booking_status'] != 'CONFIRMED':
        flash(f"Cannot cancel booking with status '{res['booking_status']}'.", 'error')
        return redirect(url_for('user_dashboard'))

    try:
        # Atomic cancellation: Update reservation + refund wallet + release slot
        refund_amount = float(res['estimated_cost'])
        database.execute_query(
            "UPDATE Reservations SET booking_status = 'CANCELLED' WHERE reservation_id = %s",
            (reservation_id,),
            commit=True
        )
        database.execute_query(
            "UPDATE Parking_Slots SET slot_status = 'AVAILABLE' WHERE slot_id = %s",
            (res['slot_id'],),
            commit=True
        )
        database.execute_query(
            "UPDATE Users SET wallet_balance = wallet_balance + %s WHERE user_id = %s",
            (refund_amount, session['user_id']),
            commit=True
        )
        # Record refund in payments ledger
        database.execute_query(
            """INSERT INTO Payments (reservation_id, user_id, amount, payment_method, payment_status, transaction_reference)
               VALUES (%s, %s, %s, 'WALLET', 'REFUNDED', %s)""",
            (reservation_id, session['user_id'], refund_amount, f"REFUND-{reservation_id}-{int(datetime.datetime.now().timestamp())}"),
            commit=True
        )
        flash(f'Reservation {res["booking_code"]} cancelled. ₹{refund_amount:.2f} refunded to wallet.', 'success')
    except Exception as e:
        flash(f'Cancellation failed: {str(e)}', 'error')

    return redirect(url_for('user_dashboard'))

@app.route('/user/payments')
@login_required
def user_payments():
    payments = database.execute_query("""
        SELECT p.*, r.booking_code
        FROM Payments p
        LEFT JOIN Reservations r ON p.reservation_id = r.reservation_id
        WHERE p.user_id = %s
        ORDER BY p.paid_at DESC;
    """, (session['user_id'],))
    return render_template('user/payments.html', payments=payments)

@app.route('/user/wallet/topup', methods=['POST'])
@login_required
def user_topup_wallet():
    amount = float(request.form.get('amount', 500.0))
    if amount <= 0:
        flash('Top-up amount must be positive.', 'error')
        return redirect(url_for('user_dashboard'))

    try:
        database.execute_query(
            "UPDATE Users SET wallet_balance = wallet_balance + %s WHERE user_id = %s",
            (amount, session['user_id']),
            commit=True
        )
        database.execute_query(
            """INSERT INTO Payments (user_id, amount, payment_method, payment_status, transaction_reference)
               VALUES (%s, %s, 'UPI', 'SUCCESS', %s)""",
            (session['user_id'], amount, f"TOPUP-{session['user_id']}-{int(datetime.datetime.now().timestamp())}"),
            commit=True
        )
        flash(f'Successfully added ₹{amount:.2f} to your wallet!', 'success')
    except Exception as e:
        flash(f'Top-up failed: {str(e)}', 'error')

    return redirect(url_for('user_dashboard'))

# ---------------------------------------------------------------------
# GATE / ENTRY & EXIT PROCESSOR
# ---------------------------------------------------------------------
@app.route('/gate/checkin', methods=['POST'])
def gate_checkin():
    code = request.form.get('booking_code', '').strip().upper()
    if not code:
        flash('Please provide booking code.', 'error')
        return redirect(request.referrer or url_for('index'))

    res = database.checkin_vehicle(code)
    if res['success']:
        flash(res['message'], 'success')
    else:
        flash(res['message'], 'error')

    return redirect(request.referrer or url_for('user_dashboard'))

# ---------------------------------------------------------------------
# ADMIN MODULE ROUTES
# ---------------------------------------------------------------------
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    tot_slots = database.execute_query("SELECT COUNT(*) AS c FROM Parking_Slots", fetch_one=True)['c']
    avail_slots = database.execute_query("SELECT COUNT(*) AS c FROM Parking_Slots WHERE slot_status = 'AVAILABLE'", fetch_one=True)['c']
    res_slots = database.execute_query("SELECT COUNT(*) AS c FROM Parking_Slots WHERE slot_status = 'RESERVED'", fetch_one=True)['c']
    occ_slots = database.execute_query("SELECT COUNT(*) AS c FROM Parking_Slots WHERE slot_status = 'OCCUPIED'", fetch_one=True)['c']
    act_sess = database.execute_query("SELECT COUNT(*) AS c FROM Parking_Sessions WHERE session_status = 'ACTIVE'", fetch_one=True)['c']
    tot_users = database.execute_query("SELECT COUNT(*) AS c FROM Users", fetch_one=True)['c']
    tot_vehs = database.execute_query("SELECT COUNT(*) AS c FROM Vehicles", fetch_one=True)['c']
    
    rev_tot = database.execute_query("SELECT COALESCE(SUM(amount), 0) AS c FROM Payments WHERE payment_status = 'SUCCESS'", fetch_one=True)['c']
    rev_today = database.execute_query("SELECT COALESCE(SUM(amount), 0) AS c FROM Payments WHERE payment_status = 'SUCCESS' AND DATE(paid_at) = CURRENT_DATE", fetch_one=True)['c']

    stats = {
        'total_slots': tot_slots,
        'available_slots': avail_slots,
        'reserved_slots': res_slots,
        'occupied_slots': occ_slots,
        'active_sessions': act_sess,
        'total_users': tot_users,
        'total_vehicles': tot_vehs,
        'total_revenue': float(rev_tot),
        'today_revenue': float(rev_today)
    }

    # Active parking sessions with duration
    active_sessions = database.execute_query("""
        SELECT s.session_id, s.entry_time, s.slot_id, s.vehicle_id,
               v.license_plate, v.vehicle_type, u.full_name AS driver_name, u.phone_number,
               sl.slot_number, pa.area_name,
               COALESCE(pr.base_hourly_rate, 30.0) AS base_hourly_rate
        FROM Parking_Sessions s
        JOIN Parking_Slots sl ON s.slot_id = sl.slot_id
        JOIN Parking_Areas pa ON sl.area_id = pa.area_id
        JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
        JOIN Users u ON v.user_id = u.user_id
        LEFT JOIN Pricing pr ON pa.area_id = pr.area_id AND v.vehicle_type = pr.vehicle_type
        WHERE s.session_status = 'ACTIVE'
        ORDER BY s.entry_time ASC;
    """)

    # Compute duration and estimated charge in Python for cross-DB compatibility
    now = datetime.datetime.now()
    for s in active_sessions:
        entry_dt = datetime.datetime.fromisoformat(str(s['entry_time']).replace(' ', 'T'))
        mins = max(1, int((now - entry_dt).total_seconds() / 60))
        s['current_duration_mins'] = mins
        hours = max(1, (mins + 59) // 60)
        s['estimated_accrued_charge'] = hours * float(s['base_hourly_rate'])

    # Category chart data
    cat_rows = database.execute_query("""
        SELECT supported_vehicle_type, 
               COUNT(*) AS total_bays,
               SUM(CASE WHEN slot_status = 'AVAILABLE' THEN 1 ELSE 0 END) AS avail_bays
        FROM Parking_Slots
        GROUP BY supported_vehicle_type;
    """)
    category_labels = [r['supported_vehicle_type'].replace('_', ' ') for r in cat_rows]
    category_totals = [r['total_bays'] for r in cat_rows]
    category_available = [r['avail_bays'] for r in cat_rows]

    return render_template('admin/dashboard.html',
                           admin=g.admin,
                           stats=stats,
                           active_sessions=active_sessions,
                           category_labels=category_labels,
                           category_totals=category_totals,
                           category_available=category_available,
                           db_driver=database.get_active_driver())

@app.route('/admin/checkout/<int:session_id>', methods=['POST'])
@admin_required
def admin_checkout_session(session_id):
    res = database.checkout_vehicle(session_id, payment_method='WALLET')
    if res['success']:
        flash(res['message'], 'success')
    else:
        flash(res['message'], 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/areas')
@admin_required
def admin_parking_areas():
    areas = database.execute_query("SELECT * FROM Parking_Areas ORDER BY area_id ASC;")
    return render_template('admin/parking_areas.html', areas=areas)

@app.route('/admin/areas/add', methods=['POST'])
@admin_required
def admin_add_area():
    name = request.form.get('area_name', '').strip()
    addr = request.form.get('location_address', '').strip()
    cap = int(request.form.get('total_capacity', 20))
    status = request.form.get('operating_status', 'OPEN')

    try:
        database.execute_query(
            "INSERT INTO Parking_Areas (area_name, location_address, total_capacity, operating_status) VALUES (%s, %s, %s, %s)",
            (name, addr, cap, status),
            commit=True
        )
        flash(f'Facility {name} successfully added!', 'success')
    except Exception as e:
        flash(f'Failed to add facility: {str(e)}', 'error')
    return redirect(url_for('admin_parking_areas'))

@app.route('/admin/areas/edit/<int:area_id>', methods=['POST'])
@admin_required
def admin_edit_area(area_id):
    name = request.form.get('area_name', '').strip()
    addr = request.form.get('location_address', '').strip()
    cap = int(request.form.get('total_capacity', 20))
    status = request.form.get('operating_status', 'OPEN')

    try:
        database.execute_query(
            "UPDATE Parking_Areas SET area_name = %s, location_address = %s, total_capacity = %s, operating_status = %s WHERE area_id = %s",
            (name, addr, cap, status, area_id),
            commit=True
        )
        flash('Facility updated.', 'success')
    except Exception as e:
        flash(f'Update failed: {str(e)}', 'error')
    return redirect(url_for('admin_parking_areas'))

@app.route('/admin/areas/delete/<int:area_id>', methods=['POST'])
@admin_required
def admin_delete_area(area_id):
    try:
        database.execute_query("DELETE FROM Parking_Areas WHERE area_id = %s", (area_id,), commit=True)
        flash('Facility removed.', 'success')
    except Exception as e:
        flash(f'Cannot delete facility: {str(e)}', 'error')
    return redirect(url_for('admin_parking_areas'))

@app.route('/admin/slots')
@admin_required
def admin_parking_slots():
    slots = database.execute_query("""
        SELECT ps.*, pa.area_name
        FROM Parking_Slots ps
        JOIN Parking_Areas pa ON ps.area_id = pa.area_id
        ORDER BY pa.area_name, ps.slot_number ASC;
    """)
    areas = database.execute_query("SELECT area_id, area_name FROM Parking_Areas ORDER BY area_name ASC;")
    return render_template('admin/parking_slots.html', slots=slots, areas=areas)

@app.route('/admin/slots/add', methods=['POST'])
@admin_required
def admin_add_slot():
    area_id = int(request.form.get('area_id'))
    slot_num = request.form.get('slot_number', '').strip().upper()
    floor = request.form.get('floor_level', 'Ground Floor').strip()
    v_type = request.form.get('supported_vehicle_type', 'SEDAN')
    is_ev = 1 if request.form.get('is_ev_charging_equipped') else 0

    try:
        database.execute_query(
            """INSERT INTO Parking_Slots (area_id, slot_number, floor_level, supported_vehicle_type, slot_status, is_ev_charging_equipped)
               VALUES (%s, %s, %s, %s, 'AVAILABLE', %s)""",
            (area_id, slot_num, floor, v_type, is_ev),
            commit=True
        )
        flash(f'Slot {slot_num} created successfully!', 'success')
    except Exception as e:
        flash(f'Failed to create slot: {str(e)}', 'error')
    return redirect(url_for('admin_parking_slots'))

@app.route('/admin/slots/edit/<int:slot_id>', methods=['POST'])
@admin_required
def admin_edit_slot(slot_id):
    slot_num = request.form.get('slot_number', '').strip().upper()
    floor = request.form.get('floor_level', '').strip()
    v_type = request.form.get('supported_vehicle_type')
    status = request.form.get('slot_status')

    try:
        database.execute_query(
            "UPDATE Parking_Slots SET slot_number = %s, floor_level = %s, supported_vehicle_type = %s, slot_status = %s WHERE slot_id = %s",
            (slot_num, floor, v_type, status, slot_id),
            commit=True
        )
        flash(f'Slot {slot_num} updated.', 'success')
    except Exception as e:
        flash(f'Update failed: {str(e)}', 'error')
    return redirect(url_for('admin_parking_slots'))

@app.route('/admin/slots/delete/<int:slot_id>', methods=['POST'])
@admin_required
def admin_delete_slot(slot_id):
    try:
        database.execute_query("DELETE FROM Parking_Slots WHERE slot_id = %s", (slot_id,), commit=True)
        flash('Slot bay removed.', 'success')
    except Exception as e:
        flash(f'Cannot delete slot (active records depend on it): {str(e)}', 'error')
    return redirect(url_for('admin_parking_slots'))

@app.route('/admin/analytics')
@admin_required
def admin_analytics():
    tot_rev = database.execute_query("SELECT COALESCE(SUM(amount), 0) AS c FROM Payments WHERE payment_status = 'SUCCESS'", fetch_one=True)['c']
    month_rev = database.execute_query("SELECT COALESCE(SUM(amount), 0) AS c FROM Payments WHERE payment_status = 'SUCCESS' AND paid_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)", fetch_one=True)['c']
    today_rev = database.execute_query("SELECT COALESCE(SUM(amount), 0) AS c FROM Payments WHERE payment_status = 'SUCCESS' AND DATE(paid_at) = CURRENT_DATE", fetch_one=True)['c']
    aov_rev = database.execute_query("SELECT COALESCE(AVG(amount), 0) AS c FROM Payments WHERE payment_status = 'SUCCESS'", fetch_one=True)['c']

    metrics = {
        'lifetime_rev': float(tot_rev),
        'month_rev': float(month_rev),
        'today_rev': float(today_rev),
        'aov': float(aov_rev)
    }

    # Daily trend
    daily_rows = database.execute_query("""
        SELECT DATE(paid_at) AS pay_date, SUM(amount) AS daily_sum
        FROM Payments
        WHERE payment_status = 'SUCCESS'
        GROUP BY DATE(paid_at)
        ORDER BY pay_date ASC
        LIMIT 7;
    """)
    revenue_days = [str(r['pay_date']) for r in daily_rows]
    revenue_values = [float(r['daily_sum']) for r in daily_rows]

    # Payment methods breakdown
    method_rows = database.execute_query("""
        SELECT payment_method, COUNT(*) AS txn_count, SUM(amount) AS total_sum
        FROM Payments
        WHERE payment_status = 'SUCCESS'
        GROUP BY payment_method;
    """)
    method_labels = [r['payment_method'] for r in method_rows]
    method_values = [float(r['total_sum']) for r in method_rows]

    recent_payments = database.execute_query("""
        SELECT p.*, u.full_name, u.email, r.booking_code
        FROM Payments p
        JOIN Users u ON p.user_id = u.user_id
        LEFT JOIN Reservations r ON p.reservation_id = r.reservation_id
        ORDER BY p.paid_at DESC
        LIMIT 10;
    """)

    return render_template('admin/analytics.html',
                           metrics=metrics,
                           revenue_days=revenue_days,
                           revenue_values=revenue_values,
                           method_labels=method_labels,
                           method_values=method_values,
                           recent_payments=recent_payments)

@app.route('/admin/sql-demo')
@admin_required
def admin_sql_demo():
    # 1. GROUP BY, HAVING, AGGREGATES
    demo_groupby = database.execute_query("""
        SELECT pa.area_name, ps.supported_vehicle_type,
               COUNT(ps.slot_id) AS total_slots,
               SUM(CASE WHEN ps.slot_status = 'AVAILABLE' THEN 1 ELSE 0 END) AS free_slots
        FROM Parking_Areas pa
        INNER JOIN Parking_Slots ps ON pa.area_id = ps.area_id
        GROUP BY pa.area_name, ps.supported_vehicle_type
        HAVING total_slots >= 2
        ORDER BY total_slots DESC;
    """)

    # 2. Relational Multi-Table JOINS
    demo_joins = database.execute_query("""
        SELECT u.full_name, v.license_plate, r.booking_code,
               pa.area_name, s.slot_number, r.estimated_cost
        FROM Reservations r
        INNER JOIN Users u ON r.user_id = u.user_id
        INNER JOIN Vehicles v ON r.vehicle_id = v.vehicle_id
        INNER JOIN Parking_Slots s ON r.slot_id = s.slot_id
        INNER JOIN Parking_Areas pa ON s.area_id = pa.area_id
        WHERE r.booking_status IN ('CONFIRMED', 'CHECKED_IN')
        LIMIT 5;
    """)

    # 3. Subquery
    demo_subquery = database.execute_query("""
        SELECT u.user_id, u.full_name, u.email,
               (SELECT COALESCE(SUM(amount), 0) FROM Payments p WHERE p.user_id = u.user_id) AS total_spent
        FROM Users u
        WHERE (SELECT COALESCE(SUM(amount), 0) FROM Payments p WHERE p.user_id = u.user_id) >
              (SELECT AVG(amount) FROM Payments)
        ORDER BY total_spent DESC;
    """)

    # 4. View Demonstration
    demo_views = database.execute_query("""
        SELECT area_name, supported_vehicle_type, total_slots, available_slots, occupied_slots, base_hourly_rate
        FROM view_available_slots_summary
        WHERE available_slots > 0
        LIMIT 5;
    """)

    return render_template('admin/sql_demo.html',
                           demo_groupby=demo_groupby,
                           demo_joins=demo_joins,
                           demo_subquery=demo_subquery,
                           demo_views=demo_views,
                           db_driver=database.get_active_driver())

# ---------------------------------------------------------------------
# INITIALIZATION & EXECUTION ENTRYPOINT
# ---------------------------------------------------------------------
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"\n==================================================================")
    print(f" SMART PARKING SLOT MANAGEMENT SYSTEM - DBMS ACADEMIC PROJECT")
    print(f" Active Database Driver: {database.get_active_driver()}")
    print(f" Server running at: http://127.0.0.1:{port}")
    print(f" Admin Demo: admin / admin123 | User Demo: aarav.patel@gmail.com / user123")
    print(f"==================================================================\n")
    app.run(host='0.0.0.0', port=port, debug=True)
