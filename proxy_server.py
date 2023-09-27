import socket
from threading import Thread

# handle connections to client on a thread need function
def handleConnectedRequest(conn, client_addr):
    print("Proxy Server connected to Proxy Client at; \n")
    print(client_addr,"\n")
     
    recv_buffsize = 4096
    request = b""

    while True:
        request_part = conn.recv(recv_buffsize)
        if not request_part:
            break
        request += request_part
    print("Prox Server Received Request from Connected Prox Client; \n")
    print(request,"\n")

    #RECEIVED REQUEST FROM PROXY CLIENT NOW SEND TO WEB SERVER
    #CREATE WEB SERVER SOCKET    
    prox_server_client_socketIP = socket.AF_INET
    prox_server_client_socketType = socket.SOCK_STREAM
    with socket.socket(prox_server_client_socketIP, prox_server_client_socketType) as prox_server_client_socket:
        #CREATE REQUEST TO WEB SERVER
        request_str = request.decode('utf-8')
        request_str_lines = request_str.split("\n")

        #CONNECT TO WEB SERVER
        host = request_str_lines[1].split()[1] #"www.google.com"
        port = 80
        prox_server_client_socket.connect((host, port))
        print("Prox Server [Acts As A Client] Connected to Web Server\n")

        #assuming connected.. SEND REQUEST TO WEBSERVER
        prox_server_client_socket.sendall(request)
        print("Prox Server [Acts As A Client] Sent Request to Web Server\n")
        print(request,"\n")

        #TELL WEB SERVER THIS SERVER CLIENT IS DONE WRITING DATA
        done = socket.SHUT_WR
        prox_server_client_socket.shutdown(done)
        print("Prox Server [Acts As A Client] Shutdown Writing to Web Server\n")

        #RECIEVED REPOSNSE FROM WEB SERVER AND SEND TO PROXY CLIENT
        #RECEIVE RESPONSE FROM WEB SERVER
        recv_buffsize = 1024
        response = b""
        while True:
            response_part = prox_server_client_socket.recv(recv_buffsize)
            if not response_part:
                break
            response += response_part
        print("Prox Server [Acts As A Client] Received Response from Web Server\n")

        #SEND RESPOSNE TO PROXY CLIENT
        conn.sendall(response)
        print("Prox Server Response from Web Server Sent to Proxy Client\n")

        #CLOSE CONNECTION
        conn.close()
        print("Prox Server Connection To Proxy Client closed\n")
    
    


    
    




#Proxy server is a client to web server and a server to proxy client
def main(threaded):
    #CREATE PROXY SERVER SOCKET
    prox_server_socketIP = socket.AF_INET
    prox_server_socketPort = socket.SOCK_STREAM
    

    with socket.socket(prox_server_socketIP, prox_server_socketPort) as prox_server_socket:
       print("Prox Server Socket Created\n")
       #BEFORE BINDING, WE WANT TO SET CONTINUOUS BINDING
       socket_lvl = socket.SOL_SOCKET
       socket_option = socket.SO_REUSEADDR
       reuse = 1
       prox_server_socket.setsockopt(socket_lvl, socket_option, reuse)
       print("Prox Server Socket will continuous bind to Proxy Server Port and IP Address\n")


       #BIND TO SERVER
       prox_serverIP = "127.0.0.1" #"localhost"
       prox_serverPort = 8080
       prox_server_socket.bind((prox_serverIP, prox_serverPort))
       print("Prox Server Socket Binded to", prox_serverIP,"\n")


       #LISTEN FOR REQUESTS FROM PROX CLIENT(S)
       nconnections = 2
       prox_server_socket.listen(nconnections)
       print("Prox Server Listening...\n")

       #CONTINUOUSLY ACCEPT CONNECTIONS TO PROX CLIENT
       while True:
        connection, prox_client_address = prox_server_socket.accept()
        print("Prox Server Accepted Connection to a Proxy Client\n")

        #USE CONNECTION TO HANDLE CONNECTION
        if threaded:
              print("Forking Proxy Server\n")
              target_thread_funct = handleConnectedRequest
              target_thread_funct_args = (connection, prox_client_address)
              connection_threads = Thread(target=target_thread_funct, args=target_thread_funct_args)
              connection_threads.run()
        else:
            print("Regular Proxy Server\n")
            handleConnectedRequest(connection,prox_client_address)


threaded=1
main(threaded)