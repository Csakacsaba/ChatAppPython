import socket
import threading
import time
import datetime
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ('Helvetica', 17)
SMALL_FONT = ('Helvetica', 13)


class ChatClient:
    def __init__(self):
        self.host = None
        self.port = 5098
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.screen = tk.Tk()
        self.setup_gui()

    def setup_gui(self):
        self.screen.geometry('600x600')
        self.screen.title('Chat Alkalmazás')
        self.screen.resizable(False, False)

        self.screen.grid_rowconfigure(0, weight=1, )
        self.screen.grid_rowconfigure(1, weight=4)
        self.screen.grid_rowconfigure(2, weight=1)

        self.top_frame = tk.Frame(self.screen, width=600, height=100, bg=DARK_GREY)
        self.top_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.middle_frame = tk.Frame(self.screen, width=600, height=400, bg=MEDIUM_GREY)
        self.middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

        self.bottom_frame = tk.Frame(self.screen, width=600, height=100, bg=DARK_GREY)
        self.bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

        self.username_label = tk.Label(self.top_frame, text="Nev: ", font=FONT, bg=DARK_GREY, fg=WHITE)
        self.username_label.pack(side=tk.LEFT, padx=3)

        self.username_textbox = tk.Entry(self.top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=12)
        self.username_textbox.pack(side=tk.LEFT, padx=5)

        self.ip_label = tk.Label(self.top_frame, text="IP: ", font=FONT, bg=DARK_GREY, fg=WHITE)
        self.ip_label.pack(side=tk.LEFT, padx=3)

        self.ip_textbox = tk.Entry(self.top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=12)
        self.ip_textbox.insert(0, "192.168.9.103")
        self.ip_textbox.pack(side=tk.LEFT, padx=5)

        self.message_box = scrolledtext.ScrolledText(self.middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE,
                                                     width=67, height=23)
        self.message_box.config(state=tk.DISABLED)
        self.message_box.pack(side=tk.TOP)

        self.message_textbox = tk.Entry(self.bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=36)
        self.message_textbox.pack(side=tk.LEFT, padx=10)
        self.message_textbox.bind("<Return>", self.send_message)

        self.message_button = tk.Button(self.bottom_frame, text="Kuldes ", font=('Helvetica', 14), bg=OCEAN_BLUE,
                                        fg=WHITE, command=self.send_message)
        self.message_button.pack(side=tk.LEFT, padx=10)

        self.username_button = tk.Button(self.top_frame, text="Kapcsolodás", font=('Helvetica', 14), bg=OCEAN_BLUE,
                                         fg="WHITE", command=self.connect)
        self.username_button.pack(side=tk.LEFT)

    def connect(self):
        self.host = self.ip_textbox.get()

        if not self.host:
            messagebox.showerror("Nincs IP-cím", "Kérlek add meg az IP-címet a csatlakozáshoz.")
            return

        try:
            self.client.connect((self.host, self.port))
            self.add_message("[SZERVER]: Sikeres csatlakozás a szerverhez")
        except:
            self.add_message("[SZERVER]: NEM sikerült csatlakozni a szerverhez")
            messagebox.showerror("NEM sikerült csatlakozni",
                                 f"[SZERVER]: NEM sikerült csatlakozni a szerverhez {self.host} {self.port}")
            exit(0)

        username = self.username_textbox.get()
        if username != '':
            self.client.sendall(username.encode())
        else:
            messagebox.showerror("Nem megfelelő felhasználó név", "A felhasználó név nem lehet üres")

        connection = threading.Thread(target=self.listen_for_message_from_server)
        connection.start()

    def send_message(self, event=None):
        message = self.message_textbox.get()
        if message != '':
            self.message_textbox.delete(0, tk.END)
            self.client.sendall(message.encode())
            time.sleep(0.005)
        else:
            messagebox.showerror("ERROR", "Az elküldött üzenet üres")

    def listen_for_message_from_server(self):
        while 1:
            message = self.client.recv(2048).decode('utf-8')
            current_time = datetime.datetime.now()

            if "☼" in message:
                username, content = message.split("☼", 1)
                self.add_message(f'[{username}] {current_time.strftime("[%Y-%m-%d %H:%M:%S]")}: {content} ')
            else:
                self.add_message(f'{message}')

    def add_message(self, message):
        self.message_box.config(state=tk.NORMAL)
        self.message_box.insert(tk.END, message + "\n")
        self.message_box.config(state=tk.DISABLED)

    def main(self):
        self.screen.mainloop()


if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.main()
