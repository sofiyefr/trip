from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

# main.py

def main():
    print("Hello, World!")

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Serving on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
    run_server()
    # Ensure the server serves files from the current directory
    os.chdir('/Users/sofia/trip/back')