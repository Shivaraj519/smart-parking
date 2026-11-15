# SMART PARKING SLOT MANAGEMENT SYSTEM
## Database Management System (DBMS) Academic Mini-Project

An enterprise-grade, high-performance DBMS mini-project built with **Python Flask**, **MySQL**, and **Chart.js**, designed to demonstrate practical relational database principles: 3NF normalization, ACID transaction processing, concurrency isolation (`SELECT ... FOR UPDATE`), triggers, stored procedures, database views, and relational algebra operations.

---

### Key Architectural Highlights

1. **Relational Database Foundation**:
   - 9 interconnected entities: `Users`, `Admins`, `Parking_Areas`, `Pricing`, `Parking_Slots`, `Vehicles`, `Reservations`, `Parking_Sessions`, `Payments`.
   - Strict 3rd Normal Form (3NF) design eliminating insertion, update, and deletion anomalies.
   - Comprehensive constraints: `PRIMARY KEY`, `FOREIGN KEY` (`ON DELETE CASCADE`/`RESTRICT`), `UNIQUE`, `NOT NULL`, and `CHECK`.

2. **Concurrency & Double-Booking Elimination**:
   - Atomic reservation procedure using database locks (`SELECT ... FOR UPDATE`).
   - Strict time-window overlap validation preventing simultaneous collision reservations.

3. **Database Automation**:
   - **Triggers**: Auto-updates slot status (`AVAILABLE` &rarr; `RESERVED` &rarr; `OCCUPIED` &rarr; `AVAILABLE`), auto-calculates session duration, updates driver wallet ledger.
   - **Stored Procedures**: `sp_reserve_parking_slot`, `sp_process_vehicle_entry`, `sp_process_vehicle_exit`.
   - **Views**: `view_available_slots_summary`, `view_active_parking_sessions`, `view_payment_audit_trail`.

4. **Academic Demonstration Laboratory**:
   - In-app interactive showcase of `INNER JOIN`, `LEFT JOIN`, `GROUP BY`, `HAVING`, Aggregate Functions (`COUNT`, `SUM`, `AVG`), Correlated Subqueries, and Views.

---

### Technology Stack

- **Frontend**: HTML5, Modern CSS3 Design System (Warm cream aesthetic, charcoal typography, forest green accents), JavaScript, Bootstrap 5, Chart.js
- **Backend**: Python 3.10+ Flask
- **Database Engine**: MySQL 8.0+ (with automated portable fallback engine)
- **Database Connector**: `mysql-connector-python`

---

### Default Demonstration Credentials

| Role | Username / Email | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin` | `admin123` | Full control over areas, slots, tariffs, check-out, analytics |
| **Driver / User** | `aarav.patel@gmail.com` | `user123` | Vehicles, live visual bay booking, cancellation, wallet |
| **Driver / User** | `aditi.sharma@yahoo.com` | `user123` | Multi-vehicle driver with existing booking history |

---

### Quick Setup & Execution Instructions

#### 1. Install Dependencies
```bash
cd smart_parking
pip install -r requirements.txt
```

#### 2. Initialize Database & Sample Data
To populate your MySQL server with the schema, triggers, stored procedures, and 20+ users, 25+ vehicles, and 30+ slots:
```bash
# If your MySQL root has a password:
python init_db.py your_mysql_password root

# Or load schema.sql and sample_data.sql directly in MySQL Workbench / CLI:
# mysql -u root -p < schema.sql
# mysql -u root -p smart_parking_db < sample_data.sql
```

*(Note: If MySQL credentials are not provided or server is offline, the project automatically initializes its embedded database engine with full transaction support so you can evaluate the project immediately).*

#### 3. Run the Application
```bash
python app.py
```
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

### Project File Structure

```text
smart_parking/
├── app.py                      # Flask main application & REST controllers
├── database.py                 # MySQL connection pooling, ACID transaction handlers & fallback
├── db.py                       # Database connection helper
├── init_db.py                  # Automated MySQL schema & sample data populator
├── schema.sql                  # Complete MySQL DDL, Views, Triggers, & Stored Procedures
├── sample_data.sql             # 20+ Users, 25+ Vehicles, 3 Areas, 37 Slots, Transactions
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── static/
│   ├── css/
│   │   └── style.css           # Premium minimalist warm-cream design system
│   └── js/
└── templates/
    ├── base.html               # Master layout with responsive navbar & alerts
    ├── index.html              # Landing page with live metrics
    ├── login.html              # User login
    ├── register.html           # User registration & wallet funding
    ├── admin_login.html        # Admin console login
    ├── parking_availability.html # Interactive visual bay grid (Green/Yellow/Red)
    ├── user/
    │   ├── dashboard.html      # Driver control panel & barrier check-in
    │   ├── vehicles.html       # Vehicle management
    │   ├── reserve.html        # ACID booking form with time-window picker
    │   ├── confirmation.html   # Booking pass confirmation
    │   ├── history.html        # Historical reservation audit trail
    │   └── payments.html       # Financial ledger & transactions
    └── admin/
        ├── dashboard.html      # Admin KPI console & live sessions
        ├── parking_areas.html  # Facility management CRUD
        ├── parking_slots.html  # Bay inventory CRUD & EV dock toggles
        ├── analytics.html      # Chart.js revenue & occupancy charts
        └── sql_demo.html       # DBMS & SQL demonstration laboratory
```
