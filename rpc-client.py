import socket;
from datetime import datetime

# Client will connect to a server running on localhost (same machine)
HOST = "127.0.0.1"
PORT = 65432

def run_client():
    print("client starting - connecting to server at IP", HOST, "and port", PORT)
    # Create a IPv4 (AF_INET) TCP socket (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server
        s.connect((HOST, PORT))
        print("connection established")
        while True:
            if not talk_to_server(s):
                break

def talk_to_server(sock):
    # Get user input
    msg = input('''
Enter message to send to server.
Possible commannds are:
    1. get_days_between <date1> <date2>
        -> This will return the number of days between the two dates.
    2. add_days <date> <days>
        -> This will return the date after adding the given number of days.
    3. quit
        -> Disconnect from the server.\n
''')
    if msg == "quit":
        return False
    
    # Parse msg and check input validity before sending it to the server. Error (str) will be returned when msg is invalid.
    result = parse_msg(msg)
    if isinstance(result, str):
        # Print error message
        print(result)
        return True
    else:
        operation, param1, param2 = result
        print(f"Msg parsed and validity checked. operation: {operation}, param1: {param1}, param2: {param2}")
    
    print(f"Sending message '{msg}' to server")
    # Send msg to the server
    sock.sendall(msg.encode('utf-8'))
    print("Message sent, waiting for reply")
    # Wait for reply from the server 
    reply = sock.recv(1024)
    if not reply:
        return False
    else:
        print(f"Received reply from server: {reply}")
        return reply

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
            return "Invalid date format. Please format the date in YYYY-MM-DD."
    elif operation == "add_days":
        if not date_valid(param1):
            return "Invalid date format. Please format the date in YYYY-MM-DD."
        if not param2.isdigit():
            return "Invalid number of days. Number of days should be an integer."
    
    return operation, param1, param2

if __name__ == "__main__":
     # Start the client
    run_client() 
    print("client is done, exiting...")
