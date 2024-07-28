import socket
import json
import time

def auto_Broadcast_IP():
    ip = socket.gethostbyname(socket.gethostname())
    parts = ip.split('.')
    parts[-1] = '255'
    broadcast_ip = '.'.join(parts)

    return broadcast_ip
    

def Service_Announcer():
    username = input("Enter your username: ")

    with open('username.txt', 'w') as f:
        json.dump(username, f)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_ip = auto_Broadcast_IP()
    broadcast_port = 6000



    try:
        while True:
            message = json.dumps({"username": username})
            sock.sendto(message.encode(), (broadcast_ip, broadcast_port))
            
            time.sleep(8)
            
    except KeyboardInterrupt:
        print("\nService Announcer is shutting down...")
        
        sock.close()

Service_Announcer()