from wsgiref.simple_server import make_server
from dotenv import load_dotenv
from os import getenv


def app(environ, start_response):
    status = "200 OK"
    # 直接は関係ないけれど apiならContent-typeも異なる
    headers = [("Content-type", "application/json; charset=utf-8")]
    start_response(status, headers)
    return [b"done"]


load_dotenv()
PORT = int(getenv("DISPATCHER_PORT", 5001))
httpd = make_server("", PORT, app)
print(f"Serving on port {PORT}...")

# Serve until process is killed
httpd.serve_forever()
