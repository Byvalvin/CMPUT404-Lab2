import socket
from threading import Thread

def handleConnectedRequest(connection, connected_client_address):
    print("Connected To; ")
    print(connected_client_address)

    #RECEIVE REQUEST FROM CLIENT
    recv_buffersize = 1024
    request = b""
    while True:
        request_part = connection.recv(recv_buffersize)
        if not request_part:
            break
        request += request_part
    
    print("\nRequest Received from Client; \n")
    print(request)

    #SEND REQUEST BACK, ECHO REQUEST
    connection.sendall(request)
    print("\nRequest Sent Back To Client\n")

    #CLOSE CONNECTION(Not Socket)
    connection.close()
    print("A Connection was closed \n")


def main(threaded):
    #CREATE SERVER SOCKET, will use with keyword
    server_socketIP = socket.AF_INET
    server_socketType = socket.SOCK_STREAM

    
    serverHost = "localhost" #127.0.0.1
    serverPort = 8001
    n_connections = 2
    with socket.socket(server_socketIP,server_socketType) as server_socket:
        print("Server Socket created\n")
        #BIND SERVER SOCKET TO SERVER
        server_socket.bind((serverHost, serverPort))
        print("Server Socket binded to Server\n")

        #CONTINUOUSLY ALLOW SOCKET TO BIND TO SERVER PORT 
        socket_level = socket.SOL_SOCKET
        socket_option = socket.SO_REUSEADDR
        reuse = 1
        server_socket.setsockopt(socket_level, socket_option, reuse)
        print("Server Socket can continue to bind to same host and port\n")

        #LISTEN FOR CLENTS LOOKING TO CONNECT TO THIS SERVER
        server_socket.listen(n_connections)
        print("Server Socket listening...\n")

        # ACCEPT CONNECTION REQUESTS FROM CLIENT
        while True:
            connection, connected_client_address = server_socket.accept()
            print("Server Socket connected to a Client\n")

            # HANDLE ALL CLIENT REQUESTS TO SERVER
            if(threaded==1):
                # Thread to handle a single client's multiple(max of n_connections) connmections "simultaneously"
                thread_target_function=handleConnectedRequest
                thread_target_function_args=(connection,connected_client_address)
                connection_threads = Thread(target=thread_target_function, args=thread_target_function_args)
                connection_threads.run()
            else:
                # No threading, handle connections from client as a queue, 1 after the other
                handleConnectedRequest(connection, connected_client_address)


threaded = 1

main(threaded)