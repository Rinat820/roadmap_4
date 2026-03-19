from jinja2 import Environment, FileSystemLoader

import traceback
import logging


logger = logging.getLogger(__name__)


class ResponseBuilder:
    env = Environment(loader=FileSystemLoader("src/view/tennis-scoreboard-html-layouts"))
    
    @classmethod
    def render(cls, status: str, template_name: str, **context):
        logger.info(f"Render: {template_name}", stacklevel=2)
        
        template = cls.env.get_template(template_name)
        rendered_html = template.render(**context).encode("utf-8")
        
        headers = [
            ("Content-Type", "text/html; charset=utf-8")
        ]
        return status, headers, [rendered_html]

    @staticmethod
    def redirect(status: str, location: str):
        logger.info(f"Redirect -> {location}", stacklevel=2)
        
        return status, [("Location", location)], [b""]

    @classmethod
    def build_error_response(cls, status: str, template, error_text="", **context):
        stack = traceback.extract_stack()
        chain = " -> ".join([f"{f.filename.split('/')[-1]}:{f.name}" for f in stack[-4:-1]])
        logger.warning(f"ERROR_RESP | PATH: {chain} | MSG: {error_text}")
        
        if status.startswith("500"):
            return status, [("Content-Type", "text/plain")], [b"Internal Server Error"]
        
        if status.startswith("404"):
            return cls.render(status, "404.html")
        
        return cls.render(status, template, error=error_text, **context)