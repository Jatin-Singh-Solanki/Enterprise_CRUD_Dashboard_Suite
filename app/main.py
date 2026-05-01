from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
import mimetypes
from app.core.config import HOST, PORT, STATIC_DIR, TEMPLATE_DIR, APP_NAME
from app.core.response import send_html, send_json
from app.data.seed import seed_database
from app.routes.api import handle_get, handle_post, handle_patch, handle_delete

mimetypes.add_type("text/css", ".css")
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("video/mp4", ".mp4")


class AtlasNexusHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        if self.path.startswith("/api/") and handle_get(self):
            return
        clean_path = urlparse(self.path).path
        if clean_path in ["/", "/workspace"]:
            html = (TEMPLATE_DIR / "index.html").read_text(encoding="utf-8")
            send_html(self, html.replace("{{APP_NAME}}", APP_NAME))
            return
        if clean_path.startswith("/static/"):
            self.serve_static(clean_path)
            return
        send_json(self, {"error": "Route not found"}, 404)

    def do_POST(self):
        if handle_post(self):
            return
        send_json(self, {"error": "Route not found"}, 404)

    def do_PATCH(self):
        if handle_patch(self):
            return
        send_json(self, {"error": "Route not found"}, 404)

    def do_DELETE(self):
        if handle_delete(self):
            return
        send_json(self, {"error": "Route not found"}, 404)

    def serve_static(self, clean_path):
        relative = clean_path.replace("/static/", "", 1)
        file_path = (STATIC_DIR / relative).resolve()
        if not str(file_path).startswith(str(STATIC_DIR.resolve())) or not file_path.exists():
            send_json(self, {"error": "Static file not found"}, 404)
            return
        content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        body = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    seed_database()
    server = ThreadingHTTPServer((HOST, PORT), AtlasNexusHandler)
    print(f"{APP_NAME} running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
