"""
Robot Control Web Server
-----------------------
A proxy server that handles serving the web interface and forwarding API requests 
to the Flask backend. This server acts as a bridge between the web client and 
the robot control services.

Key Features:
- Serves the robot control web interface
- Proxies API requests to Flask backend
- Handles CORS and request forwarding
- Automatic port selection if default is in use
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import socket
import sys
import urllib.request
import json

class RobotControlProxyHandler(SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler that serves the web interface and proxies API requests.
    Inherits from SimpleHTTPRequestHandler to handle static file serving.
    """
    
    # Flask backend URL
    FLASK_BASE_URL = "http://localhost:5000"

    def end_headers(self):
        """Add CORS headers to allow cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        """
        Handle GET requests:
        - Serve the main web interface
        - Forward API requests to Flask backend
        - Handle static file serving
        """
        # Forward requests for main page to Flask
        if self.path == '/' or self.path == '/robot_control.html':
            try:
                # Forward request to Flask backend
                flask_url = f"{self.FLASK_BASE_URL}{self.path}"
                with urllib.request.urlopen(flask_url) as response:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(response.read())
            except urllib.error.HTTPError as e:
                print(f"Flask error: {e.read().decode()}")  # Log actual error
                self.send_error(500, f"Error proxying to Flask app: {str(e)}")
            except Exception as e:
                print(f"Proxy error: {str(e)}")  # Log any other errors
                self.send_error(500, f"Error proxying to Flask app: {str(e)}")
        else:
            # Serve static files directly
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        """
        Handle POST requests:
        - Forward motor control commands to Flask
        - Forward servo control commands to Flask
        """
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        # Route requests based on endpoint
        if self.path == '/motor' or self.path == '/servo':
            try:
                # Forward request to Flask backend
                req = urllib.request.Request(
                    f"{self.FLASK_BASE_URL}{self.path}",
                    data=post_data,
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req) as response:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(response.read())
            except Exception as e:
                self.send_error(500, f"Error proxying to Flask app: {str(e)}")
        else:
            self.send_error(404, "Endpoint not found")

def start_server(port=8001):
    """
    Start the web server with automatic port fallback.
    
    Args:
        port (int): The port to start the server on (default: 8001)
        
    The server will automatically try the next port if the specified port is in use.
    """
    try:
        # Print current working directory for debugging
        print(f"Current directory: {os.getcwd()}")
        
        # Change to the directory containing the HTML file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Changing to directory: {script_dir}")
        os.chdir(script_dir)
        
        # List directory contents for debugging
        print("Directory contents:")
        print(os.listdir('.'))
        
        # Create and start server
        print(f"Attempting to start server on port {port}...")
        server = HTTPServer(('', port), RobotControlProxyHandler)
        
        print(f"Server started successfully!")
        print(f"Local URL: http://localhost:{port}/robot_control.html")
        print(f"Network URL: http://192.168.68.80:{port}/robot_control.html")
        print("Press Ctrl+C to stop the server")
        
        server.serve_forever()
        
    except socket.error as e:
        if e.errno == 98:  # Address already in use
            print(f"Port {port} is already in use. Trying port {port + 1}")
            start_server(port + 1)
        else:
            print(f"Error starting server: {e}")
            print(f"Error details: {str(e)}")
            sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        # Verify required files exist
        if not os.path.exists('robot_control.html'):
            print("Warning: robot_control.html not found in current directory!")
        
        # Start the server
        start_server()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0) 