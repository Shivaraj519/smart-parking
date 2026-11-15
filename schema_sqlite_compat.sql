-- =====================================================================
-- SMART PARKING SLOT MANAGEMENT SYSTEM - DATABASE SCHEMA
-- DBMS Academic Project: Smart Parking System
-- =====================================================================





-- ---------------------------------------------------------------------
-- TABLE 1: Users
-- Stores registered driver/customer information
-- ---------------------------------------------------------------------
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    license_number VARCHAR(50) UNIQUE,
    wallet_balance DECIMAL(10,2) DEFAULT 500.00 CHECK (wallet_balance >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ;

-- ---------------------------------------------------------------------
-- TABLE 2: Admins
-- Stores administrative personnel credentials and privileges
-- ---------------------------------------------------------------------
CREATE TABLE Admins (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role TEXT DEFAULT 'OPERATOR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ;

-- ---------------------------------------------------------------------
-- TABLE 3: Parking_Areas
-- Represents distinct physical parking facilities, lots, or multi-level garages
-- ---------------------------------------------------------------------
CREATE TABLE Parking_Areas (
    area_id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_name VARCHAR(100) NOT NULL UNIQUE,
    location_address VARCHAR(255) NOT NULL,
    total_capacity INT NOT NULL CHECK (total_capacity > 0),
    operating_status TEXT DEFAULT 'OPEN',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ;

-- ---------------------------------------------------------------------
-- TABLE 4: Pricing
-- Configurable hourly tariffs per vehicle category and parking area
-- ---------------------------------------------------------------------
CREATE TABLE Pricing (
    pricing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_id INT NOT NULL,
    vehicle_type TEXT NOT NULL,
    base_hourly_rate DECIMAL(8,2) NOT NULL CHECK (base_hourly_rate >= 0),
    grace_period_mins INT DEFAULT 15 CHECK (grace_period_mins >= 0),
    overstay_penalty_rate DECIMAL(8,2) DEFAULT 50.00 CHECK (overstay_penalty_rate >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pricing_area FOREIGN KEY (area_id) 
        REFERENCES Parking_Areas(area_id) ON DELETE CASCADE,
    CONSTRAINT uq_area_vehicletype UNIQUE (area_id, vehicle_type)
) ;

-- ---------------------------------------------------------------------
-- TABLE 5: Parking_Slots
-- Unique spatial parking bays within an area
-- ---------------------------------------------------------------------
CREATE TABLE Parking_Slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_id INT NOT NULL,
    slot_number VARCHAR(20) NOT NULL,
    floor_level VARCHAR(20) DEFAULT 'Ground Floor',
    supported_vehicle_type TEXT NOT NULL,
    slot_status TEXT DEFAULT 'AVAILABLE',
    is_ev_charging_equipped INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_slots_area FOREIGN KEY (area_id) 
        REFERENCES Parking_Areas(area_id) ON DELETE CASCADE,
    CONSTRAINT uq_area_slot UNIQUE (area_id, slot_number)
) ;

-- ---------------------------------------------------------------------
-- TABLE 6: Vehicles
-- Vehicles registered by users
-- ---------------------------------------------------------------------
CREATE TABLE Vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT NOT NULL,
    license_plate VARCHAR(30) NOT NULL UNIQUE,
    vehicle_type TEXT NOT NULL,
    make_model VARCHAR(100),
    color VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_vehicles_user FOREIGN KEY (user_id) 
        REFERENCES Users(user_id) ON DELETE CASCADE
) ;

-- ---------------------------------------------------------------------
-- TABLE 7: Reservations
-- Slot booking records with time windows and lifecycle states
-- ---------------------------------------------------------------------
CREATE TABLE Reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    slot_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    estimated_cost DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    booking_status TEXT DEFAULT 'CONFIRMED',
    booking_code VARCHAR(12) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_res_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_res_vehicle FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id) ON DELETE RESTRICT,
    CONSTRAINT fk_res_slot FOREIGN KEY (slot_id) REFERENCES Parking_Slots(slot_id) ON DELETE RESTRICT,
    CONSTRAINT chk_time_window CHECK (end_time > start_time)
) ;

