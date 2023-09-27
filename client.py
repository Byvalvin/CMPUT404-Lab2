import socket

def getRequestToSend(host):
    newline = "\n"
    encoding = 'utf-8'

    request_firstline = "GET / HTTP/1.0"
    request_headers = "Host: " + host
    request_body = ""

    request = request_firstline + newline + request_headers + newline + request_body + newline
    print("Client Request;\n")
    print(request)
    request_In_bytes = request.encode(encoding)

    return request_In_bytes

def main(serverhost, serverport):
    #CREATE CLIENT SOCKET
    client_socketIP = socket.AF_INET
    client_socketType = socket.SOCK_STREAM
    client_socket = socket.socket(client_socketIP, client_socketType)
    print("Client Socket created\n")

    #CONNECT TO SERVER 
    client_socket.connect((serverhost, serverport))
    print("Client Socket Connection sent\n")

    #CREATE DATA TO BE SENT TO SERVER
    request_bytes = getRequestToSend(serverhost)
    
    
    #SEND DATA TO SERVER
    client_socket.sendall(request_bytes)
    print("Client Socket sent request\n")

    #TELL SERVER CLIENT HAS NO MORE REQUESTS
    done = socket.SHUT_WR
    client_socket.shutdown(done)
    print("Client Socket shutdown writing capabilities\n")

    #RECEIVE SERVER RESPONSE
    recv_buffersize = 2048
    response = b""
    while True:
        response_part = client_socket.recv(recv_buffersize)
        if not response_part:
            break
        response += response_part
    print("Client Socket response received\n")

    #DISPLAY RESPONSE
    print("Server responded with;\n")
    print(response)

    #CLOSE CLIENT SOCKET
    client_socket.close()
    print("\nClient Socket closed\n")






host1 = "www.google.com"
port1 = 80

host2 = "localhost" #127.0.0.1
port2 = 8001

run = 0
if run==1:
    main(host1,port1)
else:
    main(host2,port2)