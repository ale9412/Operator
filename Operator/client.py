import re
import socket


class TCPInterfaceClient:
    """
    Class to create a socket object that will handle data over a TCP connection

    To receive data over a TCP connection four approaches could be made:

        1 - Use as aprotocol that only one message will be sent per connection,
        and once a message has been sent, the sender will inmidiately close the socket

        2 - Use fixed lenght messages. The receiver will read the number of bytes and
        know that it has the whole msg.

        3 - Prefix the msg length at the beginning fo the stream. The receiver will read
        the length from the stream, then it will read the indicated amount of bytes.

        4 - Use flags delimiters to indicate end of the stream. The receiver will scan 
        the incoming stream for the delimiter, and know it has the whole msg.

        Approaches 1 and 2 are the most simple ones but made inefficient use of resources.
        Option 3 it is consider the best approach but the most hard to code, and option 4,
        the one use in this case scenario, is the more bandwith efficient, in our case the
        flag delimiter is a null byte indicating that the sock connection was closed.
    """
    def __init__(self,addr="localhost",port=8000):
        self.HOST = addr
        self.PORT = port
        # Initializate socket object
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.HOST,self.PORT))

    def close_connection(self):
        self.sock.close()
 
    def send(self,stream):
        # In case of the server the null delimiter never gets send beacause the
        # the client does not shut the conection until data is received, hence
        # we must send this flag manually.
        stream = stream + b'\0'
        self.sock.sendall(stream)

    def receive(self):
        data = bytearray()
        msg = ""
       # Receive data from the server and shut down
        while not msg:
            received = self.sock.recv(8192)
            data = data + received
            if received == b'':
                # Get a string out of the bytes stream
                msg = data.decode()
                break
        return msg



class ClientOperator:

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
            lines = operation_file.readlines(10000)
            if not lines:
            # If the end of the file was reached break the loop
                break

            for operation in lines:
                # Clean the operations list, to contain only valid operations.
                if not self.is_valid(operation):
                    # Remove operation from the list
                    lines.remove(operation)

            # Make data stream to send over the socket connection 
            stream = self.make_stream(lines)
            
            # Instatiate the TCPSocket object in a sock object to interact with 
            # the server
            sock = TCPInterfaceClient()
            
            sock.connect()
            sock.send(stream)
            
            
            # Wait until recieved entire information
            results = sock.receive()
            sock.close_connection()

            if len(lines) != len(results.split(',')):
                print("Error")

        operation_file.close()
        
if __name__ == "__main__":
    # Instatiate the Client and start getting and sending operations
     client = ClientOperator()
     client.start()






