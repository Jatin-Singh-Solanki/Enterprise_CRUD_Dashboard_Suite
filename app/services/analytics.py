from app.core.database import connect

TABLES = {
    "customers": ["name", "industry", "region", "owner", "contract_value", "health_score", "renewal_date", "status", "notes"],
    "projects": ["name", "customer_id", "owner", "status", "priority", "budget", "spent", "progress", "start_date", "due_date", "risk_level", "description"],
    "tasks": ["project_id", "title", "assignee", "stage", "effort", "due_date"],
    "risks": ["project_id", "title", "severity", "probability", "impact", "mitigation", "owner", "status"],
    "invoices": ["customer_id", "invoice_no", "amount", "status", "due_date"],
    "milestones": ["project_id", "title", "target_date", "status", "confidence"],
}


def list_records(table):
    queries = {
        "projects": """
            SELECT p.*, c.name customer_name
            FROM projects p LEFT JOIN customers c ON c.id = p.customer_id
            ORDER BY p.id DESC
        """,
        "customers": "SELECT * FROM customers ORDER BY id DESC",
        "tasks": """
            SELECT t.*, p.name project_name
            FROM tasks t LEFT JOIN projects p ON p.id = t.project_id
            ORDER BY t.id DESC
        """,
        "risks": """
            SELECT r.*, p.name project_name
            FROM risks r LEFT JOIN projects p ON p.id = r.project_id
            ORDER BY r.id DESC
        """,
        "invoices": """
            SELECT i.*, c.name customer_name
            FROM invoices i LEFT JOIN customers c ON c.id = i.customer_id
            ORDER BY i.id DESC
        """,
        "milestones": """
            SELECT m.*, p.name project_name
            FROM milestones m LEFT JOIN projects p ON p.id = m.project_id
            ORDER BY m.id DESC
        """,
        "audit_logs": "SELECT * FROM audit_logs ORDER BY id DESC LIMIT 80",
    }
    if table not in queries:
        raise ValueError("Unsupported table")
    with connect() as connection:
        return connection.execute(queries[table]).fetchall()


def create_record(table, payload):
    fields = TABLES[table]
    values = [payload.get(field) for field in fields]
    placeholders = ",".join("?" for _ in fields)
    with connect() as connection:
        cursor = connection.execute(
            f"INSERT INTO {table}({','.join(fields)}) VALUES({placeholders})",
            values,
        )
        connection.execute(
            "INSERT INTO audit_logs(event_type, message) VALUES(?, ?)",
            ("CREATE", f"Created {table[:-1]} #{cursor.lastrowid}"),
        )
        return {"id": cursor.lastrowid}


def update_record(table, record_id, payload):
    fields = [field for field in TABLES[table] if field in payload]
    if not fields:
        return {"updated": False}
    assignments = ", ".join(f"{field} = ?" for field in fields)
    values = [payload[field] for field in fields] + [record_id]
    with connect() as connection:
        connection.execute(f"UPDATE {table} SET {assignments} WHERE id = ?", values)
        connection.execute(
            "INSERT INTO audit_logs(event_type, message) VALUES(?, ?)",
            ("UPDATE", f"Updated {table[:-1]} #{record_id}"),
        )
    return {"updated": True}


def delete_record(table, record_id):
    with connect() as connection:
        connection.execute(f"DELETE FROM {table} WHERE id = ?", (record_id,))
        connection.execute(
            "INSERT INTO audit_logs(event_type, message) VALUES(?, ?)",
            ("DELETE", f"Deleted {table[:-1]} #{record_id}"),
        )
    return {"deleted": True}


def dashboard():
    projects = list_records("projects")
    customers = list_records("customers")
    tasks = list_records("tasks")
    risks = list_records("risks")
    invoices = list_records("invoices")
    milestones = list_records("milestones")
    logs = list_records("audit_logs")
    budget = sum(float(project["budget"]) for project in projects)
    spent = sum(float(project["spent"]) for project in projects)
    avg_progress = round(sum(int(project["progress"]) for project in projects) / max(len(projects), 1), 1)
    avg_health = round(sum(int(customer["health_score"]) for customer in customers) / max(len(customers), 1), 1)
    open_risks = len([risk for risk in risks if risk["status"] != "Closed"])
    pending_revenue = sum(float(invoice["amount"]) for invoice in invoices if invoice["status"] != "Paid")
    forecast = max(50, min(98, round((avg_progress * 0.45) + (avg_health * 0.35) + ((100 - open_risks * 5) * 0.2))))
    return {
        "summary": {
            "projects": len(projects),
            "customers": len(customers),
            "budget": budget,
            "spent": spent,
            "avg_progress": avg_progress,
            "avg_health": avg_health,
            "open_risks": open_risks,
            "pending_revenue": pending_revenue,
            "forecast": forecast,
        },
        "projects": projects,
        "customers": customers,
        "tasks": tasks,
        "risks": risks,
        "invoices": invoices,
        "milestones": milestones,
        "logs": logs,
    }
