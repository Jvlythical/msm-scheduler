import sys

from http.server import HTTPServer

from .application_http_request_handler import ApplicationHTTPRequestHandler

host = '0.0.0.0'
port = int(sys.argv[1])

httpd = HTTPServer((host, port), ApplicationHTTPRequestHandler)
httpd.serve_forever()
