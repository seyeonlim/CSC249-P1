import socket
from datetime import datetime, timedelta

HOST = "127.0.0.1"
PORT = 65432

def parse_msg(msg):
    words = msg.split()
    operation, param1, param2 = words
    return operation, param1, param2

def get_days_between(date1, date2):
    d1 = datetime.strptime(date1, "%Y-%m-%d")
    d2 = datetime.strptime(date2, "%Y-%m-%d")
    delta = d2 - d1
    return delta

def add_days(date, days):
    d = datetime.strptime(date, "%Y-%m-%d")
    d += timedelta(days=days)
    return d.strftime("%Y-%m-%d")

print("server starting - listening for connections at IP", HOST, "and port", PORT)
# Create a IPv4 (AF_INET) TCP socket (SOCK_STREAM)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind the socket to the address and port
    s.bind((HOST, PORT))
    # Listen for client connections
    s.listen()
    # If a client connects, accept the connection
    conn, addr = s.accept()
    with conn:
        print(f"Connected established with {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received client message: '{data}' [{len(data)} bytes]")
            print("Parsing message...")

            # Decode msg - otherwise the input is in bytes
            data = data.decode('utf-8')
            
            operation, param1, param2 = parse_msg(data)
            print(f"Operation: {operation}, Param1: {param1}, Param2: {param2}")
            response = ""
            if operation == "get_days_between":
                response = f"The number of days between {param1} and {param2} is {get_days_between(param1, param2).days} days."
            elif operation == "add_days":
                response = f"The date after adding {param2} days to {param1} is {add_days(param1, int(param2))}."
            else:
                response = "Invalid operation"
            print("Sending response to client...")
            conn.sendall(response.encode('utf-8')) 
            print("Response sent to client!")

print("server is done!")
