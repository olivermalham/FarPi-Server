import os

# Tornado server settings
# TODO: This needs to be cleaned up
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "../html/"),
    "default_filename": "index.html",
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": False,
}

# Web server paths
paths = {}

# The TCP/IP Port number that the server will listen on
port = 8888
