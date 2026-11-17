-- =====================================================================
-- SMART PARKING SLOT MANAGEMENT SYSTEM - SAMPLE DATA
-- 20+ Users, 25+ Vehicles, 3 Parking Areas, 30+ Slots, Pricing,
-- Active/Past Reservations, Active/Completed Sessions, Payments
-- =====================================================================

USE smart_parking_db;

-- ---------------------------------------------------------------------
-- 1. Admins (Default password: admin123)
-- ---------------------------------------------------------------------
INSERT INTO Admins (username, full_name, email, password_hash, role) VALUES
('admin', 'Dr. Rajesh Rao', 'admin@smartparking.edu', 'scrypt:32768:8:1$nhal1ZzlmU4UCNEo$66d42f7bccf0eb466fa651a916544211141cf30db93c5aa6cab0aeea7ddbf56bf210c24aa27a83b1166bec7953408c81fa24b6316677cfa9a15f6cdda3c865dc', 'SUPERADMIN'),
('operator1', 'Sunil Kumar', 'sunil@smartparking.edu', 'scrypt:32768:8:1$nhal1ZzlmU4UCNEo$66d42f7bccf0eb466fa651a916544211141cf30db93c5aa6cab0aeea7ddbf56bf210c24aa27a83b1166bec7953408c81fa24b6316677cfa9a15f6cdda3c865dc', 'OPERATOR'),
('auditor', 'Priya Sharma', 'priya.audit@smartparking.edu', 'scrypt:32768:8:1$nhal1ZzlmU4UCNEo$66d42f7bccf0eb466fa651a916544211141cf30db93c5aa6cab0aeea7ddbf56bf210c24aa27a83b1166bec7953408c81fa24b6316677cfa9a15f6cdda3c865dc', 'AUDITOR');

