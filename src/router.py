from src.view.responses import ResponseBuilder
from src.new_match.controller import NewMatchController

import mimetypes
from pathlib import Path

import logging


STATIC_DIR = Path(__file__).parent.parent / "src" / "view" / "tennis-scoreboard-html-layouts"
SKIP_LOG_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.ico')


logger = logging.getLogger(__name__)


class Router:
    def handle_request(self, environ, start_response):
        path = environ.get("PATH_INFO", "/")
        method = environ.get("REQUEST_METHOD", "GET")

        if not path.lower().endswith(SKIP_LOG_EXTENSIONS):
            logger.info(f"Incoming request: {environ['REQUEST_METHOD']} {path}")


        if path == "/":
            status, headers, body = ResponseBuilder.render("200 OK", "index.html")

        elif path == "/new-match":
            if method == "POST":
                status, headers, body = NewMatchController.create_match(environ)
            
            else:
                status, headers, body = NewMatchController.render_page(environ)
            
        elif path == "/favicon.ico":
            status, headers, body = ("404 Not Found", [("Content-Type", "text/plain")], [b""])


        else:
            clean_path = path.lstrip("/")
            file_path = STATIC_DIR / clean_path
            
            if clean_path and file_path.is_file():
                content = file_path.read_bytes()
                mime_type, _ = mimetypes.guess_type(str(file_path))
                headers = [("Content-Type", mime_type or "application/octet-stream")]
                start_response("200 OK", headers)
                return [content]
            else:
                status, headers, body = ResponseBuilder.render("404 Not Found", "404.html")


        start_response(status, headers)
        return body
    
    

