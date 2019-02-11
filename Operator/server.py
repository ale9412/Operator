import socketserver
import multiprocessing as mp

from shunting_yard_algorithm import evaluate

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    
    def handle(self):
        data = self.receive()
        operations = data.split(',')
        result_list = []
        """Instatiate the ProcessHandler class, send it the operations and retrieve results,
        the default number of process is 2, if more processes wants to be used is necesary
        pass to the ProcessHandler class the "process_number" argument with a value equal
        to the number of process to be used."""
        
        process_handler = ProcessHandler(operations)

        # processes_results is a tuple with the structure (process_order,results_list)
        processes_results = process_handler.create_processes()
        

        # Sort to get the results from processes with the same order of the operations
        processes_results.sort()

        # Get only the list of results
        processes_results = [r[1] for r in processes_results]
        
        # Unify the results obtained from the processes in a single results list
        for i in range(len(processes_results)):
            result_list.extend(processes_results[i])
        stream = self.to_stream(result_list)
        
        # Send back to the client
        self.request.sendall(stream)
        self.request.close()
        
    def to_stream(self,results):
        return bytes(','.join(str(result) for result in results),"utf-8")
    
    def receive(self):
        data = bytearray()
        msg = ""
        buffer = 1048476 # 1MB the buffer
        # Receive data until the delimiter flag would be reached
        while not msg:
            # self.request is the TCP socket client connected to the server
            received = self.request.recv(buffer)
            data = data + received
            if received.endswith(b'\0'):
                # Get a string out of the bytes stream
                msg = data.decode().strip('\0')
                break
        return msg


class ProcessHandler:

    def __init__(self,operations,process_number=2):        
        """Multiprocessing module supports two types of communication channels:
        Pipes and Queue, the one used here. Queue allows process to store values
        in a common place without worrying about concurrency issues."""
        
        self.queue = mp.Queue()
        self.operations = operations
        # Split data to fit the two processes
        limit = int(len(operations)/process_number)
        self.operations_per_proc = self.split_list(process_number)
        self.processes = []

    def create_processes(self):
        # The pos identifier will allows to identify which list of results comes first
        # in order to retrieve the results in the same order they were requested
        for pos,op_list in enumerate(self.operations_per_proc):
            self.processes.append(mp.Process(target=self.resolver,args=(pos,op_list)))
        for p in self.processes:
            p.start()

        # Get from queue tuple formed by the process results and his position
        results = [self.queue.get() for p in self.processes]
        for process in self.processes:
            process.terminate()
        return results
        
    def resolver(self,pos,operations_list):
        result_list = list(map(evaluate,operations_list))
        self.queue.put((pos,result_list))

    def split_list(self,splits):
        full_list = self.operations
        # Method to split operations betwen the number of processes
        length = int(len(full_list)/splits)
        parts = []
        for i in range(splits):
            parts.append(list(full_list[:length]))
            full_list = full_list[length:]
        # If there were some elements left add them to the last list
        parts[-1].extend(full_list)
        return parts
                        
if __name__ == "__main__":
    mp.freeze_support()
    # If an ip address wants to be used instead, change localhost by the ip. If multiple interfaces want to be used
    # you could change localhost by the empty string (''), this will make the server listen on all available interfaces.
    HOST, PORT = "localhost", 8000

    # Create the server, binding to localhost on port 8000
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        """
        This is a high-level asynchronous TCP base server that will handle incomming 
        connections, and send answers. The protocol used was TCP instead of UDP because of the
        beneficts of this protocol, like:
            1- Reliability
            2- Synchronization
            3- Error recovery in case of losed and damaged data
            
        This high level server is the equivalent to the low level implementation
        with the socket module:

        srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        srvsock.bind( ("localhost", 8000) )
        srvsock.listen( 5 )

        and handling incoming conections with the select module to made it asynchronous
        (sread, swrite, sexc) = select.select( [read_socket_client], [write_socket_client], [] )

        The previous line will block the server until a conexion is made. Extra coding must be
        made in order to handle the conexion.
        """
        
        # Activate the server, this will keep running until you
        # interrupt with Ctrl-C
        print(f"Serving on port {PORT}, press Ctr-C to exit...")
        server.serve_forever()
