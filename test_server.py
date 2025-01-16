"""
Server Connection Test Module

This module tests the robot's server functionality by attempting to create
and bind to the control port. It verifies that the server can properly
initialize and bind to the required network port.

Tests:
- Socket creation
- Port binding (2001)
- Socket cleanup
"""

import socket
import json

def test_server():
    """
    Tests the server's ability to bind to the control port.
    
    Returns:
        bool: True if binding successful, False otherwise
        
    The test:
    1. Creates a socket with address reuse enabled
    2. Attempts to bind to port 2001 on all interfaces
    3. Closes the socket after successful binding
    """
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Try to bind to the port
        server_socket.bind(('0.0.0.0', 2001))
        print("Successfully bound to port 2001")
        server_socket.close()
        return True
    except Exception as e:
        print(f"Error binding to port: {e}")
        return False

if __name__ == "__main__":
    test_server() 