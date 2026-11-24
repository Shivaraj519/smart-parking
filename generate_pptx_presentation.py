import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    c_orange = RGBColor(217, 119, 54)      # #D97736 Burnt Orange
    c_terracotta = RGBColor(184, 92, 46)  # #B85C2E Deep Terracotta
    c_espresso = RGBColor(41, 35, 31)      # #29231F Dark Espresso
    c_dark_bg = RGBColor(28, 24, 21)       # #1C1815 Dark Background
    c_card_dark = RGBColor(45, 39, 34)     # #2D2722 Dark Card
    c_cream = RGBColor(250, 246, 239)      # #FAF6EF Soft Cream
    c_beige = RGBColor(245, 235, 221)      # #F5EBDD Warm Beige
    c_white = RGBColor(255, 255, 255)
    c_charcoal = RGBColor(60, 50, 45)
    c_gray = RGBColor(140, 130, 120)
    c_green = RGBColor(46, 125, 50)
    c_red = RGBColor(198, 40, 40)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="DBMS MINI-PROJECT & COMMERCIAL SAAS"):
        # Category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = c_terracotta

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Georgia"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = c_espresso

        # Accent Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = c_orange
        line.line.color.rgb = c_orange

    def add_card(slide, left, top, width, height, title, items, bg_color=c_beige, border_color=c_orange):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.05)
        tf.margin_left = Inches(0.05)
        tf.margin_right = Inches(0.05)

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.name = "Georgia"
        p_title.font.size = Pt(13)
        p_title.font.bold = True
        p_title.font.color.rgb = c_terracotta
        p_title.space_after = Pt(8)

        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.name = "Arial"
            p.font.size = Pt(10)
            p.font.color.rgb = c_charcoal
            p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Luxury Editorial Style)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = c_dark_bg
    bg1.line.fill.background()

    # Orange Top Glow Strip
    strip = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    strip.fill.solid()
    strip.fill.fore_color.rgb = c_orange
    strip.line.fill.background()

    # Title text box
    tb_title = s1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11), Inches(3.5))
    tf1 = tb_title.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "DATABASE MANAGEMENT SYSTEMS (DBMS) ENGINEERING PROJECT"
    p0.font.name = "Arial"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = c_orange
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "PARKSMART 2.0"
    p1.font.name = "Georgia"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = c_white
    p1.space_after = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "Next-Generation Smart Mall Parking Management Platform"
    p2.font.name = "Georgia"
    p2.font.size = Pt(20)
    p2.font.color.rgb = c_beige
    p2.space_after = Pt(20)

    p3 = tf1.add_paragraph()
    p3.text = "Demonstration Facility: Phoenix Mall of Asia, Bengaluru\nMulti-Floor Relational Architecture • Ultrasonic Bay Sensors • Pedestrian Wayfinding"
    p3.font.name = "Arial"
    p3.font.size = Pt(11)
    p3.font.color.rgb = c_gray

    # Bottom Metadata Pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(5.6), Inches(10.9), Inches(1.1))
    pill.fill.solid()
    pill.fill.fore_color.rgb = c_card_dark
    pill.line.color.rgb = c_orange
    pill.line.width = Pt(1)

    pill_tb = s1.shapes.add_textbox(Inches(1.4), Inches(5.7), Inches(10.5), Inches(0.9))
    ptf = pill_tb.text_frame
    pp1 = ptf.paragraphs[0]
    pp1.text = "TECH STACK: Python 3 Flask • MySQL 8.0 / SQLite 3 • Chart.js • Bootstrap 5.3 • GSAP 3.12"
    pp1.font.name = "Arial"
    pp1.font.size = Pt(11)
    pp1.font.bold = True
    pp1.font.color.rgb = c_orange

    pp2 = ptf.add_paragraph()
    pp2.text = "LIVE DEPLOYMENT: https://smart-parking.embarko.app  |  GITHUB: github.com/Shivaraj519/smart-parking"
    pp2.font.name = "Arial"
    pp2.font.size = Pt(10)
    pp2.font.color.rgb = c_cream

    # =========================================================================
    # SLIDE 2: THE PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    bg2 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg2.fill.solid()
    bg2.fill.fore_color.rgb = c_cream
    bg2.line.fill.background()
    add_header(s2, "The Real-World Mall Parking Problem", "CHALLENGES & MOTIVATION")

    add_card(s2, Inches(0.8), Inches(1.9), Inches(3.6), Inches(4.8), 
             "1. Entry Gate Congestion", 
             [
                 "Manual ticketing takes 45 to 60 seconds per vehicle at mall boom barriers.",
                 "Weekend traffic spills over onto public highways (Bellary Road, Bengaluru).",
                 "Drivers enter blindly without knowing if free bays exist inside."
             ])

    add_card(s2, Inches(4.86), Inches(1.9), Inches(3.6), Inches(4.8), 
             "2. Double-Booking Chaos", 
             [
                 "Decoupled booking software lacks atomic database-level transactions.",
                 "Multiple customers reserve the same physical slot at overlapping times.",
                 "Causes customer disputes, security intervention, and revenue loss."
             ])

    add_card(s2, Inches(8.93), Inches(1.9), Inches(3.6), Inches(4.8), 
             "3. Lost Vehicles in Basements", 
             [
                 "Phoenix Mall of Asia features 3 basement levels with thousands of bays.",
                 "Shoppers forget where they parked after spending 3-4 hours shopping.",
                 "Manual searching wastes 20-30 minutes and causes aisle gridlock."
             ])

    # =========================================================================
    # SLIDE 3: PROJECT OBJECTIVES & CORE PILLARS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    bg3 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg3.fill.solid()
    bg3.fill.fore_color.rgb = c_cream
    bg3.line.fill.background()
    add_header(s3, "ParkSmart 2.0 Solution & Engineering Goals", "CORE CAPABILITIES")

    add_card(s3, Inches(0.8), Inches(1.9), Inches(5.6), Inches(2.3),
             "ACID Concurrency & Zero Double-Booking",
             [
                 "Pessimistic row-level locking (SELECT ... FOR UPDATE).",
                 "Atomic COMMIT / ROLLBACK transactions guarantee slot uniqueness.",
                 "Prevents overlapping reservation time windows automatically."
             ])

    add_card(s3, Inches(6.9), Inches(1.9), Inches(5.6), Inches(2.3),
             "Interactive Multi-Floor 3D Mall Map",
             [
                 "Simulates ultrasonic IoT sensors across B1 (Gold), B2 (Platinum), and LG.",
                 "Color-coded states: Emerald (Available), Amber (Reserved), Crimson (Occupied).",
                 "Interactive Bay Inspector modal reveals occupant license plate and model."
             ])

    add_card(s3, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.3),
             "Indoor Pedestrian Wayfinding",
             [
                 "Search any license plate (e.g. KA01MH1001) to locate the exact bay.",
                 "Draws turn-by-turn walking route from central Lobby B elevator banks.",
                 "Provides estimated walking time and zone coordinates."
             ])

    add_card(s3, Inches(6.9), Inches(4.5), Inches(5.6), Inches(2.3),
             "3 Role-Segregated Portals",
             [
                 "Driver Portal: Real-time discovery, booking, digital wallet, and garage.",
                 "Watchman Terminal: Mobile-first touch terminal for barrier boom operations.",
                 "Mall Admin Console: Occupancy KPIs, Chart.js trends, and dynamic pricing."
             ])

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE & TECH STACK
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    bg4 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg4.fill.solid()
    bg4.fill.fore_color.rgb = c_cream
    bg4.line.fill.background()
    add_header(s4, "Multi-Tier Software & Database Architecture", "WHAT IS USED")

    add_card(s4, Inches(0.8), Inches(1.9), Inches(2.7), Inches(4.8),
             "Frontend Tier",
             [
                 "HTML5 & Semantic Elements",
                 "Bespoke Orange-Beige Palette",
                 "CSS3 Glassmorphism",
                 "Bootstrap 5.3 Responsive Grid",
                 "GSAP 3.12 & ScrollTrigger",
                 "Playfair Display Typeface",
                 "Font Awesome 6.4 Icons"
             ])

    add_card(s4, Inches(3.8), Inches(1.9), Inches(2.7), Inches(4.8),
             "Backend Tier",
             [
                 "Python 3.11+ Runtime",
                 "Flask 3.1.0 Web Framework",
                 "Werkzeug Security (PBKDF2)",
                 "Jinja2 Dynamic Templates",
                 "Role-Based Decorators",
                 "RESTful JSON APIs",
                 "Gunicorn WSGI Server"
             ])

    add_card(s4, Inches(6.8), Inches(1.9), Inches(2.7), Inches(4.8),
             "Database Tier",
             [
                 "MySQL 8.0 Enterprise Relational",
                 "Portable SQLite 3 Fallback",
                 "Connection Pooling (5 pool)",
                 "ACID Concurrency Isolation",
                 "Triggers & Stored Procedures",
                 "Relational Views",
                 "Composite Indexing"
             ])

    add_card(s4, Inches(9.8), Inches(1.9), Inches(2.7), Inches(4.8),
             "Analytics & Cloud",
             [
                 "Chart.js 4 Canvas Engine",
                 "Real-time Occupancy Doughnut",
                 "Peak Hours Arrival Bar Chart",
                 "Daily Revenue Trends",
                 "Embarko Cloud PaaS",
                 "Persistent DATA_DIR Storage",
                 "GitHub Actions CI/CD"
             ])

    # =========================================================================
    # SLIDE 5: RELATIONAL DATABASE DESIGN (3NF SCHEMA)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    bg5 = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg5.fill.solid()
    bg5.fill.fore_color.rgb = c_cream
    bg5.line.fill.background()
    add_header(s5, "3NF Relational Database Schema (9 Tables)", "DBMS FOUNDATION")

    schema_cards = [
        ("Users", ["user_id (PK)", "full_name, email, phone", "password_hash (PBKDF2)", "wallet_balance >= 0"]),
        ("Vehicles", ["vehicle_id (PK)", "user_id (FK -> Users)", "license_plate (UNIQUE)", "vehicle_type, make_model"]),
        ("Parking_Areas", ["area_id (PK)", "area_name (UNIQUE)", "location_address", "total_capacity, status"]),
        ("Parking_Slots", ["slot_id (PK)", "area_id (FK -> Areas)", "slot_number, floor_level", "section, row, is_ev_equipped"]),
        ("Reservations", ["reservation_id (PK)", "user_id, vehicle_id, slot_id", "booking_code (UNIQUE)", "start_time, end_time, cost"]),
        ("Parking_Sessions", ["session_id (PK)", "slot_id, vehicle_id, res_id", "entry_time, exit_time", "duration_minutes, checked_by"])
    ]

    for idx, (tbl, cols) in enumerate(schema_cards):
        row = idx // 3
        col = idx % 3
        left = Inches(0.8 + col * 4.0)
        top = Inches(1.9 + row * 2.5)
        add_card(s5, left, top, Inches(3.7), Inches(2.2), f"Table: {tbl}", cols)

    # =========================================================================
    # SLIDE 6: ADVANCED SQL & DBMS CONCEPTS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    bg6 = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg6.fill.solid()
    bg6.fill.fore_color.rgb = c_cream
    bg6.line.fill.background()
    add_header(s6, "Practical Implementation of Advanced DBMS Concepts", "ACADEMIC EXCELLENCE")

    add_card(s6, Inches(0.8), Inches(1.9), Inches(5.6), Inches(2.3),
             "Relational Views",
             [
                 "view_available_slots_summary: Aggregates real-time availability by mall area and vehicle type using SUM(CASE ...).",
                 "view_payment_audit_trail: Joins Users, Payments, Reservations, and Sessions into an immutable financial audit ledger."
             ])

    add_card(s6, Inches(6.9), Inches(1.9), Inches(5.6), Inches(2.3),
             "Database Triggers",
             [
                 "trg_after_session_insert_occupy: Automatically updates Parking_Slots.slot_status to 'OCCUPIED' upon check-in.",
                 "trg_after_session_update_release: Automatically restores Parking_Slots.slot_status to 'AVAILABLE' upon vehicle checkout."
             ])

    add_card(s6, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.3),
             "Stored Procedures",
             [
                 "sp_reserve_parking_slot: Implements pessimistic row-level locking (SELECT ... FOR UPDATE) to eliminate race conditions.",
                 "sp_process_vehicle_exit: Computes duration in minutes, applies EV/peak multipliers, and deducts user wallet atomically."
             ])

    add_card(s6, Inches(6.9), Inches(4.5), Inches(5.6), Inches(2.3),
             "Advanced Relational Queries",
             [
                 "Multi-Table INNER & LEFT JOINs connecting Users, Reservations, Slots, and Areas.",
                 "Correlated Subqueries identifying drivers spending above mall average.",
                 "GROUP BY and HAVING queries powering Chart.js peak usage graphs."
             ])

    # =========================================================================
    # SLIDE 7: DRIVER & USER PORTAL
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    bg7 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg7.fill.solid()
    bg7.fill.fore_color.rgb = c_cream
    bg7.line.fill.background()
    add_header(s7, "Customer Experience: The Driver Portal", "PORTAL 1")

    add_card(s7, Inches(0.8), Inches(1.9), Inches(3.6), Inches(4.8),
             "Interactive Bay Selection",
             [
                 "Visual grid filtering by mall, floor, and vehicle type.",
                 "Dedicated filters for EV Charging Docks and Two-Wheelers.",
                 "Displays real-time hourly rates and instant booking shortcuts.",
                 "Direct integration with ACID transactional reservation engine."
             ])

    add_card(s7, Inches(4.86), Inches(1.9), Inches(3.6), Inches(4.8),
             "Digital Wallet & Payments",
             [
                 "Prepaid wallet with simulated UPI / Card deposit gateways.",
                 "Automated checkout fee deduction upon gate clearance.",
                 "Eliminates cash queues and physical payment delays.",
                 "Detailed transaction history and downloadable PDF receipts."
             ])

    add_card(s7, Inches(8.93), Inches(1.9), Inches(3.6), Inches(4.8),
             "Digital Garage Management",
             [
                 "Register and manage multiple personal vehicles.",
                 "Link cars to active bookings and track session status.",
                 "Real-time countdown timer on active parking sessions.",
                 "Instant one-click cancellation for eligible reservations."
             ])

    # =========================================================================
    # SLIDE 8: 3D MAP & FIND MY CAR
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    bg8 = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg8.fill.solid()
    bg8.fill.fore_color.rgb = c_cream
    bg8.line.fill.background()
    add_header(s8, "Interactive Mall Map & Indoor Vehicle Wayfinding", "FLAGSHIP FEATURE")

    add_card(s8, Inches(0.8), Inches(1.9), Inches(5.6), Inches(2.3),
             "Multi-Floor Level Switching",
             [
                 "Basement 1 (Zone Gold): 4-Wheelers and EV Charging Docks.",
                 "Basement 2 (Zone Platinum): Standard 4-Wheeler bays.",
                 "Lower Ground (Zone Express): Two-Wheeler bays with dedicated lanes."
             ])

    add_card(s8, Inches(6.9), Inches(1.9), Inches(5.6), Inches(2.3),
             "Real-Time Ultrasonic Sensor States",
             [
                 "Green: Available for immediate parking.",
                 "Amber: Reserved by a customer currently in transit.",
                 "Red: Occupied with live vehicle present.",
                 "Pulsing radar blip indicates currently selected target vehicle."
             ])

    add_card(s8, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.3),
             "Interactive Bay Inspector Modal",
             [
                 "Click any bay on the floor map to trigger a glassmorphism modal.",
                 "Displays Bay Code, Section, Row, and EV charging compatibility.",
                 "For occupied bays: Reveals current occupant plate and car model.",
                 "For available bays: Provides a one-click reservation shortcut."
             ])

    add_card(s8, Inches(6.9), Inches(4.5), Inches(5.6), Inches(2.3),
             "Pedestrian Wayfinding Engine",
             [
                 "Enter any license plate (e.g., KA01MH1001) to locate parked vehicle.",
                 "Highlights target bay and plots walking route from Lobby B elevators.",
                 "Provides estimated walking time (2 mins) and navigational cues."
             ])

    # =========================================================================
    # SLIDE 9: WATCHMAN GATE TERMINAL
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    bg9 = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg9.fill.solid()
    bg9.fill.fore_color.rgb = c_cream
    bg9.line.fill.background()
    add_header(s9, "Gate Operations: Watchman Barrier Portal", "PORTAL 2")

    add_card(s9, Inches(0.8), Inches(1.9), Inches(3.6), Inches(4.8),
             "Touch-Optimized Terminal",
             [
                 "Engineered specifically for handheld tablets and mobile screens at entry booms.",
                 "High-contrast buttons for outdoor glare readability.",
                 "Instant switching between Inward Check-In and Outward Clearance."
             ])

    add_card(s9, Inches(4.86), Inches(1.9), Inches(3.6), Inches(4.8),
             "Sub-15s Barrier Check-In",
             [
                 "Enter 8-character booking code (e.g. PK-78A9B2) or scan license plate.",
                 "Instant validation against active database reservations.",
                 "Automatically triggers boom barrier open and starts session timer."
             ])

    add_card(s9, Inches(8.93), Inches(1.9), Inches(3.6), Inches(4.8),
             "Automated Exit Clearance",
             [
                 "Calculates exact duration down to the minute upon vehicle approach.",
                 "Verifies wallet balance or records cash settlement at gate.",
                 "Releases parking bay back to AVAILABLE in real-time.",
                 "Prevents gate tailgating and unauthorized exits."
             ])

    # =========================================================================
    # SLIDE 10: MALL ADMIN CONSOLE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    bg10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg10.fill.solid()
    bg10.fill.fore_color.rgb = c_cream
    bg10.line.fill.background()
    add_header(s10, "Operations & Intelligence: Mall Admin Portal", "PORTAL 3")

    add_card(s10, Inches(0.8), Inches(1.9), Inches(3.6), Inches(4.8),
             "Executive KPI Dashboard",
             [
                 "Live occupancy percentage across all 3 basement zones.",
                 "Active parking sessions counter and real-time revenue tally.",
                 "Registered vehicle distribution by category (4W, 2W, EV).",
                 "Immediate alerts on parking bay maintenance or violations."
             ])

    add_card(s10, Inches(4.86), Inches(1.9), Inches(3.6), Inches(4.8),
             "Chart.js Visual Analytics",
             [
                 "Doughnut Chart: Zone-by-zone real-time capacity utilization.",
                 "Bar Chart: Hourly peak traffic and arrival patterns.",
                 "Line Chart: 30-day cumulative revenue and collection trends.",
                 "Enables predictive staffing and tariff management for malls."
             ])

    add_card(s10, Inches(8.93), Inches(1.9), Inches(3.6), Inches(4.8),
             "Facility CRUD & SQL Demo",
             [
                 "Add, modify, or retire parking areas and individual bays.",
                 "Configure dynamic pricing tiers, peak multipliers, and EV rates.",
                 "Interactive SQL Lab: Run joins, subqueries, and views live.",
                 "Audit trail table inspecting all financial ledger entries."
             ])

    # =========================================================================
    # SLIDE 11: END-TO-END OPERATIONAL WORKFLOW
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    bg11 = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg11.fill.solid()
    bg11.fill.fore_color.rgb = c_cream
    bg11.line.fill.background()
    add_header(s11, "End-to-End Parking Lifecycle Workflow", "HOW IT WORKS")

    steps = [
        ("Step 1: Reservation", "Driver books Bay P-B1-02 via web portal. System locks row, verifies wallet, and generates 8-char booking code."),
        ("Step 2: Gate Check-In", "Driver reaches Phoenix Mall. Watchman verifies code at entry boom. Slot changes to OCCUPIED; session begins."),
        ("Step 3: Mall Wayfinding", "Shopper returns to basement. Uses 'Find My Car' with plate KA01MH1001. System renders walking route from Lobby B."),
        ("Step 4: Exit & Settlement", "Car reaches exit barrier. Duration calculated. Fee deducted from wallet. Barrier opens and slot is released.")
    ]

    for idx, (stitle, sdesc) in enumerate(steps):
        left = Inches(0.8 + idx * 2.95)
        card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.9), Inches(2.75), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = c_beige
        card.line.color.rgb = c_orange
        card.line.width = Pt(1.2)

        tb = s11.shapes.add_textbox(left + Inches(0.15), Inches(2.1), Inches(2.45), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"0{idx+1}"
        p1.font.name = "Georgia"
        p1.font.size = Pt(28)
        p1.font.bold = True
        p1.font.color.rgb = c_orange
        p1.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = stitle
        p2.font.name = "Georgia"
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = c_espresso
        p2.space_after = Pt(10)

        p3 = tf.add_paragraph()
        p3.text = sdesc
        p3.font.name = "Arial"
        p3.font.size = Pt(10)
        p3.font.color.rgb = c_charcoal

    # =========================================================================
    # SLIDE 12: DEMO & CONCLUSION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    bg12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg12.fill.solid()
    bg12.fill.fore_color.rgb = c_dark_bg
    bg12.line.fill.background()

    strip12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    strip12.fill.solid()
    strip12.fill.fore_color.rgb = c_orange
    strip12.line.fill.background()

    tb12 = s12.shapes.add_textbox(Inches(1.2), Inches(1.0), Inches(11), Inches(1.2))
    tf12 = tb12.text_frame
    p_c1 = tf12.paragraphs[0]
    p_c1.text = "LIVE SYSTEM DEMONSTRATION & VERIFICATION"
    p_c1.font.name = "Georgia"
    p_c1.font.size = Pt(26)
    p_c1.font.bold = True
    p_c1.font.color.rgb = c_white

    # Demo Accounts Box
    box_acc = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(2.4), Inches(5.2), Inches(4.2))
    box_acc.fill.solid()
    box_acc.fill.fore_color.rgb = c_card_dark
    box_acc.line.color.rgb = c_orange
    box_acc.line.width = Pt(1)

    tb_a = s12.shapes.add_textbox(Inches(1.4), Inches(2.6), Inches(4.8), Inches(3.8))
    tfa = tb_a.text_frame
    tfa.word_wrap = True
    pa_h = tfa.paragraphs[0]
    pa_h.text = "TESTING CREDENTIALS"
    pa_h.font.name = "Georgia"
    pa_h.font.size = Pt(14)
    pa_h.font.bold = True
    pa_h.font.color.rgb = c_orange
    pa_h.space_after = Pt(12)

    creds = [
        ("Driver Portal", "aarav.patel@gmail.com / user123", "Full driver booking, wallet, garage"),
        ("Watchman Terminal", "watchman / watchman123", "Barrier boom touch in/out gate"),
        ("Mall Admin", "admin / admin123", "Floor KPIs, Chart.js, slot CRUD")
    ]
    for role, cred, desc in creds:
        p = tfa.add_paragraph()
        p.text = f"{role}:"
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = c_beige
        
        p2 = tfa.add_paragraph()
        p2.text = f"  Login: {cred}\n  ({desc})"
        p2.font.name = "Arial"
        p2.font.size = Pt(9)
        p2.font.color.rgb = c_gray
        p2.space_after = Pt(8)

    # Demo Vehicles Box
    box_veh = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(2.4), Inches(5.2), Inches(4.2))
    box_veh.fill.solid()
    box_veh.fill.fore_color.rgb = c_card_dark
    box_veh.line.color.rgb = c_orange
    box_veh.line.width = Pt(1)

    tb_v = s12.shapes.add_textbox(Inches(7.1), Inches(2.6), Inches(4.8), Inches(3.8))
    tfv = tb_v.text_frame
    tfv.word_wrap = True
    pv_h = tfv.paragraphs[0]
    pv_h.text = "PRE-PARKED VEHICLES (FIND MY CAR)"
    pv_h.font.name = "Georgia"
    pv_h.font.size = Pt(14)
    pv_h.font.bold = True
    pv_h.font.color.rgb = c_orange
    pv_h.space_after = Pt(12)

    cars = [
        ("KA01MH1001", "Tata Nexon EV (Slot P-B1-02, Basement 1 Zone Gold - EV Dock)"),
        ("KA03CD4004", "Hyundai Creta (Slot P-B1-08, Basement 1 Zone Gold)"),
        ("KA05IJ7007", "Toyota Innova (Slot P-B2-04, Basement 2 Zone Platinum)"),
        ("KA06KL8008", "Royal Enfield Hunter (Slot P-LG-03, Lower Ground Express 2W)")
    ]
    for plate, cdesc in cars:
        p = tfv.add_paragraph()
        p.text = f"Plate: {plate}"
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = c_beige
        
        p2 = tfv.add_paragraph()
        p2.text = f"  {cdesc}"
        p2.font.name = "Arial"
        p2.font.size = Pt(9)
        p2.font.color.rgb = c_gray
        p2.space_after = Pt(8)

    output_path = os.path.join(os.path.dirname(__file__), 'ParkSmart_2.0_Project_Presentation.pptx')
    prs.save(output_path)
    print(f"==> PPTX Presentation Successfully Generated at: {output_path}")
    print(f"==> Size: {os.path.getsize(output_path) / 1024:.2f} KB | Total Slides: {len(prs.slides)}")
    return output_path

if __name__ == '__main__':
    create_presentation()
