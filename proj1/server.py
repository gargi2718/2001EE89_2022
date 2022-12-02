"""
import socket 
import threading 

HOST='127.0.0.1'
PORT=9090
# internet and tcp socket 
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients=[]
nicknames=[]

#broadcast
def broadcast():
    for client in clients:
        client.send(message)

#receive
def receive():
    while True:
        client,address=sever.accept()
        print(f"Connected with {str(addrress)}!")

        client.send("NICK".encode('utf-8'))
        nicknames.append(nickname)
        client.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname}Connected to the server".encode(utf-8))
        client.send("Connected to the server".encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

#handle

def handle(client):
    while True:
        try:
            message=client.recv(1024)
            print(f"{nicknames[client.index(client)]}")
            broadcast(message)
        except:
            index=client.index(client)
            clients.remove(client)
            client.close()
            nicknames=nicknames[index]
            nicknames.remove(nickname)
            break


if __name__ == '__main__':
    ChatServer()

"""

import socket
import threading
import random
import smtplib
import time

from typing import Dict, Union

email_address = "testmailmailtest000@gmail.com"
email_password = "mnciymhysjpktzdf"


def generate_code() -> str:
    alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    for _ in range(6):
        code += random.choice(alphabets)
    return code


def send_email(receiver, subject, content):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
        connection.login(email_address, email_password)
        connection.sendmail(
            from_addr=email_address,
            to_addrs=[receiver],
            msg=f"subject:{subject} \n\n {content}",
        )


class ChatServer:

    clients_list = []
    clients: Dict[str, Union[str, bool, socket.socket, str]] = {}

    last_received_message = ""

    def __init__(self):
        self.server_socket = None
        self.create_listening_server()

    # listen for incoming connection

    def create_listening_server(self):

        # create a socket using TCP port and ipv4
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_ip = "127.0.0.1"
        local_port = 10319
        # this will allow you to immediately restart a TCP server
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # this makes the server listen to requests coming from other computers on the network
        self.server_socket.bind((local_ip, local_port))
        print("Listening for incoming messages..")
        # listen for incoming connections / max 5 clients
        self.server_socket.listen(5)
        self.receive_messages_in_a_new_thread()

    # fun to receive new msgs

    def receive_messages(self, so: socket.socket):
        while True:
            incoming_buffer = so.recv(256)  # initialize the buffer
            print("client: ", so)
            if not incoming_buffer:
                break
            buffer = incoming_buffer.decode("utf-8")

            print(f"BUFFER: {buffer}")

            if buffer.startswith("MESSAGE: "):
                self.last_received_message = buffer
                self.broadcast_to_all_clients(so)  # send to all clients

            elif buffer.startswith("joined: "):
                client_info = buffer.replace("joined: ", "")
                client_username, client_password = client_info.split("$$$")
                if (
                    self.clients.get(client_username) is None
                    or self.clients[client_username]["password"] != client_password
                ):
                    print("FAILED")
                    so.sendall(b"LOGIN FAILED!")
                    continue
                self.last_received_message = f"USER {client_username} joined"
                self.clients[client_username]["online"] = True
                self.clients[client_username]['socket'] = so
                self.broadcast_to_all_clients(so)
                self.form_online_log_and_broadcast()

            elif buffer.startswith("REG: "):
                client_info = buffer.replace("REG: ", "")
                client_username, client_password = client_info.split("$$$")
                self.clients[client_username] = {
                    "password": client_password,
                    "online": True,
                    "socket": so,
                    "activation_code": "NULL",
                }
                so.sendall(b"MESSAGE: REGISTRATION SUCCESSFUL!")
                self.form_online_log_and_broadcast()

            elif buffer.startswith("FORGOT_PASSWORD: "):
                client_username = buffer.replace("FORGOT_PASSWORD: ", "")
                if self.clients.get(client_username) is None:
                    so.sendall(b"MESSAGE: Invalid Email!")
                else:
                    try:
                        self.clients[client_username][
                            "activation_code"
                        ] = generate_code()
                        # email...
                        send_email(
                            client_username,
                            "Activation Code",
                            f"Activation Code: {self.clients[client_username]['activation_code']}",
                        )
                        so.sendall(b"MESSAGE: Activation code sent to email.")
                        time.sleep(1)
                        so.sendall(b"RESET_PASSWORD")
                    except Exception as e:
                        print(e)
                        so.sendall(b"MESSAGE: Invalid Email!")

            elif buffer.startswith("RESET_PASSWORD: "):
                client_username, new_password, activation_code = buffer.replace(
                    "RESET_PASSWORD: ", ""
                ).split("$$$")
                if activation_code == self.clients[client_username]["activation_code"]:
                    self.clients[client_username]["password"] = new_password
                    so.sendall(b"MESSAGE: Password has been successfully reset!")
                else:
                    so.sendall(b"MESSAGE: Invalid Activation Code!")

            elif buffer.startswith("EXIT"):
                for client in self.clients.keys():
                    client = self.clients[client]
                    if so is not client["socket"]:
                        continue
                    client["online"] = False
                    temp = []
                    for c in self.clients_list:
                        socket, (_, _) = c
                        if socket is not client["socket"]:
                            temp.append(c)
                    self.clients_list = temp
                self.form_online_log_and_broadcast()
                break

            print(
                [
                    f"{client}: {self.clients[client]['online']}"
                    for client in self.clients.keys()
                ]
            )

        print(f"Closing something: {so}")
        so.close()

    # broadcast the message to all self.clients
    def form_online_log_and_broadcast(self):
        log = "ONLINE_LOG "
        for client in self.clients.keys():
            log += f"{client}: {'ONLINE' if self.clients[client]['online'] else 'OFFLINE'}\n"
        self.last_received_message = log
        for client in self.clients.items():
            if client[1]["online"]:
                print(f"Sending to {client[0]}")
                try:
                    client[1]["socket"].sendall(
                        self.last_received_message.encode("utf-8")
                    )
                except Exception as e:
                    print(e)

    def broadcast_to_all_clients(self, senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            # if not except_sender or socket is not senders_socket:
            if socket is not senders_socket:
                socket.sendall(self.last_received_message.encode("utf-8"))

    def receive_messages_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
            self.add_to_clients_list(client)

            print("Connected to ", ip, ":", str(port))
            t = threading.Thread(target=self.receive_messages, args=(so,))
            t.start()

    # add a new client

    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)


if __name__ == "__main__":
    ChatServer()
