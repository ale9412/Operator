import re
import socket


class TCPInterfaceClient:

    def __init__(self,addr,port):
        self.HOST = addr
        self.PORT = port
        # Initializate socket object
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.HOST,self.PORT))

    def close_connection(self):
        self.sock.close()
 

    def send(self,stream):
        self.sock.sendall(stream)

    def recieve(self):
        recvd = self.sock.recv(4096)
        return recvd.decode()



class Client:

    def __init__(self):
        # Expression to parse matematical operations
        self.regex = r'(\d+\s[+*-/]\s)+\d+'
    
    def is_valid(self,op):
        pattern = re.compile(self.regex)
        return pattern.match(op)

    def make_stream(self,operations_list):
        return bytes(','.join(operation.strip() for operation in operations_list).encode('utf-8'))
    
    def start(self):
        operation_file = open("operations.txt")
        while True:
            # Read in batches and send. Read the entire file could be memory expensive
            # and read it line by line to slow.
            lines = operation_file.readlines(4000)
            if not lines:
            # If the end of the file was reached break the loop
                break

            for operation in lines:
                # Clean the operations list, to contain only valid operations
                if not self.is_valid(operation):
                    # Remove operation from the list
                    lines.remove(operation)

            # Make data stream to send over the socket connection 
            stream = self.make_stream(lines)

            # Connect to the server, send operation and wait for response
            sock = TCPInterfaceClient("localhost",8000)
            sock.connect()
            sock.send(stream)
            # Wait until recieved entire information
            results = sock.recieve()
            sock.close_connection()

            # Log results to log file
        
        operation_file.close()
        
if __name__ == "__main__":

    client = Client()
    client.start()

# Execution time 12.36 seconds

##  Para el test    
##    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
##    # Connect to server and send data
##        sock.connect(('localhost', 8000))
##        sock.sendall(bytes('5+8*2,9-7+8/2*5,5*8+7/2', "utf-8"))
##
##        # Receive data from the server and shut down
##        received = str(sock.recv(1024), "utf-8")
##        print(received)


    