-- ---------------------------------------------------------------------
-- 2. Users (20 Users, Default password: user123)
-- ---------------------------------------------------------------------
INSERT INTO Users (user_id, full_name, email, phone_number, password_hash, license_number, wallet_balance) VALUES
(1, 'Aarav Patel', 'aarav.patel@gmail.com', '9876543210', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA01-20210001234', 1500.00),
(2, 'Aditi Sharma', 'aditi.sharma@yahoo.com', '9876543211', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA02-20200002345', 850.00),
(3, 'Rohan Verma', 'rohan.verma@outlook.com', '9876543212', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA03-20190003456', 2200.00),
(4, 'Sneha Kulkarni', 'sneha.k@gmail.com', '9876543213', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA04-20220004567', 420.00),
(5, 'Vikram Malhotra', 'vikram.m@gmail.com', '9876543214', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA05-20180005678', 1950.00),
(6, 'Ananya Deshmukh', 'ananya.d@gmail.com', '9876543215', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA06-20210006789', 310.00),
(7, 'Karthik Iyer', 'karthik.iyer@hotmail.com', '9876543216', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA07-20200007890', 600.00),
(8, 'Meera Nair', 'meera.nair@gmail.com', '9876543217', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA08-20220008901', 1250.00),
(9, 'Rahul Joshi', 'rahul.joshi@gmail.com', '9876543218', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA09-20190009012', 780.00),
(10, 'Pooja Reddy', 'pooja.reddy@gmail.com', '9876543219', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA10-20210010123', 950.00),
(11, 'Siddharth Hegde', 'siddharth.h@gmail.com', '9876543220', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA11-20200011234', 1100.00),
(12, 'Divya Pillai', 'divya.p@gmail.com', '9876543221', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA12-20220012345', 490.00),
(13, 'Nikhil Choudhary', 'nikhil.c@gmail.com', '9876543222', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA13-20180013456', 2500.00),
(14, 'Tanvi Sen', 'tanvi.sen@gmail.com', '9876543223', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA14-20210014567', 670.00),
(15, 'Arjun Menon', 'arjun.menon@gmail.com', '9876543224', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA15-20190015678', 1800.00),
(16, 'Ritu Gupta', 'ritu.gupta@gmail.com', '9876543225', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA16-20230016789', 540.00),
(17, 'Gaurav Bhat', 'gaurav.b@gmail.com', '9876543226', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA17-20200017890', 920.00),
(18, 'Kavya Singhania', 'kavya.s@gmail.com', '9876543227', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA18-20220018901', 1340.00),
(19, 'Manoj Gowda', 'manoj.g@gmail.com', '9876543228', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA19-20210019012', 710.00),
(20, 'Swati Rao', 'swati.rao@gmail.com', '9876543229', 'scrypt:32768:8:1$VnqlCObCABo5q6u6$1c98383fdaf8ee9e5df5ac556180af69ab702bbbd9af95dc6650cd54d34b3ba28ef9d5b67476915c2373e20aa241e01c7d30ec810821c4a689a87ca3888fefd2', 'KA20-20230020123', 890.00);

-- ---------------------------------------------------------------------
-- 3. Parking_Areas (3 Real-World Style Parking Facilities)
-- ---------------------------------------------------------------------
INSERT INTO Parking_Areas (area_id, area_name, location_address, total_capacity, operating_status) VALUES
(1, 'Central Tech Park Plaza', 'Gate 1, Electronic City Phase 1, Bengaluru', 15, 'OPEN'),
(2, 'Metro Grand Central Complex', 'MG Road Metro Station Hub, Bengaluru', 12, 'OPEN'),
(3, 'Airport Express Terminal Lot', 'Terminal 2 Approach Road, Devanahalli', 10, 'OPEN');

-- ---------------------------------------------------------------------
-- 4. Pricing (Configured tariffs for each area and vehicle category)
-- ---------------------------------------------------------------------
INSERT INTO Pricing (area_id, vehicle_type, base_hourly_rate, grace_period_mins, overstay_penalty_rate) VALUES
(1, 'TWO_WHEELER', 20.00, 15, 30.00),
(1, 'SEDAN', 40.00, 15, 60.00),
(1, 'SUV', 50.00, 15, 75.00),
(1, 'ELECTRIC_VEHICLE', 35.00, 15, 50.00),
(1, 'TRUCK', 80.00, 15, 120.00),
(2, 'TWO_WHEELER', 15.00, 10, 25.00),
(2, 'SEDAN', 35.00, 10, 50.00),
(2, 'SUV', 45.00, 10, 70.00),
(2, 'ELECTRIC_VEHICLE', 30.00, 10, 45.00),
(3, 'TWO_WHEELER', 30.00, 20, 50.00),
(3, 'SEDAN', 70.00, 20, 100.00),
(3, 'SUV', 90.00, 20, 140.00),
(3, 'ELECTRIC_VEHICLE', 60.00, 20, 90.00);

-- ---------------------------------------------------------------------
-- 5. Parking_Slots (37 Parking Slots across 3 Areas)
-- ---------------------------------------------------------------------
INSERT INTO Parking_Slots (slot_id, area_id, slot_number, floor_level, supported_vehicle_type, slot_status, is_ev_charging_equipped) VALUES
(1, 1, 'TP-A01', 'Ground Floor', 'SEDAN', 'OCCUPIED', 0),
(2, 1, 'TP-A02', 'Ground Floor', 'SEDAN', 'AVAILABLE', 0),
(3, 1, 'TP-A03', 'Ground Floor', 'SUV', 'OCCUPIED', 0),
(4, 1, 'TP-A04', 'Ground Floor', 'SUV', 'AVAILABLE', 0),
(5, 1, 'TP-A05', 'Ground Floor', 'ELECTRIC_VEHICLE', 'RESERVED', 1),
(6, 1, 'TP-A06', 'Ground Floor', 'ELECTRIC_VEHICLE', 'AVAILABLE', 1),
(7, 1, 'TP-A07', 'Level 1', 'TWO_WHEELER', 'AVAILABLE', 0),
(8, 1, 'TP-A08', 'Level 1', 'TWO_WHEELER', 'OCCUPIED', 0),
(9, 1, 'TP-A09', 'Level 1', 'TWO_WHEELER', 'AVAILABLE', 0),
(10, 1, 'TP-A10', 'Level 1', 'SEDAN', 'AVAILABLE', 0),
(11, 1, 'TP-A11', 'Level 1', 'SEDAN', 'AVAILABLE', 0),
(12, 1, 'TP-A12', 'Level 2', 'SUV', 'AVAILABLE', 0),
(13, 1, 'TP-A13', 'Level 2', 'ELECTRIC_VEHICLE', 'AVAILABLE', 1),
(14, 1, 'TP-A14', 'Ground Floor', 'TRUCK', 'AVAILABLE', 0),
(15, 1, 'TP-A15', 'Ground Floor', 'TRUCK', 'AVAILABLE', 0),
(16, 2, 'MC-B01', 'Basement 1', 'SEDAN', 'RESERVED', 0),
(17, 2, 'MC-B02', 'Basement 1', 'SEDAN', 'AVAILABLE', 0),
(18, 2, 'MC-B03', 'Basement 1', 'SUV', 'OCCUPIED', 0),
(19, 2, 'MC-B04', 'Basement 1', 'SUV', 'AVAILABLE', 0),
(20, 2, 'MC-B05', 'Basement 1', 'ELECTRIC_VEHICLE', 'AVAILABLE', 1),
(21, 2, 'MC-B06', 'Basement 1', 'ELECTRIC_VEHICLE', 'AVAILABLE', 1),
(22, 2, 'MC-B07', 'Basement 2', 'TWO_WHEELER', 'AVAILABLE', 0),
(23, 2, 'MC-B08', 'Basement 2', 'TWO_WHEELER', 'AVAILABLE', 0),
(24, 2, 'MC-B09', 'Basement 2', 'TWO_WHEELER', 'AVAILABLE', 0),
(25, 2, 'MC-B10', 'Basement 2', 'SEDAN', 'AVAILABLE', 0),
(26, 2, 'MC-B11', 'Basement 2', 'SEDAN', 'AVAILABLE', 0),
(27, 2, 'MC-B12', 'Basement 2', 'SUV', 'AVAILABLE', 0),
(28, 3, 'AP-C01', 'Terminal Bay 1', 'SEDAN', 'AVAILABLE', 0),
(29, 3, 'AP-C02', 'Terminal Bay 1', 'SEDAN', 'AVAILABLE', 0),
(30, 3, 'AP-C03', 'Terminal Bay 1', 'SUV', 'OCCUPIED', 0),
(31, 3, 'AP-C04', 'Terminal Bay 1', 'SUV', 'AVAILABLE', 0),
(32, 3, 'AP-C05', 'Terminal Bay 1', 'ELECTRIC_VEHICLE', 'AVAILABLE', 1),
(33, 3, 'AP-C06', 'Terminal Bay 2', 'ELECTRIC_VEHICLE', 'AVAILABLE', 1),
(34, 3, 'AP-C07', 'Terminal Bay 2', 'TWO_WHEELER', 'AVAILABLE', 0),
(35, 3, 'AP-C08', 'Terminal Bay 2', 'TWO_WHEELER', 'AVAILABLE', 0),
(36, 3, 'AP-C09', 'Terminal Bay 2', 'SEDAN', 'AVAILABLE', 0),
(37, 3, 'AP-C10', 'Terminal Bay 2', 'SUV', 'AVAILABLE', 0);

-- ---------------------------------------------------------------------
-- 6. Vehicles (26 Registered Vehicles)
-- ---------------------------------------------------------------------
INSERT INTO Vehicles (vehicle_id, user_id, license_plate, vehicle_type, make_model, color) VALUES
(1, 1, 'KA01MH1001', 'SEDAN', 'Honda City', 'Pearl White'),
(2, 1, 'KA01EK2002', 'TWO_WHEELER', 'Ather 450X', 'Space Grey'),
(3, 2, 'KA02AB3003', 'SEDAN', 'Hyundai Verna', 'Starry Night'),
(4, 3, 'KA03CD4004', 'SUV', 'Tata Harrier', 'Calypso Red'),
(5, 3, 'KA03EF5005', 'ELECTRIC_VEHICLE', 'Tata Nexon EV', 'Teal Blue'),
(6, 4, 'KA04GH6006', 'TWO_WHEELER', 'Royal Enfield Classic 350', 'Stealth Black'),
(7, 5, 'KA05IJ7007', 'SUV', 'Mahindra XUV700', 'Midnight Black'),
(8, 6, 'KA06KL8008', 'SEDAN', 'Skoda Slavia', 'Crystal Blue'),
(9, 7, 'KA07MN9009', 'ELECTRIC_VEHICLE', 'MG ZS EV', 'Curator Silver'),
(10, 8, 'KA08OP0110', 'TWO_WHEELER', 'Honda Activa 6G', 'Pearl Precious White'),
(11, 9, 'KA09QR1221', 'SEDAN', 'Maruti Suzuki Ciaz', 'Metallic Magma Grey'),
(12, 10, 'KA10ST2332', 'SUV', 'Toyota Fortuner', 'Super White'),
(13, 11, 'KA11UV3443', 'TWO_WHEELER', 'TVS Jupiter 125', 'Titanium Grey'),
(14, 12, 'KA12WX4554', 'SEDAN', 'Volkswagen Virtus', 'Wild Cherry Red'),
(15, 13, 'KA13YZ5665', 'SUV', 'Hyundai Creta', 'Knight Black'),
(16, 14, 'KA14AA6776', 'TWO_WHEELER', 'Yamaha FZ-S', 'Matte Blue'),
(17, 15, 'KA15BB7887', 'ELECTRIC_VEHICLE', 'BYD Atto 3', 'Ski White'),
(18, 16, 'KA16CC8998', 'SEDAN', 'Honda Amaze', 'Radiant Red'),
(19, 17, 'KA17DD9001', 'SUV', 'Kia Seltos', 'Gravity Grey'),
(20, 18, 'KA18EE0112', 'TWO_WHEELER', 'Suzuki Access 125', 'Metallic Matte Platinum'),
(21, 19, 'KA19FF1223', 'SEDAN', 'Maruti Suzuki Dzire', 'Arctic White'),
(22, 20, 'KA20GG2334', 'SUV', 'Tata Safari', 'Cosmic Gold'),
(23, 2, 'KA02HH3445', 'ELECTRIC_VEHICLE', 'Hyundai Ioniq 5', 'Gravity Gold Matte'),
(24, 5, 'KA05II4556', 'SEDAN', 'BMW 330Li', 'Portimao Blue'),
(25, 7, 'KA07JJ5667', 'TWO_WHEELER', 'KTM Duke 250', 'Electronic Orange'),
(26, 1, 'KA01KK6778', 'TRUCK', 'Tata Ace Gold', 'Arctic White');

-- ---------------------------------------------------------------------
-- 7. Reservations (Active, Confirmed, Completed, Cancelled)
-- ---------------------------------------------------------------------
INSERT INTO Reservations (reservation_id, user_id, vehicle_id, slot_id, start_time, end_time, estimated_cost, booking_status, booking_code) VALUES
(1, 1, 1, 1, DATE_SUB(NOW(), INTERVAL 2 HOUR), DATE_ADD(NOW(), INTERVAL 2 HOUR), 160.00, 'CHECKED_IN', 'PK-A01001'),
(2, 3, 4, 3, DATE_SUB(NOW(), INTERVAL 3 HOUR), DATE_ADD(NOW(), INTERVAL 1 HOUR), 200.00, 'CHECKED_IN', 'PK-A03002'),
(3, 4, 6, 8, DATE_SUB(NOW(), INTERVAL 1 HOUR), DATE_ADD(NOW(), INTERVAL 3 HOUR), 80.00, 'CHECKED_IN', 'PK-A08003'),
(4, 5, 7, 18, DATE_SUB(NOW(), INTERVAL 4 HOUR), DATE_ADD(NOW(), INTERVAL 2 HOUR), 270.00, 'CHECKED_IN', 'PK-B03004'),
(5, 10, 12, 30, DATE_SUB(NOW(), INTERVAL 1 HOUR), DATE_ADD(NOW(), INTERVAL 4 HOUR), 450.00, 'CHECKED_IN', 'PK-C03005'),
(6, 3, 5, 5, DATE_ADD(NOW(), INTERVAL 1 HOUR), DATE_ADD(NOW(), INTERVAL 4 HOUR), 105.00, 'CONFIRMED', 'PK-A05006'),
(7, 2, 3, 16, DATE_ADD(NOW(), INTERVAL 2 HOUR), DATE_ADD(NOW(), INTERVAL 5 HOUR), 105.00, 'CONFIRMED', 'PK-B01007'),
(8, 6, 8, 2, DATE_SUB(NOW(), INTERVAL 2 DAY), DATE_SUB(NOW(), INTERVAL 2 DAY - INTERVAL 3 HOUR), 120.00, 'COMPLETED', 'PK-A02008'),
(9, 7, 9, 6, DATE_SUB(NOW(), INTERVAL 1 DAY), DATE_SUB(NOW(), INTERVAL 1 DAY - INTERVAL 2 HOUR), 70.00, 'COMPLETED', 'PK-A06009'),
(10, 8, 10, 7, DATE_SUB(NOW(), INTERVAL 3 DAY), DATE_SUB(NOW(), INTERVAL 3 DAY - INTERVAL 4 HOUR), 80.00, 'COMPLETED', 'PK-A07010'),
(11, 9, 11, 10, DATE_SUB(NOW(), INTERVAL 4 DAY), DATE_SUB(NOW(), INTERVAL 4 DAY - INTERVAL 2 HOUR), 80.00, 'COMPLETED', 'PK-A10011'),
(12, 11, 13, 22, DATE_SUB(NOW(), INTERVAL 2 DAY), DATE_SUB(NOW(), INTERVAL 2 DAY - INTERVAL 3 HOUR), 45.00, 'COMPLETED', 'PK-B07012'),
(13, 12, 14, 11, DATE_SUB(NOW(), INTERVAL 1 DAY), DATE_SUB(NOW(), INTERVAL 1 DAY - INTERVAL 2 HOUR), 80.00, 'CANCELLED', 'PK-A11013');

-- ---------------------------------------------------------------------
-- 8. Parking_Sessions (Active and Historical)
-- ---------------------------------------------------------------------
INSERT INTO Parking_Sessions (session_id, reservation_id, slot_id, vehicle_id, entry_time, exit_time, duration_minutes, calculated_amount, session_status) VALUES
(1, 1, 1, 1, DATE_SUB(NOW(), INTERVAL 2 HOUR), NULL, NULL, 0.00, 'ACTIVE'),
(2, 2, 3, 4, DATE_SUB(NOW(), INTERVAL 3 HOUR), NULL, NULL, 0.00, 'ACTIVE'),
(3, 3, 8, 6, DATE_SUB(NOW(), INTERVAL 75 MINUTE), NULL, NULL, 0.00, 'ACTIVE'),
(4, 4, 18, 7, DATE_SUB(NOW(), INTERVAL 210 MINUTE), NULL, NULL, 0.00, 'ACTIVE'),
(5, 5, 30, 12, DATE_SUB(NOW(), INTERVAL 50 MINUTE), NULL, NULL, 0.00, 'ACTIVE'),
(6, 8, 2, 8, DATE_SUB(NOW(), INTERVAL 2 DAY), DATE_SUB(NOW(), INTERVAL 2 DAY - INTERVAL 180 MINUTE), 180, 120.00, 'COMPLETED'),
(7, 9, 6, 9, DATE_SUB(NOW(), INTERVAL 1 DAY), DATE_SUB(NOW(), INTERVAL 1 DAY - INTERVAL 115 MINUTE), 115, 70.00, 'COMPLETED'),
(8, 10, 7, 10, DATE_SUB(NOW(), INTERVAL 3 DAY), DATE_SUB(NOW(), INTERVAL 3 DAY - INTERVAL 240 MINUTE), 240, 80.00, 'COMPLETED'),
(9, 11, 10, 11, DATE_SUB(NOW(), INTERVAL 4 DAY), DATE_SUB(NOW(), INTERVAL 4 DAY - INTERVAL 130 MINUTE), 130, 80.00, 'COMPLETED'),
(10, 12, 22, 13, DATE_SUB(NOW(), INTERVAL 2 DAY), DATE_SUB(NOW(), INTERVAL 2 DAY - INTERVAL 170 MINUTE), 170, 45.00, 'COMPLETED');

-- ---------------------------------------------------------------------
-- 9. Payments (Settled Financial Transactions)
-- ---------------------------------------------------------------------
INSERT INTO Payments (payment_id, session_id, reservation_id, user_id, amount, payment_method, payment_status, transaction_reference, paid_at) VALUES
(1, 1, 1, 1, 160.00, 'WALLET', 'SUCCESS', 'TXN-9F8A7B6C5D4E', DATE_SUB(NOW(), INTERVAL 2 HOUR)),
(2, 2, 2, 3, 200.00, 'UPI', 'SUCCESS', 'TXN-8E7D6C5B4A3F', DATE_SUB(NOW(), INTERVAL 3 HOUR)),
(3, 3, 3, 4, 80.00, 'CREDIT_CARD', 'SUCCESS', 'TXN-7D6C5B4A3F2E', DATE_SUB(NOW(), INTERVAL 75 MINUTE)),
(4, 4, 4, 5, 270.00, 'WALLET', 'SUCCESS', 'TXN-6C5B4A3F2E1D', DATE_SUB(NOW(), INTERVAL 210 MINUTE)),
(5, 5, 5, 10, 450.00, 'DEBIT_CARD', 'SUCCESS', 'TXN-5B4A3F2E1D0C', DATE_SUB(NOW(), INTERVAL 50 MINUTE)),
(6, NULL, 6, 3, 105.00, 'WALLET', 'SUCCESS', 'TXN-4A3F2E1D0C9B', NOW()),
(7, NULL, 7, 2, 105.00, 'UPI', 'SUCCESS', 'TXN-3F2E1D0C9B8A', NOW()),
(8, 6, 8, 6, 120.00, 'WALLET', 'SUCCESS', 'TXN-2E1D0C9B8A7F', DATE_SUB(NOW(), INTERVAL 2 DAY)),
(9, 7, 9, 7, 70.00, 'UPI', 'SUCCESS', 'TXN-1D0C9B8A7F6E', DATE_SUB(NOW(), INTERVAL 1 DAY)),
(10, 8, 10, 8, 80.00, 'DEBIT_CARD', 'SUCCESS', 'TXN-0C9B8A7F6E5D', DATE_SUB(NOW(), INTERVAL 3 DAY)),
(11, 9, 11, 9, 80.00, 'WALLET', 'SUCCESS', 'TXN-9B8A7F6E5D4C', DATE_SUB(NOW(), INTERVAL 4 DAY)),
(12, 10, 12, 11, 45.00, 'CASH', 'SUCCESS', 'TXN-8A7F6E5D4C3B', DATE_SUB(NOW(), INTERVAL 2 DAY)),
(13, NULL, 13, 12, 80.00, 'WALLET', 'REFUNDED', 'TXN-7F6E5D4C3B2A', DATE_SUB(NOW(), INTERVAL 1 DAY));
