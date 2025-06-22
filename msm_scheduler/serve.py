import os
import sys
import logging

from http.server import HTTPServer

from .application_http_request_handler import ApplicationHTTPRequestHandler

LOG_LEVEL = os.getenv("MSM_SCHEDULER_LOG_LEVEL", "info").lower()
LOG_LEVEL_MAP = {
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "info": logging.INFO,
}
logging.basicConfig(
    level=LOG_LEVEL_MAP.get(LOG_LEVEL, logging.INFO),
    format="[%(asctime)s] %(levelname)s - %(message)s",
)

host = '0.0.0.0'
port = int(sys.argv[1])

httpd = HTTPServer((host, port), ApplicationHTTPRequestHandler)
logging.info("Starting server on %s:%s", host, port)
httpd.serve_forever()
