import socket
import json
import time

def Peer_Discovery():
    




    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 6000))
    active_users = {}
    sock.settimeout(5.0)

    try:
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                message = json.loads(data.decode())
                active_users[message['username']] = (addr[0], time.time())

            except socket.timeout:
                pass
            except Exception as err:
                print("Error: " + str(err))
                print("Try again!")

                continue
            


            if not active_users:
                print("\nNo active users")

            else:
                online_users = {}
                with open('active_users.txt', 'w') as f:
                    print("\nUsers Status:")
                    
                    for username, (ip, last_heard) in list(active_users.items()):
                        if time.time() - last_heard > 900:
                            print(f"{username} (Offline) - IP: {ip}")
                            del active_users[username]
                        else:
                            status = "(Away)" if time.time() - last_heard > 10 else "(Online)"
                            print(f"{username} {status} - IP: {ip}")
                            if status == "(Online)":
                                online_users[username] = (ip, last_heard)
                    with open('active_users.txt', 'w') as f:
                        json.dump(online_users, f)



    except KeyboardInterrupt:
        print("\nPeer Discovery is shutting down...")
        sock.close()
        online_users.clear()
        with open('active_users.txt', 'w') as f:
            json.dump(online_users, f)
Peer_Discovery()