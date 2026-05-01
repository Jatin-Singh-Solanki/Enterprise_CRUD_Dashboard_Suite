from app.core.database import connect, init_database

CUSTOMERS = [
    ("Nova Health Group", "Healthcare", "North America", "Abhinay", 420000, 91, "2026-11-20", "Active", "Enterprise renewal with analytics expansion"),
    ("BlueRiver Finance", "Finance", "North America", "Sarah", 365000, 86, "2026-10-12", "Active", "Fraud and compliance portfolio"),
    ("GreenGrid Energy", "Energy", "Asia Pacific", "David", 290000, 82, "2026-09-01", "Active", "Operational data modernization"),
    ("Skyline Retail", "Retail", "Europe", "Priya", 210000, 74, "2026-07-15", "Watch", "Design-heavy portal refresh"),
    ("Apex Logistics", "Logistics", "North America", "Rahul", 180000, 69, "2026-06-22", "Watch", "Legacy integration risk"),
    ("Orion Manufacturing", "Manufacturing", "Europe", "Maya", 255000, 88, "2026-12-05", "Active", "IoT reporting and maintenance insights"),
]

PROJECTS = [
    ("AI Claims Workflow Automation", 1, "Abhinay", "Active", "High", 230000, 126000, 71, "2026-01-10", "2026-08-20", "Medium", "Automates claims intake, validation, review queues, and leadership reporting."),
    ("Fraud Signal Intelligence Hub", 2, "Sarah", "Active", "Critical", 310000, 174000, 64, "2026-02-01", "2026-09-18", "High", "Centralized fraud signal scoring, analyst feedback, and alert triage."),
    ("Operational Data Quality Center", 3, "David", "Completed", "Medium", 125000, 118000, 100, "2025-11-04", "2026-04-20", "Low", "Rules-driven data quality checks with SLA trend reporting."),
    ("Customer 360 Portal Refresh", 4, "Priya", "Planning", "High", 175000, 32000, 28, "2026-04-01", "2026-11-01", "Medium", "Modern customer workspace with role-based dashboards and clean UI patterns."),
    ("Executive KPI Platform", 1, "Rahul", "Active", "Medium", 150000, 76000, 58, "2026-03-01", "2026-10-10", "Low", "Executive metric layer covering delivery, revenue, and risk outcomes."),
    ("API Modernization Program", 5, "Abhinay", "At Risk", "Critical", 260000, 197000, 52, "2026-01-25", "2026-07-31", "High", "Legacy service modernization with containerized deployment strategy."),
    ("Predictive Maintenance Console", 6, "Maya", "Active", "High", 215000, 99000, 61, "2026-02-14", "2026-09-30", "Medium", "Equipment health visibility using sensor events and service history."),
]

TASKS = [
    (1, "Build document ingestion API", "Maya", "In Progress", 8, "2026-05-14"),
    (1, "Finalize workflow approval UI", "Chris", "Review", 5, "2026-05-18"),
    (2, "Tune anomaly detection rules", "Alex", "In Progress", 13, "2026-05-21"),
    (2, "Create fraud analyst dashboard", "Neha", "To Do", 10, "2026-05-26"),
    (3, "Publish data quality SLA report", "David", "Done", 3, "2026-04-19"),
    (4, "Design customer profile experience", "Priya", "In Progress", 6, "2026-05-17"),
    (5, "Add executive forecast metrics", "Rahul", "Review", 4, "2026-05-16"),
    (6, "Containerize legacy services", "Abhinay", "Blocked", 12, "2026-05-24"),
    (7, "Create equipment alert policy", "Maya", "To Do", 8, "2026-05-30"),
]

RISKS = [
    (1, "OCR model accuracy drops on scanned PDFs", "Medium", 45, 70, "Add confidence scoring and human review queue", "Abhinay", "Open"),
    (2, "False positive fraud alerts may increase analyst load", "High", 60, 85, "Introduce threshold tuning and feedback loop", "Sarah", "Open"),
    (4, "Customer branding feedback not finalized", "Medium", 50, 55, "Set weekly design review checkpoint", "Priya", "Monitoring"),
    (6, "Legacy dependency blocks Kubernetes rollout", "High", 70, 90, "Create adapter layer and phased cutover", "Abhinay", "Open"),
    (7, "Sensor data delay can reduce alert confidence", "Medium", 40, 66, "Buffer events and show data freshness indicators", "Maya", "Monitoring"),
]

INVOICES = [
    (1, "INV-1001", 76000, "Paid", "2026-04-10"),
    (2, "INV-1002", 54000, "Pending", "2026-05-20"),
    (3, "INV-1003", 43000, "Paid", "2026-04-28"),
    (4, "INV-1004", 22000, "Overdue", "2026-04-30"),
    (5, "INV-1005", 39000, "Pending", "2026-05-25"),
    (6, "INV-1006", 61000, "Paid", "2026-05-04"),
]

MILESTONES = [
    (1, "Claims document classifier release", "2026-06-15", "On Track", 88),
    (2, "Fraud model production tuning", "2026-06-28", "Watch", 71),
    (4, "Customer UX prototype approval", "2026-05-29", "Watch", 64),
    (6, "Legacy adapter pilot", "2026-06-10", "At Risk", 58),
    (7, "Maintenance alert beta launch", "2026-07-02", "On Track", 82),
]


def seed_database(force=False):
    init_database()
    with connect() as connection:
        existing = connection.execute("SELECT COUNT(*) total FROM customers").fetchone()["total"]
        if existing and not force:
            return
        for table in ["audit_logs", "milestones", "invoices", "risks", "tasks", "projects", "customers"]:
            connection.execute(f"DELETE FROM {table}")
        connection.executemany("INSERT INTO customers(name, industry, region, owner, contract_value, health_score, renewal_date, status, notes) VALUES(?,?,?,?,?,?,?,?,?)", CUSTOMERS)
        connection.executemany("INSERT INTO projects(name, customer_id, owner, status, priority, budget, spent, progress, start_date, due_date, risk_level, description) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", PROJECTS)
        connection.executemany("INSERT INTO tasks(project_id, title, assignee, stage, effort, due_date) VALUES(?,?,?,?,?,?)", TASKS)
        connection.executemany("INSERT INTO risks(project_id, title, severity, probability, impact, mitigation, owner, status) VALUES(?,?,?,?,?,?,?,?)", RISKS)
        connection.executemany("INSERT INTO invoices(customer_id, invoice_no, amount, status, due_date) VALUES(?,?,?,?,?)", INVOICES)
        connection.executemany("INSERT INTO milestones(project_id, title, target_date, status, confidence) VALUES(?,?,?,?,?)", MILESTONES)
        connection.execute("INSERT INTO audit_logs(event_type, message) VALUES('SYSTEM', 'Database seeded with enterprise demo data')")
