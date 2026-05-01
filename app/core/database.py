import sqlite3
from contextlib import contextmanager
from app.core.config import DB_PATH, DATA_DIR

DATA_DIR.mkdir(parents=True, exist_ok=True)


def row_to_dict(cursor, row):
    return {column[0]: row[index] for index, column in enumerate(cursor.description)}


@contextmanager
def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = row_to_dict
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def init_database():
    schema = """
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        industry TEXT NOT NULL,
        region TEXT NOT NULL,
        owner TEXT NOT NULL,
        contract_value REAL NOT NULL,
        health_score INTEGER NOT NULL,
        renewal_date TEXT NOT NULL,
        status TEXT NOT NULL,
        notes TEXT DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        customer_id INTEGER NOT NULL,
        owner TEXT NOT NULL,
        status TEXT NOT NULL,
        priority TEXT NOT NULL,
        budget REAL NOT NULL,
        spent REAL NOT NULL,
        progress INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        risk_level TEXT NOT NULL,
        description TEXT DEFAULT '',
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    );
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        assignee TEXT NOT NULL,
        stage TEXT NOT NULL,
        effort INTEGER NOT NULL,
        due_date TEXT NOT NULL,
        FOREIGN KEY(project_id) REFERENCES projects(id)
    );
    CREATE TABLE IF NOT EXISTS risks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        severity TEXT NOT NULL,
        probability INTEGER NOT NULL,
        impact INTEGER NOT NULL,
        mitigation TEXT NOT NULL,
        owner TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY(project_id) REFERENCES projects(id)
    );
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        invoice_no TEXT NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        due_date TEXT NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    );
    CREATE TABLE IF NOT EXISTS milestones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        target_date TEXT NOT NULL,
        status TEXT NOT NULL,
        confidence INTEGER NOT NULL,
        FOREIGN KEY(project_id) REFERENCES projects(id)
    );
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """
    with connect() as connection:
        connection.executescript(schema)


def log_event(event_type, message):
    with connect() as connection:
        connection.execute(
            "INSERT INTO audit_logs(event_type, message) VALUES(?, ?)",
            (event_type, message),
        )
