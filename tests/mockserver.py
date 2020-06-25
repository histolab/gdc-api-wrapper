# encoding: utf-8

import json
import re
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import requests


class MockServerRequestHandler(BaseHTTPRequestHandler):
    API_PATTERN = re.compile(r"/data")

    def do_GET(self):
        if re.search(self.API_PATTERN, self.path):
            # Add response status code.
            self.send_response(requests.codes.ok)

            # Add response headers.
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()

            # Add response content.
            response_content = json.dumps([])
            self.wfile.write(response_content.encode("utf-8"))
            return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port):
    mock_server = HTTPServer(("localhost", port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()
