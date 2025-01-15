import socket
import json

def test_server():
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