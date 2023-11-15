import socket
import threading


class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.active_clients = []

    def send_private_message(self, sender, recipient, message):
        recipient_trim = recipient.strip("@ ")
        for user in self.active_clients:
            # print(user[0],"=",recipient_trim)
            if user[0] == recipient_trim:
                print("Megkapta a klienst")
                self.send_message_to_client(user[1], f'[{sender}] Privát üzenet: {message}')
                return

    def listen_for_messages(self, client, username):
        while 1:
            try:
                message = client.recv(2048).decode('utf-8')
                if message != '':
                    if message.startswith('@'):

                        recipient, message_content = message.split(":", 1)
                        self.send_private_message(username, recipient, message_content)
                    else:
                        final_msg = f'{username}☼{message}'
                        self.send_message_to_all(final_msg)
                else:
                    print(f'Üres üzenet érkezett {username} felhasználótól')
            except ConnectionResetError:
                import traceback
                traceback.print_exc()
                break
            except Exception as e:
                print(e)
                break

    def send_message_to_all(self, message):
        for user in self.active_clients:
            self.send_message_to_client(user[1], message)

    def send_message_to_client(self, client, message):
        client.sendall(message.encode())

    def client_handler(self, client):
        while 1:
            username = client.recv(2048).decode('utf-8')
            if username != '':
                self.active_clients.append((username, client))
                print(self.active_clients)
                connect_message = f'{username} csatlakozott a chathez.'
                self.send_message_to_all(connect_message)
                break
            else:
                print('A kliens neve nem található')
        threading.Thread(target=self.listen_for_messages, args=(client, username)).start()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind((self.host, self.port))
            print(f'A szerver fut......')
        except:
            print(f'Nem sikerült a kapcsolatot létrehozni {self.host}, {self.port}')

        server.listen()

        while True:
            client, address = server.accept()
            print(f'Sikeres csatlakozás {address[0]} {address[1]}')
            threading.Thread(target=self.client_handler, args=(client,)).start()

    # def close_database_connection(self):
    #     self.db_connection.close()


if __name__ == "__main__":
    chat_server = ChatServer('0.0.0.0', 5098)
    chat_server.start_server()

