from shunting_yard_algorithm import evaluate
import re

def shunting_yard_tester():
    operations_file = open("operations.txt")
    ops_list = operations_file.readlines(100000)
    operations_file.close()

    # Grab a bunch of operations and test if the shunting_yard_algorithm works well
    for operation in ops_list:
        try:
            assert(evaluate(operation) == round(eval(operation)),3)
        except AssertionError:
            print(operation)
            print("Shunting Yard algorithm failed")
            
            return False
    return True

# Test whether the tokenizer regex works
def tokenizer_tester():
    operations_file = open("operations.txt")
    # Read some valid operations
    ops_list = operations_file.readlines(300)
    operations_file.close()
    regex = r'(\d+\s[+*-/]\s)+\d+'
    pattern = re.compile(regex)
    for operation in ops_list:
        try:
            assert(pattern.match(operation))
    
        except AssertionError:
            print("The regular expresion to parse aritmetic operations does not work")
            return False
    return True


def socket_connection_test():
    # To test socket conection the server must be running
    from client import TCPInterfaceClient as Sock
    from client import ClientOperator as Client
    
    operations_file = open("operations.txt")
    ops_list = operations_file.readlines(10000)
    operations_file.close()

    try:
        # Call the make_stream method of ClientOperator to
        # convert list to stream of bytes
        client = Client()
        stream = client.make_stream(ops_list)

        # Send and receive data over the TCPInterfaceClient
        sockclient = Sock()
        sockclient.connect()
        sockclient.send(stream)
        results = sockclient.receive()
        
    except Exception as e:
        # Any error inside the TCPInterfaceClient class
        print("Socket Error:",e)
        return False
    try:
        # Check if there were received the same amount that was send
        assert(len(ops_list) == len(results.split(',')))
        return True
    except AssertionError:
        print("There were some missing data in the socket connection")
        return False

def data_splitter_test():
    from server import ProcessHandler as PH
    operations_file = open("operations.txt")
    ops_list = operations_file.readlines(10000)
    operations_file.close()
    
    ph = PH(ops_list)
    try:
        # Split in 2 samples
        length = int(len(ops_list)/2)
        manual_splits = [ops_list[:length],ops_list[length:]]
        automatic_split = ph.split_list(2)
        assert(manual_splits==automatic_split)
        
        # Split in 3 samples
        length = int(len(ops_list)/3)
        manual_splits = [ops_list[:length],ops_list[length:2*length],ops_list[2*length:]]
        automatic_split = ph.split_list(3)
        assert(manual_splits==automatic_split)

        # etc
        return True
    except AssertionError:
        return False
    
def valids_results():
    file = open('operations.log')
    lines = file.readlines()
    operation = r'(\d+\s[+*-/]\s)+\d+'
    patt = re.compile(operation)

    res = re.compile("= (-?\d+(\.\d+)?)")
    new_lines = lines[2:]
    try:
        for line in new_lines:
            op = patt.search(line)
            result = res.search(line)
            oper = op.group()
            result = result.group(1)
            assert(round(eval(oper),3) == float(result))
        return True
    except AssertionError:
        print("Results in log file are incorrect")
        return False
    

if shunting_yard_tester(): print("Shunting Yard Algorithm works well")
if tokenizer_tester(): print("The regular expresion to parse aritmetic operations works well")
if socket_connection_test(): print("Socket connection works well")
if data_splitter_test(): print("List splitter works well")
if valids_results(): print("Results in log file are correct")
