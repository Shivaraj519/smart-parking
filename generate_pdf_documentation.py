import os
import sys
from fpdf import FPDF
from fpdf.enums import XPos, YPos

def clean_text(s):
    if not isinstance(s, str):
        s = str(s)
    replacements = {
        '\u2014': '--',
        '\u2013': '-',
        '\u2022': '*',
        '\u2018': "'",
        '\u2019': "'",
        '\u201c': '"',
        '\u201d': '"',
        '\u2192': '->',
        '\u2026': '...',
        '\u00a0': ' ',
        '\u2265': '>=',
        '\u2264': '<=',
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    return s.encode('latin-1', 'replace').decode('latin-1')

class ParkSmartDocPDF(FPDF):
    def cell(self, *args, **kwargs):
        if len(args) > 2 and isinstance(args[2], str):
            args = list(args)
            args[2] = clean_text(args[2])
            args = tuple(args)
        elif 'text' in kwargs and isinstance(kwargs['text'], str):
            kwargs['text'] = clean_text(kwargs['text'])
        return super().cell(*args, **kwargs)

    def multi_cell(self, *args, **kwargs):
        if len(args) > 2 and isinstance(args[2], str):
            args = list(args)
            args[2] = clean_text(args[2])
            args = tuple(args)
        elif 'text' in kwargs and isinstance(kwargs['text'], str):
            kwargs['text'] = clean_text(kwargs['text'])
        return super().multi_cell(*args, **kwargs)

    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(15, 18, 15)
        # Theme colors
        self.c_orange = (217, 119, 54)     # #D97736 Burnt Orange
        self.c_terracotta = (184, 92, 46) # #B85C2E
        self.c_cream = (250, 246, 239)     # #FAF6EF Soft Cream
        self.c_beige = (245, 235, 221)     # #F5EBDD Warm Beige
        self.c_espresso = (41, 35, 31)     # #29231F Dark Espresso
        self.c_charcoal = (70, 60, 55)     # #463C37
        self.c_gray_border = (214, 194, 172) # #D6C2AC
        self.c_green = (34, 139, 34)
        self.c_red = (178, 34, 34)

    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'B', 8)
            self.set_text_color(*self.c_terracotta)
            self.cell(0, 6, 'PARKSMART 2.0 | SMART MALL PARKING MANAGEMENT PLATFORM', align='L')
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(120, 110, 100)
            self.cell(0, 6, 'DBMS MINI-PROJECT DOCUMENTATION', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_draw_color(*self.c_gray_border)
            self.set_line_width(0.3)
            self.line(15, 25, 195, 25)
            self.ln(6)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(*self.c_gray_border)
        self.set_line_width(0.3)
        self.line(15, 283, 195, 283)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(130, 120, 110)
        self.cell(0, 8, 'Phoenix Mall of Asia, Bengaluru  |  https://smart-parking.embarko.app', align='L')
        self.cell(0, 8, f'Page {self.page_no()}/{{nb}}', align='R')

    def chapter_title(self, number, title):
        self.ln(4)
        self.set_fill_color(*self.c_beige)
        self.set_draw_color(*self.c_terracotta)
        self.set_line_width(0.8)
        
        # Chapter header box
        self.rect(15, self.get_y(), 180, 10, style='F')
        self.line(15, self.get_y(), 15, self.get_y() + 10)
        self.set_xy(18, self.get_y() + 1.5)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*self.c_terracotta)
        self.cell(0, 7, f"{number}. {title.upper()}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)

    def section_title(self, title):
        self.ln(2)
        self.set_font('Helvetica', 'B', 10.5)
        self.set_text_color(*self.c_espresso)
        self.cell(0, 6, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*self.c_orange)
        self.set_line_width(0.4)
        y = self.get_y()
        self.line(15, y, 70, y)
        self.ln(2)

    def body_paragraph(self, text):
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*self.c_charcoal)
        self.multi_cell(0, 4.8, text)
        self.ln(2)

    def callout_box(self, title, text, bg_color=None, border_color=None):
        if not bg_color:
            bg_color = self.c_beige
        if not border_color:
            border_color = self.c_orange
        self.set_fill_color(*bg_color)
        self.set_draw_color(*border_color)
        self.set_line_width(0.5)
        
        y_start = self.get_y()
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(*self.c_terracotta)
        
        # Calculate height
        lines = len(text.split('\n'))
        box_height = max(14, 8 + (lines * 4.5))
        
        self.rect(15, y_start, 180, box_height, style='FD')
        self.set_xy(18, y_start + 2)
        self.cell(0, 5, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(18, self.get_y())
        self.set_font('Helvetica', '', 8.5)
        self.set_text_color(*self.c_espresso)
        self.multi_cell(174, 4.2, text)
        self.set_y(y_start + box_height + 3)

    def draw_table(self, headers, rows, col_widths, align_cols=None):
        self.set_font('Helvetica', 'B', 8.5)
        self.set_fill_color(*self.c_terracotta)
        self.set_text_color(255, 255, 255)
        self.set_draw_color(*self.c_gray_border)
        self.set_line_width(0.3)
        
        # Header
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 7, header, border=1, align='C', fill=True)
        self.ln()
        
        # Rows
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*self.c_espresso)
        
        for r_idx, row in enumerate(rows):
            fill = (r_idx % 2 == 1)
            if fill:
                self.set_fill_color(*self.c_cream)
            else:
                self.set_fill_color(255, 255, 255)
                
            for c_idx, cell in enumerate(row):
                align = align_cols[c_idx] if align_cols else 'L'
                self.cell(col_widths[c_idx], 6, str(cell), border=1, align=align, fill=True)
            self.ln()
        self.ln(2)

