import socket
import json
import time
import random
import pyDes
from datetime import datetime

def diffie_hellman_function(conn):
    base = 5
    modulus = 23
    private_key = random.randint(1, modulus)
    public_key = (base ** private_key) % modulus
    opponents_public_key = conn.recv(1024)
    opponents_public_key= json.loads(opponents_public_key.decode())
    opponents_public_key = opponents_public_key["key"]
    public_key = json.dumps({"key": public_key})
    conn.send(public_key.encode())
    shared_secret_key = (opponents_public_key ** private_key) % modulus
    
    return shared_secret_key



def Get_Date():
    now = datetime.now()
    message_receive_time = now.strftime("%Y-%m-%d %H:%M:%S")

    return message_receive_time




def Give_Response():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_ip = socket.gethostbyname(socket.gethostname())
    sock.bind((client_ip, 6001))


    sock.listen(1)

    loop = 1
    while True:
        try:
            conn, addr = sock.accept()
            diffie_hellman_choice = conn.recv(1024).decode() 
            if diffie_hellman_choice.lower() == "y":
                shared_secret_key = diffie_hellman_function(conn)
            


            try:
                socket.setdefaulttimeout(10.0)
                loop = 2

                while loop == 2:
                    if diffie_hellman_choice.lower() == "y":
                        encrypted_message = conn.recv(1024)
                        encrypted_message = json.loads(encrypted_message.decode())
                        encrypted_message = bytes(encrypted_message["encrypted_message"]) 
                        message_receive_time = Get_Date()
                        key = str(shared_secret_key).rjust(8, '0')
                        des = pyDes.des(key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
                        message = des.decrypt(encrypted_message)
                        message = message.decode('utf-8')

                    elif diffie_hellman_choice.lower() == "n":
                        message = conn.recv(1024).decode()
                        message = json.loads(message)
                        message = message["message"]
                        message_receive_time = Get_Date()



                    print(message.ljust(100) + " " + message_receive_time)

                    if not addr[0] == client_ip:
                        with open('history.txt', 'a', encoding='utf-8') as f:
                            f.write(message.ljust(100) + " " + message_receive_time + "\n")

            except KeyboardInterrupt:
                
                print("\nShutting...")
                print("\nServer closed!")



                try:
                    conn.close()
                except:
                    pass
                sock.close()

                return

            except socket.error as e:
                if isinstance(e, ConnectionResetError):
                    print("Connection has been closed by client!\n")
                    conn.close()

                    continue
                    


            except:
                print("Connection has been closed by client!\n")
                conn.close()

                continue
                
        except KeyboardInterrupt:
            print("\nShutting...")
            print("\nServer closed!")
            try:
                conn.close()
            except:
                pass
            sock.close()
            time.sleep(3)

            return

        except UnicodeError:
            print("Use UTF-8 encoding for your message!")

            continue
    


        except Exception as err:
            print("Error: " + str(err))
            print("Try again!")

            continue
       




Give_Response()