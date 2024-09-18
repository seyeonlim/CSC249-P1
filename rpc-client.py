import socket;

# Client will connect to a server running on localhost (same machine)
HOST = "127.0.0.1"
PORT = 65432

def run_client():
    print("Client starting - connecting to server at IP", HOST, "and port", PORT)
    # Create a IPv4 (AF_INET) TCP socket (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server
        s.connect((HOST, PORT))
        print("Connection established.")
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
    
    if msg == "":
        sock.sendall(b"")
        return False
    
    print(f"Sending message '{msg}' to server...")
    # Send msg to the server
    sock.sendall(msg.encode('utf-8'))
    print("Message sent, waiting for reply...")
    # Wait for reply from the server 
    reply = sock.recv(1024)
    if not reply:
        print("No reply received from server, closing connection.")
        return False
    else:
        print(f"Received reply from server: {reply.decode('utf-8')}")
        return reply

if __name__ == "__main__":
     # Start the client
    run_client() 
    print("Client is done, exiting...")
