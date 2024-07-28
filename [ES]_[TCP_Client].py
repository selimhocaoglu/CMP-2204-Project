import socket
import time
import json
import ast
import random
import pyDes
from datetime import datetime


def diffie_hellman_function(sock):
    base = 5
    modulus = 23
    private_key = random.randint(1, modulus)

    
    public_key = (base ** private_key) % modulus
    public_key = json.dumps({"key": public_key})
    sock.send(public_key.encode())

    opponents_public_key = sock.recv(1024)
    opponents_public_key= json.loads(opponents_public_key.decode())
    opponents_public_key = opponents_public_key["key"]

    shared_secret_key = (opponents_public_key ** private_key) % modulus
    
    return shared_secret_key




def Save_Chat(message, message_sent_time):
    with open('history.txt', 'a', encoding='utf-8') as f:
        f.write(message.ljust(100) + " " + message_sent_time + "\n")


def Get_Date():
    now = datetime.now()
    message_receive_time = now.strftime("%Y-%m-%d %H:%M:%S")

    return message_receive_time






def Chat_Initiator():
    loop = 1


    while loop == 1:
        
        print("1- Chat history")
        print("2- Send a message")
        print("0- Exit")


        choice = input("Select your choice above the menu..")

        if choice.lower() == "1":
            with open('history.txt', 'r', encoding='utf-8') as f:
                print(f.read())

                continue

        elif choice.lower() == "2":
            pass

        elif choice.lower() == "0":
            print("Exiting...")
            time.sleep(2)

            break

        else:
            print("Input is invalid, please try again!")
            time.sleep(2)

            continue


        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            with open('username.txt', 'r') as f:
                your_previous_name = json.load(f)

            print(f"Your previous name is \'{your_previous_name}\'")
            answer = input("Would you like to change your previous name? (y/n): ")

            if answer.lower() == "y":
                your_name = input("Enter a name: ")

            elif answer.lower() == "n":
                your_name = your_previous_name

            else:
                print("Input is invalid, your previous name will not change.")
                your_name = your_previous_name


            
            with open('active_users.txt', 'r') as f:
                users = ast.literal_eval(f.read())

            print("Active users:\n")
            for username in users:
                print(username)

            if not users:
                print("No active users\n")
                time.sleep(5)

                return

            username = input("\nEnter the username of the user that you would like to send a message to: ")




            if username not in users:
                print("User not found!")
                time.sleep(5)

                return
            
            user_data = users[username]
            ip_address = user_data[0]

            
            sock.connect((ip_address, 6001))



            while True:
                
                use_diffie_hellman_function = input("Would you like to apply Diffie-Hellman encryption? (y/n): ")
                if use_diffie_hellman_function.lower() not in ["y", "n"]:
                    print("Input is invalid, please try again!")

                    continue
                break

            sock.send(use_diffie_hellman_function.encode())


            if use_diffie_hellman_function.lower() == "y":
                shared_secret_key = diffie_hellman_function(sock)
            
            loop = 2

            while loop == 2:
                try:
                    my_message = input("Your message: ")
                    message = f"{your_name}: {my_message}"

                    if my_message == "EXIT":
                        print("Session is end!")
                        print("Exiting...")
                        time.sleep(5)
                        sock.close()
                        loop = 1

                        continue

                    if use_diffie_hellman_function.lower() == "y":
                        key = str(shared_secret_key).rjust(8, '0')
                        des = pyDes.des(key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
                        encrypted_message = des.encrypt(message.encode('utf-8'))
                        encrypted_message = list(encrypted_message)    
                        encrypted_message = json.dumps({"encrypted_message": encrypted_message})
                        sock.send(encrypted_message.encode())
                        message_sent_time = Get_Date()

                    elif use_diffie_hellman_function.lower() == "n":
                        message_ = json.dumps({"message": message})
                        sock.send(message_.encode())
                        message_sent_time = Get_Date()

                    Save_Chat(message, message_sent_time)


                except KeyboardInterrupt:
                    print("Exiting...")
                    sock.close()
                    time.sleep(2)
                    loop = 0

        except KeyboardInterrupt:
            print("Application is dismissed!")
            sock.close()
            time.sleep(3)

            break

        except ConnectionRefusedError:
            print("The user is unavailable.")
            time.sleep(3)

        except Exception as err:
            print("Error " + str(err))
            print("Try again!")
            time.sleep(5)







Chat_Initiator()