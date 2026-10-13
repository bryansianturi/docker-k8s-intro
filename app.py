import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

import redis

db = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_response(404)
            self.end_headers()
            return

        try:
            visits = f"Visits: {db.incr('visits')}"
        except redis.exceptions.ConnectionError:
            visits = "No database connected"

        page = f"<h1>Hello from container {socket.gethostname()}</h1><p>{visits}</p>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(page.encode())


print("Server running on port 8000")
HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
