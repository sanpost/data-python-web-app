import os
import re
import sys
from math import lcm
from urllib.parse import parse_qs

# Duże liczby: wyłącz limit konwersji int<->str (Python 3.11+)
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

EMAIL = os.environ.get("APP_EMAIL", "md.smith2@mail-fr.com").lower()
SLUG = re.sub(r"[^A-Za-z0-9]", "_", EMAIL)
SUFFIX = "/" + SLUG

DIGITS = re.compile(r"[0-9]{1,100000}")
HEADERS = [("Content-Type", "text/plain; charset=utf-8")]


def parse(v):
    if v and DIGITS.fullmatch(v):
        return int(v)
    return None


def app(environ, start_response):
    if environ["REQUEST_METHOD"] not in ("GET", "HEAD"):
        start_response("405 Method Not Allowed", HEADERS)
        return [b"NaN"]

    if not environ.get("PATH_INFO", "").rstrip("/").endswith(SUFFIX):
        start_response("404 Not Found", HEADERS)
        return [b"Not found"]

    q = parse_qs(environ.get("QUERY_STRING", ""))
    x = parse(q.get("x", [None])[0])
    y = parse(q.get("y", [None])[0])

    body = b"NaN" if x is None or y is None else str(lcm(x, y)).encode()
    start_response("200 OK", HEADERS + [("Content-Length", str(len(body)))])
    return [body]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    port = int(os.environ.get("PORT", 8000))
    print(f"http://localhost:{port}{SUFFIX}?x=4&y=6")
    make_server("0.0.0.0", port, app).serve_forever()