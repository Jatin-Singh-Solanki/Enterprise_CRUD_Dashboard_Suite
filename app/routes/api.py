import csv
import io
import json
from urllib.parse import urlparse
from app.core.response import send_json
from app.services.analytics import dashboard, list_records, create_record, update_record, delete_record, TABLES


def read_body(handler):
    length = int(handler.headers.get("Content-Length", 0))
    if length == 0:
        return {}
    return json.loads(handler.rfile.read(length).decode("utf-8"))


def parse_path(path):
    parts = [part for part in urlparse(path).path.split("/") if part]
    return parts


def handle_get(handler):
    parts = parse_path(handler.path)
    if parts == ["api", "dashboard"]:
        send_json(handler, dashboard())
        return True
    if len(parts) == 2 and parts[0] == "api" and parts[1] in [*TABLES.keys(), "audit_logs"]:
        send_json(handler, list_records(parts[1]))
        return True
    if len(parts) == 3 and parts[0] == "api" and parts[1] == "export" and parts[2] in [*TABLES.keys(), "audit_logs"]:
        rows = list_records(parts[2])
        output = io.StringIO()
        if rows:
            writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        body = output.getvalue().encode("utf-8")
        handler.send_response(200)
        handler.send_header("Content-Type", "text/csv")
        handler.send_header("Content-Disposition", f"attachment; filename={parts[2]}.csv")
        handler.send_header("Content-Length", str(len(body)))
        handler.end_headers()
        handler.wfile.write(body)
        return True
    return False


def handle_post(handler):
    parts = parse_path(handler.path)
    if len(parts) == 2 and parts[0] == "api" and parts[1] in TABLES:
        send_json(handler, create_record(parts[1], read_body(handler)), 201)
        return True
    return False


def handle_patch(handler):
    parts = parse_path(handler.path)
    if len(parts) == 3 and parts[0] == "api" and parts[1] in TABLES:
        send_json(handler, update_record(parts[1], int(parts[2]), read_body(handler)))
        return True
    return False


def handle_delete(handler):
    parts = parse_path(handler.path)
    if len(parts) == 3 and parts[0] == "api" and parts[1] in TABLES:
        send_json(handler, delete_record(parts[1], int(parts[2])))
        return True
    return False
