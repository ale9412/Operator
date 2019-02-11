
def shunting_yard_tester():
    from shunting_yard_algorithm import evaluate
    
    operations_file = open("operations.txt")
    ops_list = operations_file.readlines(10000)
    operations_file.close()

    # Grab a bunch of operations and test if the shunting_yard_algorithm works well
    for operation in ops_list:
        try:
            assert(evaluate(operation) == eval(operation))
        except AssertionError:
            print("Shunting Yard algorithm failed")
            
            return False
    return True

# Test whether the tokenizer regex works
def tokenizer_tester():
    import re
    
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


if shunting_yard_tester(): print("Shunting Yard Algorithm works well")
if tokenizer_tester(): print("The regular expresion to parse aritmetic operations works well")
if socket_connection_test(): print("Socket connection works well")
