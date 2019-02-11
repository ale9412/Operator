from shunting_yard_algorithm import evaluate
import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        data = self.receive()#request.recv(4096).strip()
        
        operations = data.split(',')
##        print(len(operations))
        # Here the operations recieved will be process and returned the results
        result_list = resolver(operations)
        stream = self.to_stream(result_list)
        # Send back to the client
        self.request.sendall(stream)
        self.request.close()
        
    def to_stream(self,results):
        return bytes(','.join(str(result) for result in results),"utf-8")
    
    def receive(self):
        data = bytearray()
        msg = ""
       # Receive data from the server and shut down
        while not msg:
            received = self.request.recv(8192)
            data = data + received
            if received.endswith(b'\0'):
                # Get a string out of the bytes stream
                msg = data.decode()
                break
        return msg
    
def resolver(operations_list):
    result_list = []
    for operation in operations_list:
    	result = evaluate(operation)
    	result_list.append(round(result,3))
    return result_list

if __name__ == "__main__":
    HOST, PORT = "localhost", 8000

    # Create the server, binding to localhost on port 8000
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
