import http.server
import socketserver

def launch():
    PORT = 1337
    DIRECTORY = "."
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f'Serving at port {PORT}')
        httpd.serve_forever()

launch()