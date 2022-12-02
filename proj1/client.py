from tkinter import (
    Tk,
    Frame,
    Scrollbar,
    Label,
    END,
    Entry,
    Text,
    VERTICAL,
    Button,
    messagebox,
    Toplevel,
)
import socket  # Sockets for network connection
import threading  # for multiple process
import tqdm 


class GUI:
    client_socket = None
    last_received_message = None

    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.chat_online_log_area = None
        self.name_widget = None
        self.password_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.reset_window = None
        self.initialize_socket()
        self.initialize_gui()
        self.listen_for_incoming_messages_in_a_thread()

    def initialize_socket(self):
        # initializing socket with TCP and IPv4
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = "127.0.0.1"  # IP address
        remote_port = 10319  # TCP port
        # connect to the remote server
        self.client_socket.connect((remote_ip, remote_port))

    def initialize_gui(self):  # GUI initializer
        self.root.title("Socket Chat")
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_name_section()
        self.display_chat_entry_box()
        # self.display_reset_password()

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(
            target=self.receive_message_from_server, args=(self.client_socket,)
        )  # Create a thread for the send and receive in same time
        thread.start()

    # function to receive msg

    def receive_message_from_server(self, so):
        while True:
            buffer = so.recv(256)
            if not buffer:
                break
            message = buffer.decode("utf-8")

            print(message)

            if "joined" in message:
                user = message.split(":")[1]
                message = user + " has joined"
                self.chat_transcript_area.insert("end", message + "\n")
                self.chat_transcript_area.yview(END)

            elif message == "LOGIN FAILED!":
                # self.on_login_fail_close_window()
                self.name_widget.config(state="normal")
                self.password_widget.config(state="normal")

            elif message.startswith("ONLINE_LOG"):
                print(message)
                self.chat_online_log_area.delete(1.0, "end")
                self.chat_online_log_area.insert(
                    "end", message.replace("ONLINE_LOG ", "") + "\n"
                )
                continue

            elif message.startswith("MESSAGE: "):
                message = message.replace("MESSAGE: ", "")
                self.chat_transcript_area.insert("end", message + "\n")
                self.chat_transcript_area.yview(END)

            elif message == "RESET_PASSWORD":
                self.display_reset_password()

        so.close()

    def display_reset_password(self):
        self.reset_window = Toplevel()
        frame_username = Frame(self.reset_window)
        frame_password = Frame(self.reset_window)
        frame_code = Frame(self.reset_window)
        frame_buttons = Frame(self.reset_window)

        Label(
            frame_username, text="Enter username/email:", font=("Helvetica", 11)
        ).pack(side="left", padx=10)
        self.reset_name_widget = Entry(frame_username, width=50, borderwidth=2)
        Label(frame_password, text="Enter new password:", font=("Helvetica", 11)).pack(
            side="left", padx=10
        )
        self.reset_password_widget = Entry(frame_password, width=50, borderwidth=2)
        self.code_widget = Entry(frame_code, width=50, borderwidth=2)
        Label(frame_code, text="Enter activation code:", font=("Helvetica", 11)).pack(
            side="left", padx=10
        )
        self.reset_name_widget.pack(side="left", anchor="e")
        self.reset_password_widget.pack(side="left", anchor="w")
        self.code_widget.pack(side="left", anchor="w")

        Button(frame_buttons, text="Submit", width=10, command=self.on_reset).pack(
            side="top"
        )

        frame_username.pack(side="top", anchor="nw")
        frame_password.pack(side="top", anchor="nw")
        frame_code.pack(side="top", anchor="nw")
        frame_buttons.pack(side="top", anchor="nw")
        frame_buttons

    def file_transfer(self,so:socket.socket()):
        '''
        file = open('client-file.txt', 'wb')
        # Keep receiving data from the server
        line = so.recv(1024)'''
        filename = "data.csv"
        # get the file size
        filesize = os.path.getsize(filename)
        # start sending the file
        so.send(f"{filename}{SEPARATOR}{filesize}".encode())

        progress = tqdm.tqdm(range(
            filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in
                # busy networks
                so.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        # close the socket
        so.close()


        while(line):
            file.write(line)
            line = so.recv(1024)
        print('File has been received successfully.')

    def on_reset(self):
        if (
            self.reset_name_widget.get() == ""
            or self.reset_password_widget.get() == ""
            or self.code_widget.get() == ""
        ):
            messagebox.showerror("Empty Fields", "Fill all the fields")
            return

        self.client_socket.sendall(
            (
                f"RESET_PASSWORD: {self.reset_name_widget.get()}$$${self.reset_password_widget.get()}$$${self.code_widget.get()}"
            ).encode("utf-8")
        )

        self.reset_window.destroy()

    def display_name_section(self):
        frame_username = Frame()
        frame_password = Frame()
        frame_buttons = Frame()
        Label(frame_username, text="Enter username:", font=("Helvetica", 11)).pack(
            side="left", padx=10
        )
        self.name_widget = Entry(frame_username, width=50, borderwidth=2)
        Label(frame_password, text="Enter password:", font=("Helvetica", 11)).pack(
            side="left", padx=10
        )
        self.password_widget = Entry(frame_password, width=50, borderwidth=2)
        self.name_widget.pack(side="left", anchor="e")

        self.password_widget.pack(side="left", anchor="w")
        self.join_button = Button(
            frame_buttons, text="Join", width=10, command=self.on_join
        ).pack(side="top")
        self.register_button = Button(
            frame_buttons, text="Register", width=10, command=self.on_reg
        ).pack(side="top")
        self.forgot_password = Button(
            frame_buttons,
            text="Forgot Password",
            width=10,
            command=self.on_forgot_password,
        ).pack(side="top")
        self.send_file = Button(
            frame_buttons, text="Send File", width=10, command=self.file_transfer
        ).pack(side="top")
        frame_username.pack(side="top", anchor="nw")
        frame_password.pack(side="top", anchor="nw")
        frame_buttons.pack(side="top", anchor="nw")

    def display_chat_box(self):
        frame = Frame()
        frame_online = Frame()
        Label(frame, text="Chat Box:", font=("Serif", 12)).pack(side="top", anchor="w")
        self.chat_transcript_area = Text(frame, width=60, height=10, font=("Serif", 12))
        scrollbar = Scrollbar(
            frame, command=self.chat_transcript_area.yview, orient=VERTICAL
        )
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind("<KeyPress>", lambda e: "break")
        self.chat_transcript_area.pack(side="left", padx=10)
        scrollbar.pack(side="right", fill="y")
        frame.pack(side="top")

        Label(frame_online, text="Online Log:", font=("Serif", 12)).pack(
            side="top", anchor="w"
        )
        self.chat_online_log_area = Text(
            frame_online, width=60, height=10, font=("Serif", 12)
        )
        scrollbar2 = Scrollbar(
            frame_online, command=self.chat_online_log_area.yview, orient=VERTICAL
        )
        self.chat_online_log_area.config(yscrollcommand=scrollbar.set)
        self.chat_online_log_area.pack(side="left", padx=10)
        scrollbar2.pack(side="right", fill="y")

        frame_online.pack(side="top")

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text="Enter message:", font=("Serif", 12)).pack(
            side="top", anchor="w"
        )
        self.enter_text_widget = Text(frame, width=60, height=3, font=("Serif", 12))
        self.enter_text_widget.pack(side="left", pady=15)
        self.enter_text_widget.bind("<Return>", self.on_enter_key_pressed)
        frame.pack(side="top")

    def on_join(self):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror("Enter your name", "Enter your name to send a message")
            return
        self.name_widget.config(state="disabled")
        self.password_widget.config(state="disabled")
        self.client_socket.sendall(
            (
                "joined: " + self.name_widget.get() + "$$$" + self.password_widget.get()
            ).encode("utf-8")
        )

    def on_forgot_password(self):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror(
                "Enter your email",
                "Enter your email to get your password mailed to you.",
            )
            return

        self.client_socket.sendall(
            b"FORGOT_PASSWORD: " + self.name_widget.get().encode("utf-8")
        )

    def on_reg(self):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror("Enter your name", "Enter your name to send a message")
            return
        self.name_widget.config(state="disabled")
        self.password_widget.config(state="disabled")
        self.client_socket.sendall(
            (
                "REG: " + self.name_widget.get() + "$$$" + self.password_widget.get()
            ).encode("utf-8")
        )

    def on_enter_key_pressed(self, event):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror("Enter your name", "Enter your name to send a message")
            return
        self.send_chat()
        self.clear_text()

    def clear_text(self):
        self.enter_text_widget.delete(1.0, "end")

    def send_chat(self):
        senders_name = self.name_widget.get().strip() + ": "
        data = self.enter_text_widget.get(1.0, "end").strip()
        message = (senders_name + data).encode("utf-8")
        self.chat_transcript_area.insert("end", message.decode("utf-8") + "\n")
        self.chat_transcript_area.yview(END)
        self.client_socket.sendall(b"MESSAGE: " + message)
        self.enter_text_widget.delete(1.0, "end")
        return "break"

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            print("EXITING!!")
            self.client_socket.sendall(("EXIT").encode("utf-8"))
            self.client_socket.close()
            exit(0)

    def on_login_fail_close_window(self):
        if messagebox.askokcancel("Quit", "Login failed! Do you want to quit?"):
            self.root.destroy()
            self.client_socket.sendall
            self.client_socket.close()
            exit(0)


# the mail function
if __name__ == "__main__":
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()
