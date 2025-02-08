import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import qrcode
from PIL import Image, ImageTk
import json
import threading
import io

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Panel")

        self.code_word_label = tk.Label(root, text="Code Word", font="Halvetica 20")
        self.code_word_label.grid(row=0, column=0, padx=20, pady=5, sticky="w")

        self.code_word_var = tk.StringVar()
        self.code_word_entry = tk.Entry(root, textvariable=self.code_word_var)
        self.code_word_entry.grid(row=0, column=1, padx=1, pady=5, sticky="w")

        self.update_button = tk.Button(root, text="Update Code", command=self.update_code_word, height=3, width=37, font="Halvetica 10")
        self.update_button.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.start_button = tk.Button(root, text="Start Server", command=self.start_server, height=3, width=37, font="Halvetica 10")
        self.start_button.grid(row=1, column=1, padx=20, pady=5, sticky="w")
        
        self.stop_button = tk.Button(root, text="Stop Server", command=self.stop_server, height=3, width=37, font="Halvetica 10")
        self.stop_button.grid(row=1, column=2, padx=20, pady=5, sticky="w")

        self.log_label = tk.Label(root, text="Logs", font="Halvetica 20")
        self.log_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        self.log_text = scrolledtext.ScrolledText(root, height=20, width=92, font="Halvetica 10")
        self.log_text.grid(row=3, column=0, columnspan=2, padx=18, pady=5, sticky="w")

        self.qr_label = tk.Label(root)
        self.qr_label.grid(row=3, column=2, padx=20, pady=5, sticky="n")
        
        self.server_process = None

        self.generate_qr_code()
        self.load_code_word()

    def load_code_word(self):
        try:
            with open('code.json', 'r') as file:
                data = json.load(file)
                self.code_word_var.set(data['code_word'])
        except (FileNotFoundError, json.JSONDecodeError):
            self.code_word_var.set("")

    def update_code_word(self):
        new_code_word = self.code_word_var.get()
        if not new_code_word:
            messagebox.showwarning("Warning", "Please enter a code word!")
            return

        with open('code.json', 'w') as file:
            json.dump({"code_word": new_code_word}, file)

        messagebox.showinfo("Info", "Code word updated successfully")

    def generate_qr_code(self):
        url = "http://192.168.0.101:5000/control"
        qr = qrcode.make(url)
        qr_img = qr.resize((310, 310))  # Устанавливаем размер QR-кода
        qr_img_tk = ImageTk.PhotoImage(qr_img)
        self.qr_label.config(image=qr_img_tk)
        self.qr_label.image = qr_img_tk

    def start_server(self):
        code_word = self.code_word_var.get()
        if not code_word:
            messagebox.showwarning("Warning", "Please enter a code word!")
            return

        self.server_process = subprocess.Popen(["python", "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        threading.Thread(target=self.read_logs).start()
    
    def stop_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
    
    def read_logs(self):
        while True:
            if not self.server_process:
                break
            line = self.server_process.stdout.readline()
            if not line:
                break
            self.log_text.insert(tk.END, line.decode())
            self.log_text.yview(tk.END)

root = tk.Tk()
app = App(root)
root.mainloop()
