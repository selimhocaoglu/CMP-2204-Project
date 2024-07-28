
Bahcesehir University Computer Engineering Introductioning to Computer Networks (CMP2204) Project

# Chat Application

This project consists of a TCP-based chat system with encryption support using Diffie-Hellman key exchange and a UDP-based peer discovery system.

## Description

### UDP_Client.py and UDP_Server.py

These files implement a peer discovery system using UDP broadcasting. Users can discover other online users by running the UDP server and broadcasting their status using the UDP client. Online users may appear as "Away" or "Offline" after a certain period of inactivity.

### TCP_Client.py and TCP_Server.py

These files contain the client and server sides of the TCP-based chat application, respectively. The client can send messages to another user which is online by specifying their username that stored in json manner. The server receives and displays these messages. The application supports encryption using the Diffie-Hellman key exchange algorithm.

## How to Run

### UDP Peer Discovery

1. Run `UDP_Server.py` to start the UDP server for peer discovery. This program enables user to get broadcast messages that sent by other devices on same Wi-fi network.
2. Run `UDP_Client.py` to broadcast your presence. Enter your username to join the broadcast in order to show yourself to devices on same Wi-fi network.

### TCP Chat Application

1. Run `TCP_Server.py` to start the server.
2. Run `TCP_Client.py` select the option that you would like to operate.


## Known Limitations

1. **Limited Encryption Support**: The encryption implemented using Diffie-Hellman key exchange in the TCP chat application has limitations and may not provide full security guarantees.
2. **Single-Threaded Design**: Both the TCP server and client operate in a single-threaded manner, which may limit scalability in high-traffic scenarios.
3. **Manual Username Input**: Users need to manually input their usernames in both the TCP and UDP applications, which may lead to inconsistencies or errors.
4. **Chat History**: Users can view chat history by selecting the appropriate option. However, the application does not store chat history beyond the current session.
5. **User Activity Status**: Online users may appear as "Away" after a certain period(10 second for being "Away" and 900 second for being "Offline") of inactivity to indicate their status to other users.

## Dependencies

### Python Version

- Python 3.12.3

### Essential Libraries
- Random (for encryption)
- ast (to store user's status)
- pyDes (for encryption)
- Socket
- time
- json
- datetime (from datetime import datetime)

