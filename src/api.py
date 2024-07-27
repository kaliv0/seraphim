import inspect
import os

from jinja2 import Environment, FileSystemLoader
from parse import parse
from webob import Request, Response
from requests import Session as RequestsSession  # TODO: do we need aliases?
from whitenoise import WhiteNoise
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter


class API:
    def __init__(self, templates_dir=None, static_dir=None):
        self.routes = {}
        self.exception_handler = None

        # TODO: fix, handle default dirs
        if templates_dir is not None:
            self.templates_env = Environment(
                loader=FileSystemLoader(os.path.abspath(templates_dir))
            )
        if static_dir is not None:
            self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)

    def __call__(self, environ, start_response):
        # return self.wsgi_app(environ, start_response)
        return self.whitenoise(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def template(self, template_name, context=None):
        if context is None:
            context = {}
        return self.templates_env.get_template(template_name).render(**context)

    def add_exception_handler(self, exception_handler):
        self.exception_handler =  exception_handler

    def add_route(self, path, handler):
        assert path not in self.routes, "Route already exists"
        self.routes[path] = handler

    def route(self, path):
        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)
        try:
            if handler is not None:
                if inspect.isclass(handler):
                    # TODO: do we need to call handler?
                    handler = getattr(handler(), request.method.lower(), None)
                    if handler is None:
                        raise AttributeError(
                            f"Method not allowed: {request.method}"
                        )  # TODO: should we return 500?
                handler(request, response, **kwargs)
            else:
                self.default_response(response)
        except Exception as e:  # TODO: change exception type
            if self.exception_handler is None:
                raise e
            else:
                self.exception_handler(request, response, e)
        return response

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    @staticmethod
    def default_response(response):
        response.status_code = 404
        response.text = "Not found."

    ###################
    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session