def generate_pdf():
    pdf = ParkSmartDocPDF()
    pdf.alias_nb_pages()
    
    # =========================================================================
    # COVER PAGE
    # =========================================================================
    pdf.add_page()
    
    # Outer Decorative Border
    pdf.set_draw_color(*pdf.c_terracotta)
    pdf.set_line_width(1.0)
    pdf.rect(12, 12, 186, 273)
    pdf.set_draw_color(*pdf.c_gray_border)
    pdf.set_line_width(0.4)
    pdf.rect(14, 14, 182, 269)
    
    # Top Burnt Orange Banner
    pdf.set_fill_color(*pdf.c_orange)
    pdf.rect(15, 25, 180, 48, style='F')
    
    pdf.set_xy(20, 32)
    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'PARKSMART 2.0', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(255, 240, 220)
    pdf.cell(0, 7, 'SMART MALL PARKING MANAGEMENT PLATFORM', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 6, 'Complete Academic DBMS Mini-Project & Production SaaS Architecture Report', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Hero Information Badge
    pdf.set_y(85)
    pdf.set_fill_color(*pdf.c_beige)
    pdf.set_draw_color(*pdf.c_orange)
    pdf.set_line_width(0.5)
    pdf.rect(25, 80, 160, 40, style='FD')
    
    pdf.set_xy(30, 85)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*pdf.c_terracotta)
    pdf.cell(0, 6, 'DEMONSTRATION LOCATION: PHOENIX MALL OF ASIA, BENGALURU', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font('Helvetica', '', 9.5)
    pdf.set_text_color(*pdf.c_espresso)
    pdf.set_x(30)
    pdf.cell(0, 5, 'Flagship 3-Tier Multi-Floor Facility: B1 (Gold), B2 (Platinum), LG (Express 2-Wheelers)', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(30)
    pdf.cell(0, 5, 'Total Monitored Bays: 20 Demo Sensor Nodes | Real-Time Ultrasonic Feedback', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(30)
    pdf.cell(0, 5, 'Live System Status: ONLINE & OPERATIONAL', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Metadata Table
    pdf.set_y(135)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*pdf.c_espresso)
    pdf.cell(0, 6, 'PROJECT METADATA & DEPLOYMENT DETAILS', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    
    meta_headers = ['Field / Resource', 'Specification Details']
    meta_rows = [
        ['Academic Discipline', 'Database Management Systems (DBMS) - B.Tech / B.E. Mini-Project'],
        ['Live Application URL', 'https://smart-parking.embarko.app'],
        ['GitHub Repository', 'https://github.com/Shivaraj519/smart-parking'],
        ['Local Server Endpoint', 'http://127.0.0.1:5050 (configured to avoid port 5000 collisions)'],
        ['Core Database Engines', 'MySQL 8.0 Enterprise DDL/DML + SQLite 3 Embedded Compatibility'],
        ['Backend Web Framework', 'Python 3.11+ / Flask 3.1.0 with WSGI Gunicorn Server'],
        ['Frontend Design Architecture', 'HTML5, CSS3 Glassmorphism, Bootstrap 5.3, GSAP 3.12, Chart.js 4'],
        ['Database Normalization', 'Third Normal Form (3NF) compliant across 9 relational tables'],
        ['Security & Auth', 'PBKDF2-SHA256 Cryptographic Hashes + Role-Based Access Control'],
        ['Version & Date', 'Release 2.0.4 | November 2026']
    ]
    pdf.draw_table(meta_headers, meta_rows, [55, 125])
    
    # Portals Summary Box
    pdf.set_y(215)
    pdf.callout_box(
        'SUPPORTED SYSTEM PORTALS (3 INDEPENDENT WORKSPACES)',
        '1. Driver / User Portal: Online reservation, wallet payments, digital garage, and Find My Car.\n'
        '2. Watchman Barrier Portal: Fast touch barrier check-in/out terminal for security personnel.\n'
        '3. Mall Admin Console: Capacity analytics, dynamic tariff configuration, slot CRUD, SQL demo lab.'
    )
    
    pdf.set_y(255)
    pdf.set_font('Helvetica', 'I', 8.5)
    pdf.set_text_color(130, 120, 110)
    pdf.cell(0, 5, 'Designed and authored as an engineering DBMS Mini-Project and production-grade Web App.', align='C')

    # =========================================================================
    # CHAPTER 1: EXECUTIVE SUMMARY & OBJECTIVE
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title(1, 'Executive Summary & Project Overview')
    
    pdf.section_title('1.1 Project Objective')
    pdf.body_paragraph(
        'The Smart Parking Slot Management System (ParkSmart 2.0) is a comprehensive web-based platform designed to '
        'eliminate urban parking friction within modern multi-level shopping centers, with a specific focus on the '
        'Phoenix Mall of Asia in Bengaluru. Unlike trivial database mockups, this project establishes a rock-solid '
        'relational foundation that models every real-world entity—from ultrasonic bay sensors and floor zoning to '
        'prepaid wallet deductions, barrier gate boom triggers, and minute-accurate duration tracking.'
    )
    
    pdf.section_title('1.2 High-Density Mall Parking Challenges')
    pdf.body_paragraph(
        'Modern high-footfall commercial shopping destinations experience severe bottlenecking during peak weekend '
        'and festive hours. Typical challenges include:\n'
        ' • Entry Barrier Queue Stalls: Paper tickets require 45-60 seconds per car, causing street-level traffic spills.\n'
        ' • Double-Booking Anomalies: Disconnected booking apps assign the same physical slot to multiple vehicles.\n'
        ' • Parking Space Lostness: Drivers frequently forget their vehicle bay in sprawling 3-level basement facilities.\n'
        ' • Revenue Leakage: Unaudited cash collections at exit barriers lack atomic relational ledger tracking.'
    )
    
    pdf.section_title('1.3 Solution Pillars in ParkSmart 2.0')
    pdf.body_paragraph(
        'ParkSmart 2.0 directly resolves these pain points through three engineered core capabilities:\n'
        ' 1. Atomic Concurrency Control: Relational database transactions with pessimistic row locking prevent race '
        'conditions and guarantee that two drivers cannot book the same slot for overlapping intervals.\n'
        ' 2. Real-Time Ultrasonic Sensor Map: A visual floor plan displaying live occupancy states (Available, Reserved, Occupied) '
        'with an interactive modal allowing users to inspect bay properties and vehicle occupancy.\n'
        ' 3. Find My Car & Pedestrian Wayfinding: Enter any registered license plate to pinpoint exact floor, section, '
        'and row coordinates with turn-by-turn walking guidance from the nearest mall elevators.'
    )

    # =========================================================================
    # CHAPTER 2: WHAT IS USED (TECHNOLOGY STACK)
    # =========================================================================
    pdf.chapter_title(2, 'What Is Used (Technology Stack & Architecture)')
    
    pdf.body_paragraph(
        'The application employs a decoupled, multi-tier architecture adhering to modern web development standards. '
        'Every technology choice was selected to balance developer productivity, visual elegance, and strict database integrity.'
    )
    
    tech_headers = ['Tier / Component', 'Technologies Employed', 'Architectural Purpose & Responsibility']
    tech_rows = [
        ['Frontend Markup & Style', 'HTML5, CSS3 Custom Properties', 'Semantic layout, responsive grid, bespoke beige & orange styling'],
        ['CSS Framework', 'Bootstrap 5.3 + Utilities', 'Cross-browser responsive grid, modals, alert banners, navbar'],
        ['Visual Styling & Theme', 'Glassmorphism (backdrop-filter)', 'Soft cream (#FAF6EF), burnt orange (#D97736), espresso typography'],
        ['Animations & Transitions', 'GSAP 3.12 + ScrollTrigger', 'Editorial text reveals, card fade-ins, live sensor radar sweeps'],
        ['Interactive Charts', 'Chart.js 4 (Canvas API)', 'Real-time occupancy doughnuts, hourly revenue bars, daily trend lines'],
        ['Backend Engine', 'Python 3.11+ / Flask 3.1.0', 'REST routing, view controllers, session auth, business logic'],
        ['Cryptography & Security', 'Werkzeug Security (PBKDF2)', 'Cryptographic password hashing, RBAC session decorators'],
        ['Template Engine', 'Jinja2 Server-Side Engine', 'Dynamic data rendering, layout inheritance, XSS escaping'],
        ['WSGI Production Server', 'Gunicorn 21.2+ (Green Unicorn)', 'Pre-fork worker model for high-concurrency production serving'],
        ['Primary Database Engine', 'MySQL 8.0 Enterprise Relational', 'Strict 3NF DDL/DML, InnoDB engine, foreign keys, triggers, views'],
        ['Local Fallback Engine', 'SQLite 3 Embedded Relational', 'Self-healing portable zero-config engine with auto date translation'],
        ['Cloud Deployment', 'Embarko PaaS / Render Web Svc', 'Production cloud hosting with DATA_DIR persistent storage']
    ]
    pdf.draw_table(tech_headers, tech_rows, [35, 45, 100])
    
    pdf.section_title('2.1 Bespoke Color Palette & Typography')
    pdf.body_paragraph(
        'To distance the project from generic Bootstrap templates, a tailored Editorial Orange & Beige color system was created:\n'
        ' • Canvas Background: Soft Cream (#FAF6EF) and Warm Beige (#F5EBDD).\n'
        ' • Primary Action Accent: Burnt Orange (#D97736) and Deep Terracotta (#B85C2E).\n'
        ' • Dark Typography: Dark Espresso (#29231F) ensuring WCAG AAA contrast ratio compliance.\n'
        ' • Editorial Typeface: Playfair Display for editorial headings, paired with Inter and DM Sans for clean numbers.'
    )

    # =========================================================================
    # CHAPTER 3: WHAT WE HAVE (DATABASE DESIGN)
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title(3, 'Relational Database Architecture (The DBMS Foundation)')
    
    pdf.body_paragraph(
        'The relational database is the central core of ParkSmart 2.0. The schema is fully normalized into Third Normal '
        'Form (3NF), ensuring zero functional dependencies on non-key attributes and eliminating insertion, update, and '
        'deletion anomalies across all business operations.'
    )
    
    pdf.section_title('3.1 Relational Tables Specification')
    schema_headers = ['Table Name', 'Primary Key', 'Foreign Keys', 'Key Columns & Constraints']
    schema_rows = [
        ['Users', 'user_id', 'None', 'email (UNIQUE), phone (UNIQUE), password_hash, wallet_balance >= 0'],
        ['Admins', 'admin_id', 'None', 'username (UNIQUE), role IN (\'SUPER_ADMIN\', \'MANAGER\', \'WATCHMAN\')'],
        ['Vehicles', 'vehicle_id', 'user_id -> Users', 'license_plate (UNIQUE), vehicle_type, make_model, is_active'],
        ['Parking_Areas', 'area_id', 'None', 'area_name (UNIQUE), total_capacity, operating_status (\'OPEN\')'],
        ['Parking_Slots', 'slot_id', 'area_id -> Areas', 'slot_number (UNIQUE per area), floor_level, section, row, status'],
        ['Reservations', 'reservation_id', 'user, vehicle, slot', 'booking_code (UNIQUE), start_time, end_time, status, cost'],
        ['Parking_Sessions', 'session_id', 'slot, vehicle, res_id', 'entry_time, exit_time, duration_minutes, checked_in/out_by'],
        ['Payments', 'payment_id', 'user, res_id, session', 'transaction_ref (UNIQUE), amount > 0, payment_method, status'],
        ['Pricing', 'pricing_id', 'area_id -> Areas', 'vehicle_type, base_hourly_rate, peak_multiplier, ev_surcharge']
    ]
    pdf.draw_table(schema_headers, schema_rows, [30, 25, 45, 80])
    
    pdf.section_title('3.2 Database Views')
    pdf.body_paragraph(
        ' • view_available_slots_summary: Aggregates real-time availability by mall area and vehicle type, combining total, '
        'available, reserved, and occupied slot metrics using conditional SUM(CASE ...) expressions.\n'
        ' • view_payment_audit_trail: Joins Users, Payments, Reservations, and Parking_Sessions into an immutable financial '
        'audit log detailing transaction references, payer identity, duration, and settlement status.'
    )
    
    pdf.section_title('3.3 Triggers & Automated State Synchronization')
    pdf.body_paragraph(
        ' • trg_after_session_insert_occupy: Automatically updates Parking_Slots.slot_status to \'OCCUPIED\' immediately '
        'upon the insertion of an active vehicle check-in record.\n'
        ' • trg_after_session_update_release: Automatically changes Parking_Slots.slot_status back to \'AVAILABLE\' as soon as '
        'an exit timestamp and completed status are recorded in Parking_Sessions.'
    )
    
    pdf.section_title('3.4 Stored Procedures')
    pdf.body_paragraph(
        ' • sp_reserve_parking_slot: Executes an ACID transaction with pessimistic row-level locking (SELECT ... FOR UPDATE). '
        'Validates user wallet balance, verifies slot availability, inserts the reservation, and commits atomically.\n'
        ' • sp_process_vehicle_exit: Calculates exact parked duration in minutes, queries active pricing tiers, applies EV/peak '
        'multipliers, generates a payment record, deducts the user wallet, and releases the slot.'
    )

    # =========================================================================
    # CHAPTER 4: WHAT WE HAVE (PORTALS & FEATURES)
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title(4, 'What We Have in This Website (Portals & Features)')
    
    pdf.body_paragraph(
        'ParkSmart 2.0 provides three distinct, role-segregated portals serving drivers, security staff, and mall administrators.'
    )
    
    pdf.section_title('4.1 Driver & User Portal')
    pdf.body_paragraph(
        ' • Visual Parking Availability (/availability): Interactive grid displaying available slots filtered by mall, floor, '
        'and vehicle type (Four-Wheeler, Two-Wheeler, EV Charging Dock).\n'
        ' • Digital Wallet & Instant Invoicing: Pre-fund balances with simulated UPI/Card payment channels; automatic fee '
        'deduction upon vehicle checkout with downloadable digital receipts.\n'
        ' • Digital Garage: Customers can register multiple personal vehicles, track active reservations, and cancel eligible bookings.'
    )
    
    pdf.section_title('4.2 Interactive 3D Mall Map & Find My Car (/find-my-car)')
    pdf.body_paragraph(
        ' • Multi-Floor Switching: Seamlessly toggle between Basement 1 (Zone Gold), Basement 2 (Zone Platinum), and '
        'Lower Ground (Two-Wheeler Express) at Phoenix Mall of Asia.\n'
        ' • Live Ultrasonic Sensor Visualization: Bays glow in real-time sensor states—Green (Available), Amber (Reserved), '
        'and Red (Occupied).\n'
        ' • Interactive Bay Inspection Modal: Clicking any bay opens a glassmorphism modal presenting slot code, exact row/section, '
        'vehicle compatibility, EV charging capability, and occupant license plate.\n'
        ' • License Plate Search & Wayfinding: Searching a license plate (e.g., KA01MH1001) pulses the target vehicle on the floor plan '
        'and activates pedestrian walking route guidance from Lobby B elevator banks.'
    )
    
    pdf.section_title('4.3 Mobile-First Watchman Barrier Portal (/watchman/login)')
    pdf.body_paragraph(
        ' • Touch-Optimized Gate Interface: Tailored for handheld tablets and ruggedized phones mounted at entrance/exit booms.\n'
        ' • Quick Inward Verification: Guards scan or enter the 8-character booking code (e.g. PK-78A9B2) or license plate to '
        'verify booking and trigger gate opening.\n'
        ' • One-Tap Outward Clearance: Calculates exact duration, verifies payment settlement, opens exit boom, and releases bay.'
    )
    
    pdf.section_title('4.4 Mall Admin & Operations Center (/admin/login)')
    pdf.body_paragraph(
        ' • Executive KPI Dashboard: Real-time mall occupancy percentage, live active sessions, registered customer metrics, '
        'and cumulative daily revenue.\n'
        ' • Chart.js Business Analytics: Visual breakdown of hourly peak arrival times, revenue distribution, and floor utilization.\n'
        ' • Infrastructure CRUD: Add, update, and manage parking areas, slots, and dynamic hourly pricing rules.\n'
        ' • SQL Demonstration Console (/admin/sql-demo): Educational tool executing multi-table joins, correlated subqueries, '
        'and group-by aggregations live against the database.'
    )

    # =========================================================================
    # CHAPTER 5: HOW IT WORKS (OPERATIONAL WORKFLOWS)
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title(5, 'How It Works (End-to-End Operational Workflows)')
    
    pdf.body_paragraph(
        'The following five sequential stages detail how an end-to-end parking transaction is processed through the system:'
    )
    
    flow_headers = ['Stage', 'Actor', 'System Action', 'Database Operations']
    flow_rows = [
        ['1. Discovery', 'Driver', 'Browses live floor capacity at Phoenix Mall of Asia', 'SELECT FROM view_available_slots_summary'],
        ['2. Booking', 'Driver', 'Selects Bay P-B1-02 and reserves slot with wallet balance', 'BEGIN -> SELECT ... FOR UPDATE -> INSERT Reservation -> COMMIT'],
        ['3. Check-In', 'Watchman', 'Enters booking code at entry boom barrier terminal', 'UPDATE Slot (OCCUPIED) -> INSERT Parking_Session (entry_time)'],
        ['4. Wayfinding', 'Driver', 'Uses "Find My Car" with plate KA01MH1001 after shopping', 'SELECT Slot, Section, Row, Floor FROM Sessions JOIN Slots'],
        ['5. Checkout', 'Watchman', 'Processes exit at outward gate; confirms fee settlement', 'UPDATE Session (exit_time) -> INSERT Payment -> UPDATE Slot (AVAILABLE)']
    ]
    pdf.draw_table(flow_headers, flow_rows, [20, 25, 65, 70])
    
    pdf.section_title('5.1 Concurrency & Double-Booking Prevention Algorithm')
    pdf.body_paragraph(
        'When two drivers attempt to book the identical parking slot simultaneously, standard optimistic databases suffer '
        'from race conditions. ParkSmart 2.0 solves this through pessimistic database locking:\n'
        ' 1. Transaction Start: BEGIN TRANSACTION isolates the user request.\n'
        ' 2. Slot Row Lock: The database executes SELECT slot_status FROM Parking_Slots WHERE slot_id = ? FOR UPDATE. '
        'This locks the target row and forces competing requests into a brief queue.\n'
        ' 3. Overlap Check: The system queries active reservations for the slot within the target time window.\n'
        ' 4. Atomic Confirmation: If free, slot status updates to \'RESERVED\', the reservation record is inserted, '
        'and COMMIT finalizes the transaction. If occupied, the transaction performs ROLLBACK and returns an error.'
    )
    
    pdf.section_title('5.2 Automated Duration & Dynamic Tariff Engine')
    pdf.body_paragraph(
        'Upon checkout, the system calculates duration: Duration = CEIL((Exit_Time - Entry_Time) / 60 minutes).\n'
        'Fee Calculation: Total Fee = (Duration in Hours * Base Hourly Rate * Peak Multiplier) + EV Dock Surcharge.\n'
        'The amount is automatically deducted from the driver\'s registered wallet or settled via cash/UPI at the gate.'
    )

    # =========================================================================
    # CHAPTER 6: DEMONSTRATION & VERIFICATION GUIDE
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title(6, 'Testing Credentials & Verification Guide')
    
    pdf.body_paragraph(
        'ParkSmart 2.0 includes pre-seeded demo records for Phoenix Mall of Asia allowing examiners, evaluators, and '
        'users to immediately test every system feature without manual registration.'
    )
    
    cred_headers = ['Portal / Role', 'Access URL', 'Username / Email', 'Password', 'Key Capabilities to Test']
    cred_rows = [
        ['Driver / User', '/login', 'aarav.patel@gmail.com', 'user123', 'Slot booking, digital garage, wallet top-up'],
        ['Driver / User', '/login', 'priya.sharma@gmail.com', 'user123', 'Secondary customer profile, booking history'],
        ['Watchman', '/watchman/login', 'watchman', 'watchman123', 'Barrier gate in/out, booking scanner, plate lookup'],
        ['Mall Admin', '/admin/login', 'admin', 'admin123', 'KPI overview, Chart.js analytics, slot CRUD, SQL lab']
    ]
    pdf.draw_table(cred_headers, cred_rows, [30, 30, 45, 25, 50])
    
    pdf.section_title('6.1 Pre-Parked Demo Vehicles (For "Find My Car" Testing)')
    demo_car_headers = ['License Plate', 'Make & Model', 'Parked Slot', 'Floor Level & Zone', 'Section & Row']
    demo_car_rows = [
        ['KA01MH1001', 'Tata Nexon EV', 'P-B1-02', 'Basement 1 (Zone Gold)', 'Section A, Row 1 (EV Dock)'],
        ['KA03CD4004', 'Hyundai Creta', 'P-B1-08', 'Basement 1 (Zone Gold)', 'Section B, Row 2'],
        ['KA05IJ7007', 'Toyota Innova', 'P-B2-04', 'Basement 2 (Zone Platinum)', 'Section A, Row 2'],
        ['KA06KL8008', 'Royal Enfield Hunter', 'P-LG-03', 'Lower Ground (Zone Express)', 'Section B, Row 1 (2-Wheeler)']
    ]
    pdf.draw_table(demo_car_headers, demo_car_rows, [30, 40, 25, 45, 40])
    
    pdf.section_title('6.2 Running the Application Locally')
    pdf.body_paragraph(
        '1. Clone repository: git clone https://github.com/Shivaraj519/smart-parking.git\n'
        '2. Navigate to project: cd smart_parking\n'
        '3. Install dependencies: pip install -r requirements.txt\n'
        '4. Start application: python app.py\n'
        '5. Access locally at: http://127.0.0.1:5050 (avoids port 5000 conflicts with local voice assistants)'
    )
    
    pdf.ln(4)
    pdf.callout_box(
        'ACADEMIC & EVALUATION NOTE',
        'This project satisfies all requirements for college engineering DBMS curriculum:\n'
        '• Demonstrates 1NF, 2NF, 3NF normalization, primary/foreign key referential integrity.\n'
        '• Implements Views, Triggers, Stored Procedures, Composite Indexes, and ACID Concurrency.\n'
        '• Live production deployment accessible globally at: https://smart-parking.embarko.app'
    )

    output_path = os.path.join(os.path.dirname(__file__), 'ParkSmart_2.0_Complete_Project_Documentation.pdf')
    pdf.output(output_path)
    print(f"==> PDF Successfully Generated at: {output_path}")
    print(f"==> Size: {os.path.getsize(output_path) / 1024:.2f} KB | Total Pages: {pdf.page_no()}")
    return output_path

if __name__ == '__main__':
    generate_pdf()
