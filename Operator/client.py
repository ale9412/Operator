import re
import socket


class TCPInterfaceClient:
    """
    Class to create a socket object that will handle data over a TCP connection

    To receive data over a TCP connection four approaches could be made:

        1 - Use as a protocol that only one message will be sent per connection,
        and once a message has been sent, the sender will inmidiately close the socket

        2 - Use fixed lenght messages. The receiver will read the number of bytes and
        know that it has the whole msg.

        3 - Prefix the msg length at the beginning of the stream. The receiver will read
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
        self.buffer = 1048476 # 1MB buffer

    def connect(self):
        self.sock.connect((self.HOST,self.PORT))

    def close_connection(self):
        self.sock.close()
 
    def send(self,stream):
        stream = stream + b'\0'
        self.sock.sendall(stream)

    def receive(self):
        data = bytearray()
        msg = ""
       # Receive data from the server and shut down
        while not msg:
            received = self.sock.recv(self.buffer)
            data = data + received
            if received == b'':
                # Get a string out of the bytes stream
                msg = data.decode()
                break
        return msg



class ClientOperator:

    def __init__(self,file_path='operations.log'):
        # Expression to parse matematical operations
        self.regex = r'(\d+\s[+*-/]\s)+\d+'
        self.file_path = file_path
        # Clean the log file in case that exist already
        log_file = open(self.file_path,'w')
        log_file.close()

    
    def is_valid(self,op):
        pattern = re.compile(self.regex)
        return pattern.match(op)

    def make_stream(self,operations_list):
        return bytes(','.join(operation.strip() for operation in operations_list).encode('utf-8'))
    
    def start(self):
        operation_file = open("operations.txt")
        operations = []
        results = []
        while True:
            """ Read in batches and send. Read the entire file could be memory expensive
                and read it line by line to slow.
                The number passed to the readlines method is the number of caracters to be read, the file will be 
                read multiple times until end of the file is reached."""
            lines = operation_file.readlines(2000000)
            
            if not lines:
            # If the end of the file was reached break the loop
                break

            # Clean the operations list, to contain only valid operations.
            for operation in lines:
                if not self.is_valid(operation):
                    # If it is not a valid arithmetic operation remove it.
                    lines.remove(operation)

            # Stores all operations for further logging.
            operations += lines
           
            # Make data a bytes stream to send over the socket connection .
            stream = self.make_stream(lines)
            
            # Instatiate the TCPSocket class in a sock object to interact with the server.
            sock = TCPInterfaceClient()
            
            sock.connect()
            sock.send(stream)
            # In case of the server the null delimiter never gets send beacause the
            # the client does not shut the conection until data is received, hence
            # we must send this flag manually.
            
            # Wait until recieved entire information
            r = sock.receive()
            #Store every iteration result in the results variable to further logging
            results = results + r.split(",")
            sock.close_connection()
        
        operation_file.close()
        self.log(operations,results)

    def log(self,operations,results):
        # Open the file in append mode
        log_file = open(self.file_path,'a')
        
        # opeations and results list are ordered list objects where every item
        # inside them correspond with the item in the same position
        # in the other.
    
        log_file.write("Operations log file".center(60,'*'))
        log_file.write("\n")
        for operation,result in zip(operations,results):
            full_operation = f"\nOperation: {operation.rstrip()} = {result}"
            log_file.write(full_operation)

        log_file.close()
        return
    
if __name__ == "__main__":
    # Instatiate the Client and start getting and sending operations
     client = ClientOperator()
     client.start()





