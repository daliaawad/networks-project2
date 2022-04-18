from socket import *
from urllib.parse import *


def get_url(url, receive_buffer=4096):
                                 
    parsed = urlparse(url)                                                     
    try:                                                                       
        host, port = parsed.netloc.split(':')                                  
    except ValueError:                                                         
        host, port = parsed.netloc, 80  
                                           
    sock = socket(AF_INET, SOCK_STREAM)
    
    sock.connect((host, port))
    sock.sendall(('GET %s HTTP/1.0\n\n' % parsed.path).encode())                          

    response = [sock.recv(receive_buffer).decode()]                                
    while response[-1]:                                                        
        response.append(sock.recv(receive_buffer).decode())                             

    return ''.join(response) 



def create_server():
    serversocket = socket(AF_INET, SOCK_STREAM)
    try :
        serversocket.bind(('localhost', 9006))
        serversocket.listen(5)
        while(1):
            (clientsocket, address) = serversocket.accept()

            received_data = clientsocket.recv(5000).decode()
            pieces = received_data.split("\n")
            if(len(pieces) > 0) : print(pieces[0])
            if(received_data[0] == 'G'): #GET
                received_data = received_data[5:].split(' ')[0] #Remove 'GET' part
                
            received_data = 'http://' + received_data + '/'     
            data = get_url(received_data)    
            clientsocket.sendall(data.encode())
            clientsocket.shutdown(SHUT_WR)

    except KeyboardInterrupt :
        print("\nShutting down...\n")
    except Exception as exc :
        print("Error:\n")
        print(exc)

    serversocket.close()

print('Access http://localhost:9006')
create_server()