# Operator
A client-server program to calculate mathematical operations, exchanging information using sockets in a multithreaded way

## Getting Started

This project is a simple client-server implementation for analyzing large files containing mathematical operations. The client loads all the operations and send it to the server, who is in charge of solving them, using processes to speed up the task, and return the results back to the client who will record them in a log file.

### Prerequisites

It is necesary to install a version of python < 3.7 . All the modules used are from the standard library who comes on board with the python installation.

### How to use

To use it, run the script **server.py** which will start listen connections on specified port (default 8000)


Once the server is running, run the **client.py** which will extract the operations out of the **operations.txt** file  (which needs to be in same directory, or you can specify another file with the same format inside the script) and send them through a TCP socket connection to the server, which will solve the operations and send back the results to be log by the client in the **operations.log** file.

The server to speed up the calculations will use multiple processes, the default is 2 processes but this parameter can be change inside the **server.py** script

To complete the task the programm takes no more that 10 seconds.

### Running the tests

The script test.py contains all the test necessary to check whether the system works properly. If something goes wrong the script will tell you exactly what part fail.

### Bugs

Currently the server throw an error on Windows with python 3.7.2 due to multiprocessing module. This does not occur with a lower python 3 version or in a Linux OS.

## Authors

* **Alejandro Martin** - *Initial work* - [PyChat](https://github.com/ale9412/PyChaT)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



