import socket
 #proxy client is a client to proxy server


def main():
    #CREATE PROXY CLIENT
    prox_client_socketIP = socket.AF_INET
    prox_client_socketType = socket.SOCK_STREAM
    prox_client_socket = socket.socket(prox_client_socketIP, prox_client_socketType)
    print("Proxy Client Socket Created\n")

    #CONNECT TO PROX SERVER
    prox_serverIP = "127.0.0.1" #"localhost"
    prox_serverPort = 8080
    prox_client_socket.connect((prox_serverIP, prox_serverPort))
    print("Proxy Client Connection to Proxy Server",prox_serverIP,"sent\n")

    #CREATE REQUEST
    #We want to go to google
    destIP = "www.google.com"
    newline = "\n"
    request_firstline = "GET / HTTP/1.0"
    request_headers = "Host: " + destIP
    request_body = ""

    request = request_firstline + newline + request_headers + newline + request_body + newline
    print("Proxy Client Created Request; \n")
    print(request)
    print("\n")


    #assuming connected..SEND REQUEST TO PROXY SERVER AS BYTES
    prox_client_socket.sendall(request.encode())
    print("Proxy Client Sent request to Proxy Server",prox_serverIP,"\n")


    #TELL PROX SERVER PROX CLEINT IS NO LONGER WRITING DATA
    done = socket.SHUT_WR
    prox_client_socket.shutdown(done)
    print("Proxy Client no longer writing data\n")

    #RECEIV RESPOMNSE FROM PROXY SERVER
    recv_buffsize = 4096
    response = b""
    while True:
        response_part = prox_client_socket.recv(recv_buffsize)
        if not response_part:
            break
        response += response_part

    
    #SHOW RESPONSE FROM PROX SERVER
    print("Prox Client got Response from Prox Server; \n")
    print(response,"\n")

    # CLOSE PROX CLIENT SOCKET
    prox_client_socket.close()
    print("Prox Client Socket Closed\n")

main()