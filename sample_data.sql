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

-- (Rest of sample records for areas, slots, vehicles, reservations, sessions, payments remain identical)
