import socket
from datetime import datetime, timedelta

HOST = "127.0.0.1"
PORT = 65432

def date_valid(date):
    # Check if the date is in the format YYYY-MM-DD
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def parse_msg(msg):
    # Parse the message into operation and parameters
    words = msg.split()

    # If the length is not 3, the input is invalid
    if len(words) != 3:
        return "Invalid command format. Please use the format: <command> <arg1> <arg2>"
    
    # Assign the operation and parameters from msg
    operation, param1, param2 = words 

    possible_operations = ["get_days_between", "add_days"]
    if operation not in possible_operations:
        return f"Operation '{operation}' is invalid. Possible operations are: 1. get_days_between; 2. add_days"
    
    if operation == "get_days_between":
        if not (date_valid(param1) and date_valid(param2)):
            return "Invalid date format. Please use an existing date and format the date in YYYY-MM-DD."
    elif operation == "add_days":
        if not date_valid(param1):
            return "Invalid date format. Please use an existing date and format the date in YYYY-MM-DD."
        if not param2.isdigit():
            return "Invalid number of days. Number of days should be an integer."

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
                print("Received empty input from client")
                conn.sendall("Empty input received".encode('utf-8'))
                break
            print(f"Received client message: '{data.decode('utf-8')}' [{len(data)} bytes]")
            print("Parsing message...")

            # Decode msg - otherwise the input is in bytes
            data = data.decode('utf-8')
            
            # Parse msg and check input validity. Error (str) will be returned when msg is invalid.
            result = parse_msg(data)
            if isinstance(result, str):
                # Print error message
                print("Invalid input from client. Sending error message...")
                conn.sendall(result.encode('utf-8'))
                continue
            else:
                operation, param1, param2 = result
                print(f"Msg parsed and validity checked. Operation: {operation}, Param1: {param1}, Param2: {param2}")

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

print("Server is done!")
