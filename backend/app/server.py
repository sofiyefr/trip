from http.server import SimpleHTTPRequestHandler, HTTPServer

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Serving on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()