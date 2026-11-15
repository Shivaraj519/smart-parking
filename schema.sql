-- =====================================================================
-- SMART PARKING SLOT MANAGEMENT SYSTEM - DATABASE SCHEMA
-- DBMS Academic Project: Smart Parking System
-- =====================================================================

DROP DATABASE IF EXISTS smart_parking_db;
CREATE DATABASE smart_parking_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smart_parking_db;

-- ---------------------------------------------------------------------
-- TABLE 1: Users
-- Stores registered driver/customer information
-- ---------------------------------------------------------------------
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    license_number VARCHAR(50) UNIQUE,
    wallet_balance DECIMAL(10,2) DEFAULT 500.00 CHECK (wallet_balance >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABLE 2: Admins
-- Stores administrative personnel credentials and privileges
-- ---------------------------------------------------------------------
CREATE TABLE Admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('SUPERADMIN', 'OPERATOR', 'AUDITOR') DEFAULT 'OPERATOR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABLE 3: Parking_Areas
-- Represents distinct physical parking facilities, lots, or multi-level garages
-- ---------------------------------------------------------------------
CREATE TABLE Parking_Areas (
    area_id INT AUTO_INCREMENT PRIMARY KEY,
    area_name VARCHAR(100) NOT NULL UNIQUE,
    location_address VARCHAR(255) NOT NULL,
    total_capacity INT NOT NULL CHECK (total_capacity > 0),
    operating_status ENUM('OPEN', 'CLOSED', 'MAINTENANCE') DEFAULT 'OPEN',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABLE 4: Pricing
-- Configurable hourly tariffs per vehicle category and parking area
-- ---------------------------------------------------------------------
CREATE TABLE Pricing (
    pricing_id INT AUTO_INCREMENT PRIMARY KEY,
    area_id INT NOT NULL,
    vehicle_type ENUM('TWO_WHEELER', 'SEDAN', 'SUV', 'ELECTRIC_VEHICLE', 'TRUCK') NOT NULL,
    base_hourly_rate DECIMAL(8,2) NOT NULL CHECK (base_hourly_rate >= 0),
    grace_period_mins INT DEFAULT 15 CHECK (grace_period_mins >= 0),
    overstay_penalty_rate DECIMAL(8,2) DEFAULT 50.00 CHECK (overstay_penalty_rate >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pricing_area FOREIGN KEY (area_id) 
        REFERENCES Parking_Areas(area_id) ON DELETE CASCADE,
    CONSTRAINT uq_area_vehicletype UNIQUE (area_id, vehicle_type)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABLE 5: Parking_Slots
-- Unique spatial parking bays within an area
-- ---------------------------------------------------------------------
CREATE TABLE Parking_Slots (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    area_id INT NOT NULL,
    slot_number VARCHAR(20) NOT NULL,
    floor_level VARCHAR(20) DEFAULT 'Ground Floor',
    supported_vehicle_type ENUM('TWO_WHEELER', 'SEDAN', 'SUV', 'ELECTRIC_VEHICLE', 'TRUCK') NOT NULL,
    slot_status ENUM('AVAILABLE', 'RESERVED', 'OCCUPIED', 'UNDER_MAINTENANCE') DEFAULT 'AVAILABLE',
    is_ev_charging_equipped BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_slots_area FOREIGN KEY (area_id) 
        REFERENCES Parking_Areas(area_id) ON DELETE CASCADE,
    CONSTRAINT uq_area_slot UNIQUE (area_id, slot_number)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABLE 6: Vehicles
-- Vehicles registered by users
-- ---------------------------------------------------------------------
CREATE TABLE Vehicles (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    license_plate VARCHAR(30) NOT NULL UNIQUE,
    vehicle_type ENUM('TWO_WHEELER', 'SEDAN', 'SUV', 'ELECTRIC_VEHICLE', 'TRUCK') NOT NULL,
    make_model VARCHAR(100),
    color VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_vehicles_user FOREIGN KEY (user_id) 
        REFERENCES Users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABLE 7: Reservations
-- Slot booking records with time windows and lifecycle states
-- ---------------------------------------------------------------------
CREATE TABLE Reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    slot_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    estimated_cost DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    booking_status ENUM('PENDING', 'CONFIRMED', 'CHECKED_IN', 'COMPLETED', 'CANCELLED') DEFAULT 'CONFIRMED',
    booking_code VARCHAR(12) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_res_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_res_vehicle FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id) ON DELETE RESTRICT,
    CONSTRAINT fk_res_slot FOREIGN KEY (slot_id) REFERENCES Parking_Slots(slot_id) ON DELETE RESTRICT,
    CONSTRAINT chk_time_window CHECK (end_time > start_time)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABLE 8: Parking_Sessions
-- Physical entry/exit tracking linked to reservation or drive-in
-- ---------------------------------------------------------------------
CREATE TABLE Parking_Sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT UNIQUE,
    slot_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    entry_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exit_time DATETIME NULL,
    duration_minutes INT DEFAULT NULL,
    calculated_amount DECIMAL(10,2) DEFAULT 0.00,
    session_status ENUM('ACTIVE', 'COMPLETED') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sess_res FOREIGN KEY (reservation_id) REFERENCES Reservations(reservation_id) ON DELETE SET NULL,
    CONSTRAINT fk_sess_slot FOREIGN KEY (slot_id) REFERENCES Parking_Slots(slot_id) ON DELETE RESTRICT,
    CONSTRAINT fk_sess_veh FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- TABLE 9: Payments
-- Financial transaction ledger verifying settlement of charges
-- ---------------------------------------------------------------------
CREATE TABLE Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NULL,
    reservation_id INT NULL,
    user_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0),
    payment_method ENUM('WALLET', 'CREDIT_CARD', 'DEBIT_CARD', 'UPI', 'CASH') DEFAULT 'WALLET',
    payment_status ENUM('PENDING', 'SUCCESS', 'FAILED', 'REFUNDED') DEFAULT 'SUCCESS',
    transaction_reference VARCHAR(64) NOT NULL UNIQUE,
    paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pay_session FOREIGN KEY (session_id) REFERENCES Parking_Sessions(session_id) ON DELETE SET NULL,
    CONSTRAINT fk_pay_res FOREIGN KEY (reservation_id) REFERENCES Reservations(reservation_id) ON DELETE SET NULL,
    CONSTRAINT fk_pay_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

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
    TIMESTAMPDIFF(MINUTE, s.entry_time, NOW()) AS current_duration_mins,
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
        (CEIL(GREATEST(TIMESTAMPDIFF(MINUTE, s.entry_time, NOW()), 1) / 60.0)) * pr.base_hourly_rate, 
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

DELIMITER $$

-- Trigger 1: After Reservation Inserted -> Mark Slot as RESERVED
CREATE TRIGGER trg_after_reservation_insert
AFTER INSERT ON Reservations
FOR EACH ROW
BEGIN
    IF NEW.booking_status = 'CONFIRMED' THEN
        UPDATE Parking_Slots 
        SET slot_status = 'RESERVED' 
        WHERE slot_id = NEW.slot_id;
    END IF;
END$$

-- Trigger 2: After Reservation Updated (e.g. Cancelled/Completed) -> Free Slot if not occupied
CREATE TRIGGER trg_after_reservation_update
AFTER UPDATE ON Reservations
FOR EACH ROW
BEGIN
    IF NEW.booking_status = 'CANCELLED' AND OLD.booking_status = 'CONFIRMED' THEN
        -- Only set AVAILABLE if slot is currently marked RESERVED
        UPDATE Parking_Slots 
        SET slot_status = 'AVAILABLE' 
        WHERE slot_id = NEW.slot_id AND slot_status = 'RESERVED';
    END IF;
END$$

-- Trigger 3: After Parking Session Inserted (Vehicle Entry) -> Mark Slot OCCUPIED
CREATE TRIGGER trg_after_session_insert
AFTER INSERT ON Parking_Sessions
FOR EACH ROW
BEGIN
    UPDATE Parking_Slots 
    SET slot_status = 'OCCUPIED' 
    WHERE slot_id = NEW.slot_id;

    IF NEW.reservation_id IS NOT NULL THEN
        UPDATE Reservations
        SET booking_status = 'CHECKED_IN'
        WHERE reservation_id = NEW.reservation_id;
    END IF;
END$$

-- Trigger 4: After Parking Session Updated (Vehicle Exit) -> Mark Slot AVAILABLE & Auto-calculate duration
CREATE TRIGGER trg_before_session_update
BEFORE UPDATE ON Parking_Sessions
FOR EACH ROW
BEGIN
    IF NEW.session_status = 'COMPLETED' AND OLD.session_status = 'ACTIVE' THEN
        IF NEW.exit_time IS NULL THEN
            SET NEW.exit_time = NOW();
        END IF;
        SET NEW.duration_minutes = TIMESTAMPDIFF(MINUTE, OLD.entry_time, NEW.exit_time);
    END IF;
END$$

CREATE TRIGGER trg_after_session_completed
AFTER UPDATE ON Parking_Sessions
FOR EACH ROW
BEGIN
    IF NEW.session_status = 'COMPLETED' AND OLD.session_status = 'ACTIVE' THEN
        UPDATE Parking_Slots 
        SET slot_status = 'AVAILABLE' 
        WHERE slot_id = NEW.slot_id;

        IF NEW.reservation_id IS NOT NULL THEN
            UPDATE Reservations
            SET booking_status = 'COMPLETED'
            WHERE reservation_id = NEW.reservation_id;
        END IF;
    END IF;
END$$

-- Trigger 5: Wallet deduction and balance protection on Payment
CREATE TRIGGER trg_after_payment_success
AFTER INSERT ON Payments
FOR EACH ROW
BEGIN
    IF NEW.payment_status = 'SUCCESS' AND NEW.payment_method = 'WALLET' THEN
        UPDATE Users 
        SET wallet_balance = wallet_balance - NEW.amount 
        WHERE user_id = NEW.user_id;
    END IF;
END$$

DELIMITER ;

-- ---------------------------------------------------------------------
-- STORED PROCEDURES
-- ---------------------------------------------------------------------

DELIMITER $$

-- Procedure 1: Safe Concurrency-Controlled Slot Reservation with Double-Booking Prevention
CREATE PROCEDURE sp_reserve_parking_slot(
    IN p_user_id INT,
    IN p_vehicle_id INT,
    IN p_slot_id INT,
    IN p_start_time DATETIME,
    IN p_end_time DATETIME,
    IN p_payment_method VARCHAR(20),
    OUT p_reservation_id INT,
    OUT p_booking_code VARCHAR(12),
    OUT p_total_amount DECIMAL(10,2),
    OUT p_status_message VARCHAR(255)
)
proc_label: BEGIN
    DECLARE v_slot_status VARCHAR(20);
    DECLARE v_area_id INT;
    DECLARE v_veh_type VARCHAR(30);
    DECLARE v_slot_type VARCHAR(30);
    DECLARE v_hourly_rate DECIMAL(8,2) DEFAULT 30.00;
    DECLARE v_hours DECIMAL(6,2);
    DECLARE v_overlap_count INT DEFAULT 0;
    DECLARE v_wallet DECIMAL(10,2) DEFAULT 0.00;
    DECLARE v_code VARCHAR(12);

    -- Declare error handler for rollbacks
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_reservation_id = 0;
        SET p_booking_code = '';
        SET p_total_amount = 0.00;
        SET p_status_message = 'ERROR: Database transaction failed during booking.';
    END;

    START TRANSACTION;

    -- Step 1: Validate vehicle ownership & type
    SELECT vehicle_type INTO v_veh_type 
    FROM Vehicles 
    WHERE vehicle_id = p_vehicle_id AND user_id = p_user_id;

    IF v_veh_type IS NULL THEN
        ROLLBACK;
        SET p_reservation_id = 0;
        SET p_status_message = 'ERROR: Vehicle not registered or does not belong to user.';
        LEAVE proc_label;
    END IF;

    -- Step 2: Concurrency lock on target slot using SELECT ... FOR UPDATE
    SELECT area_id, slot_status, supported_vehicle_type 
    INTO v_area_id, v_slot_status, v_slot_type
    FROM Parking_Slots 
    WHERE slot_id = p_slot_id
    FOR UPDATE;

    IF v_slot_status IS NULL THEN
        ROLLBACK;
        SET p_reservation_id = 0;
        SET p_status_message = 'ERROR: Selected parking slot does not exist.';
        LEAVE proc_label;
    END IF;

    IF v_slot_status = 'UNDER_MAINTENANCE' THEN
        ROLLBACK;
        SET p_reservation_id = 0;
        SET p_status_message = 'ERROR: Slot is currently under maintenance.';
        LEAVE proc_label;
    END IF;

    IF v_slot_type != v_veh_type THEN
        ROLLBACK;
        SET p_reservation_id = 0;
        SET p_status_message = CONCAT('ERROR: Slot type (', v_slot_type, ') does not match vehicle (', v_veh_type, ').');
        LEAVE proc_label;
    END IF;

    -- Step 3: Check for overlapping reservations for this slot (Strict Concurrency Check)
    SELECT COUNT(*) INTO v_overlap_count
    FROM Reservations
    WHERE slot_id = p_slot_id
      AND booking_status IN ('CONFIRMED', 'CHECKED_IN')
      AND (
          (p_start_time >= start_time AND p_start_time < end_time) OR
          (p_end_time > start_time AND p_end_time <= end_time) OR
          (p_start_time <= start_time AND p_end_time >= end_time)
      );

    IF v_overlap_count > 0 THEN
        ROLLBACK;
        SET p_reservation_id = 0;
        SET p_status_message = 'ERROR: Slot already reserved for the selected time window.';
        LEAVE proc_label;
    END IF;

    -- Step 4: Fetch pricing tariff
    SELECT base_hourly_rate INTO v_hourly_rate
    FROM Pricing
    WHERE area_id = v_area_id AND vehicle_type = v_veh_type
    LIMIT 1;

    -- Calculate fee (minimum 1 hour)
    SET v_hours = CEIL(TIMESTAMPDIFF(MINUTE, p_start_time, p_end_time) / 60.0);
    IF v_hours < 1 THEN SET v_hours = 1; END IF;
    SET p_total_amount = v_hours * v_hourly_rate;

    -- Step 5: Check wallet balance if paying via WALLET
    IF p_payment_method = 'WALLET' THEN
        SELECT wallet_balance INTO v_wallet FROM Users WHERE user_id = p_user_id;
        IF v_wallet < p_total_amount THEN
            ROLLBACK;
            SET p_reservation_id = 0;
            SET p_status_message = CONCAT('ERROR: Insufficient wallet balance. Required: ₹', p_total_amount, ', Available: ₹', v_wallet);
            LEAVE proc_label;
        END IF;
    END IF;

    -- Step 6: Generate unique booking reference code (e.g. PK-8F92D1)
    SET v_code = CONCAT('PK-', UPPER(SUBSTRING(MD5(CONCAT(p_user_id, p_slot_id, NOW(), RAND())), 1, 6)));
    SET p_booking_code = v_code;

    -- Step 7: Insert Reservation record
    INSERT INTO Reservations (
        user_id, vehicle_id, slot_id, start_time, end_time, estimated_cost, booking_status, booking_code
    ) VALUES (
        p_user_id, p_vehicle_id, p_slot_id, p_start_time, p_end_time, p_total_amount, 'CONFIRMED', v_code
    );
    SET p_reservation_id = LAST_INSERT_ID();

    -- Step 8: Insert initial Payment record
    INSERT INTO Payments (
        reservation_id, user_id, amount, payment_method, payment_status, transaction_reference
    ) VALUES (
        p_reservation_id, p_user_id, p_total_amount, p_payment_method, 'SUCCESS', 
        CONCAT('TXN-', UPPER(SUBSTRING(MD5(CONCAT(v_code, RAND())), 1, 12)))
    );

    COMMIT;
    SET p_status_message = 'SUCCESS: Slot reservation confirmed successfully!';
END$$

-- Procedure 2: Vehicle Check-In (Converts Reservation into Active Parking Session)
CREATE PROCEDURE sp_process_vehicle_entry(
    IN p_booking_code VARCHAR(12),
    OUT p_session_id INT,
    OUT p_status_message VARCHAR(255)
)
proc_label: BEGIN
    DECLARE v_res_id INT;
    DECLARE v_slot_id INT;
    DECLARE v_vehicle_id INT;
    DECLARE v_status VARCHAR(20);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_session_id = 0;
        SET p_status_message = 'ERROR: Database error occurred during check-in.';
    END;

    START TRANSACTION;

    SELECT reservation_id, slot_id, vehicle_id, booking_status
    INTO v_res_id, v_slot_id, v_vehicle_id, v_status
    FROM Reservations
    WHERE booking_code = p_booking_code
    FOR UPDATE;

    IF v_res_id IS NULL THEN
        ROLLBACK;
        SET p_session_id = 0;
        SET p_status_message = 'ERROR: Invalid booking reference code.';
        LEAVE proc_label;
    END IF;

    IF v_status != 'CONFIRMED' THEN
        ROLLBACK;
        SET p_session_id = 0;
        SET p_status_message = CONCAT('ERROR: Booking is in ', v_status, ' state. Cannot check in.');
        LEAVE proc_label;
    END IF;

    INSERT INTO Parking_Sessions (reservation_id, slot_id, vehicle_id, entry_time, session_status)
    VALUES (v_res_id, v_slot_id, v_vehicle_id, NOW(), 'ACTIVE');
    SET p_session_id = LAST_INSERT_ID();

    COMMIT;
    SET p_status_message = 'SUCCESS: Vehicle checked in. Slot marked as OCCUPIED.';
END$$

-- Procedure 3: Vehicle Check-Out & Final Bill Settlement
CREATE PROCEDURE sp_process_vehicle_exit(
    IN p_session_id INT,
    IN p_payment_method VARCHAR(20),
    OUT p_final_amount DECIMAL(10,2),
    OUT p_duration_mins INT,
    OUT p_status_message VARCHAR(255)
)
proc_label: BEGIN
    DECLARE v_res_id INT;
    DECLARE v_slot_id INT;
    DECLARE v_veh_id INT;
    DECLARE v_user_id INT;
    DECLARE v_area_id INT;
    DECLARE v_veh_type VARCHAR(30);
    DECLARE v_entry_time DATETIME;
    DECLARE v_hourly_rate DECIMAL(8,2) DEFAULT 30.00;
    DECLARE v_initial_paid DECIMAL(10,2) DEFAULT 0.00;
    DECLARE v_additional_due DECIMAL(10,2) DEFAULT 0.00;
    DECLARE v_billable_hours DECIMAL(6,2);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_final_amount = 0.00;
        SET p_duration_mins = 0;
        SET p_status_message = 'ERROR: Database error occurred during checkout.';
    END;

    START TRANSACTION;

    SELECT s.reservation_id, s.slot_id, s.vehicle_id, s.entry_time, sl.area_id, v.vehicle_type, v.user_id
    INTO v_res_id, v_slot_id, v_veh_id, v_entry_time, v_area_id, v_veh_type, v_user_id
    FROM Parking_Sessions s
    JOIN Parking_Slots sl ON s.slot_id = sl.slot_id
    JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
    WHERE s.session_id = p_session_id AND s.session_status = 'ACTIVE'
    FOR UPDATE;

    IF v_slot_id IS NULL THEN
        ROLLBACK;
        SET p_final_amount = 0.00;
        SET p_duration_mins = 0;
        SET p_status_message = 'ERROR: Active session not found for provided ID.';
        LEAVE proc_label;
    END IF;

    -- Calculate duration
    SET p_duration_mins = TIMESTAMPDIFF(MINUTE, v_entry_time, NOW());
    IF p_duration_mins <= 0 THEN SET p_duration_mins = 1; END IF;

    -- Fetch rate
    SELECT base_hourly_rate INTO v_hourly_rate
    FROM Pricing
    WHERE area_id = v_area_id AND vehicle_type = v_veh_type
    LIMIT 1;

    SET v_billable_hours = CEIL(p_duration_mins / 60.0);
    IF v_billable_hours < 1 THEN SET v_billable_hours = 1; END IF;
    SET p_final_amount = v_billable_hours * v_hourly_rate;

    -- Check what was already paid at booking
    IF v_res_id IS NOT NULL THEN
        SELECT COALESCE(SUM(amount), 0) INTO v_initial_paid
        FROM Payments
        WHERE reservation_id = v_res_id AND payment_status = 'SUCCESS';
    END IF;

    IF p_final_amount > v_initial_paid THEN
        SET v_additional_due = p_final_amount - v_initial_paid;
        -- Record incremental charge
        INSERT INTO Payments (
            session_id, user_id, amount, payment_method, payment_status, transaction_reference
        ) VALUES (
            p_session_id, v_user_id, v_additional_due, p_payment_method, 'SUCCESS',
            CONCAT('OVERSTAY-', UPPER(SUBSTRING(MD5(CONCAT(p_session_id, NOW())), 1, 10)))
        );
    END IF;

    -- Complete session
    UPDATE Parking_Sessions
    SET session_status = 'COMPLETED',
        exit_time = NOW(),
        duration_minutes = p_duration_mins,
        calculated_amount = p_final_amount
    WHERE session_id = p_session_id;

    COMMIT;
    SET p_status_message = CONCAT('SUCCESS: Checkout completed. Duration: ', p_duration_mins, ' mins. Total: ₹', p_final_amount);
END$$

DELIMITER ;
