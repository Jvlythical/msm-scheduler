import os
import pdb
import re

from mergedeep import merge
from urllib.parse import urlparse, parse_qs

from .routes import ROUTES
from .lib.simple_http_request_handler import SimpleHTTPRequestHandler

class ApplicationHTTPRequestHandler(SimpleHTTPRequestHandler):
    ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

    ### Method handlers

    def do_OPTIONS(self):
        self.render(
            plain = 'OK',
            status = 200
        )

    def do_GET(self):
        self.preprocess()

        merge(self.params, self.parse_query_params())

        if not self.route('GET'):
            return self.not_found()

    def preprocess(self):
        self.uri = urlparse(self.path)

        self.fullpath = self.path
        self.path = self.uri.path
        self.params = {}
        self.body = ''

    def route(self, method):
        for endpoint_handler in ROUTES[method]:
            path = endpoint_handler[0]

            matches = self.path == path if isinstance(path, str) else bool(re.match(path, self.path))

            if matches:
                handler = endpoint_handler[1]
                handler(self)
                return True

        return False

    def parse_query_params(self):
        query_params = parse_qs(self.uri.query)

        for key, value in query_params.items():
            if len(value) == 1:
                query_params[key] = value[0]

        return query_params
