from socket import *
from urllib.parse import *


def get_url(url, receive_buffer=4096):
    url = 'http://' + url + '/'                              
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
        serversocket.bind(('localhost', 9000))
        serversocket.listen(5)
        while(1):
            (clientsocket, address) = serversocket.accept()

            rd = clientsocket.recv(5000).decode()
            pieces = rd.split("\n")
            if(len(pieces) > 0) : print(pieces[0])
            
            data = get_url(rd)
            
            clientsocket.sendall(data.encode())
            clientsocket.shutdown(SHUT_WR)

    except KeyboardInterrupt :
        print("\nShutting down...\n")
    except Exception as exc :
        print("Error:\n")
        print(exc)

    serversocket.close()

print('Access http://localhost:9000')
create_server()