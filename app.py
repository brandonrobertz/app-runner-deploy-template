"""
A no-dependency example application that runs on whatever port specified
by the PORT environment variable, or 8000. It prints out all the environment
variables seen.
"""
import os
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server


# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    ret = [
        ("%s: %s\n" % (key, value)).encode("utf-8")
        for key, value in environ.items()
        if "secret" not in key.lower()
    ]
    return ret


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    with make_server('', port, simple_app) as httpd:
        print(f"Serving on port {port}...")
        httpd.serve_forever()