-- ---------------------------------------------------------------------
-- TABLE 8: Parking_Sessions
-- Physical entry/exit tracking linked to reservation or drive-in
-- ---------------------------------------------------------------------
CREATE TABLE Parking_Sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation_id INT UNIQUE,
    slot_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    entry_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exit_time DATETIME NULL,
    duration_minutes INT DEFAULT NULL,
    calculated_amount DECIMAL(10,2) DEFAULT 0.00,
    session_status TEXT DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sess_res FOREIGN KEY (reservation_id) REFERENCES Reservations(reservation_id) ON DELETE SET NULL,
    CONSTRAINT fk_sess_slot FOREIGN KEY (slot_id) REFERENCES Parking_Slots(slot_id) ON DELETE RESTRICT,
    CONSTRAINT fk_sess_veh FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id) ON DELETE RESTRICT
) ;

-- ---------------------------------------------------------------------
-- TABLE 9: Payments
-- Financial transaction ledger verifying settlement of charges
-- ---------------------------------------------------------------------
CREATE TABLE Payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INT NULL,
    reservation_id INT NULL,
    user_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0),
    payment_method TEXT DEFAULT 'WALLET',
    payment_status TEXT DEFAULT 'SUCCESS',
    transaction_reference VARCHAR(64) NOT NULL UNIQUE,
    paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pay_session FOREIGN KEY (session_id) REFERENCES Parking_Sessions(session_id) ON DELETE SET NULL,
    CONSTRAINT fk_pay_res FOREIGN KEY (reservation_id) REFERENCES Reservations(reservation_id) ON DELETE SET NULL,
    CONSTRAINT fk_pay_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
) ;

-- ---------------------------------------------------------------------
-- PERFORMANCE & QUERY INDEXES
-- ---------------------------------------------------------------------
CREATE INDEX idx_slot_lookup ON Parking_Slots(area_id, supported_vehicle_type, slot_status);
CREATE INDEX idx_res_window ON Reservations(slot_id, start_time, end_time, booking_status);
CREATE INDEX idx_user_reservations ON Reservations(user_id, created_at);
CREATE INDEX idx_active_sessions ON Parking_Sessions(session_status, entry_time);
CREATE INDEX idx_payments_date ON Payments(paid_at, payment_status);

-- ---------------------------------------------------------------------
-- DATABASE VIEWS
-- ---------------------------------------------------------------------

-- View 1: Real-time Slot Availability Overview
CREATE OR REPLACE VIEW view_available_slots_summary AS
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
GROUP BY pa.area_id, pa.area_name, pa.location_address, ps.supported_vehicle_type, pr.base_hourly_rate;

-- View 2: Detailed Active Sessions with Vehicle and Slot Info
CREATE OR REPLACE VIEW view_active_parking_sessions AS
SELECT 
    s.session_id,
    s.entry_time,
    TIMESTAMPDIFF(MINUTE, s.entry_time, datetime('now')) AS current_duration_mins,
    v.license_plate,
    v.vehicle_type,
    v.make_model,
    u.user_id,
    u.full_name AS driver_name,
    u.phone_number,
    pa.area_name,
    sl.slot_number,
    sl.floor_level,
    pr.base_hourly_rate,
    ROUND(
        (CEIL(GREATEST(TIMESTAMPDIFF(MINUTE, s.entry_time, datetime('now')), 1) / 60.0)) * pr.base_hourly_rate, 
        2
    ) AS estimated_accrued_charge
FROM Parking_Sessions s
JOIN Parking_Slots sl ON s.slot_id = sl.slot_id
JOIN Parking_Areas pa ON sl.area_id = pa.area_id
JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
JOIN Users u ON v.user_id = u.user_id
LEFT JOIN Pricing pr ON pa.area_id = pr.area_id AND v.vehicle_type = pr.vehicle_type
WHERE s.session_status = 'ACTIVE';

-- View 3: Complete Billing & Financial Audit Trail
CREATE OR REPLACE VIEW view_payment_audit_trail AS
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
LEFT JOIN Parking_Sessions s ON p.session_id = s.session_id;

-- ---------------------------------------------------------------------
-- DATABASE TRIGGERS
-- ---------------------------------------------------------------------

