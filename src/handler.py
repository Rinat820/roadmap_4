from urllib.parse import parse_qs


class BaseHandler:
    @staticmethod
    def _parse_form_data(environ):
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError, TypeError):
            content_length = 0
            
        if content_length > 0:
            body = environ['wsgi.input'].read(content_length).decode('utf-8')
            return parse_qs(body)
        
        return {}

    @staticmethod
    def _parse_query_params(environ):
        query_string = environ.get('QUERY_STRING', '')

        if not query_string:
            return {}    

        return parse_qs(query_string)