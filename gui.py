import tkinter as tk
from tkinter import messagebox
import subprocess
import qrcode
from PIL import Image, ImageTk
import json
import threading

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Panel")
        
        self.code_word_label = tk.Label(root, text="Current Code Word")
        self.code_word_label.pack()

        self.code_word_entry = tk.Entry(root)
        self.code_word_entry.pack()
        self.load_code_word()
        
        self.update_button = tk.Button(root, text="Update Code Word", command=self.update_code_word)
        self.update_button.pack()

        self.start_button = tk.Button(root, text="Start Server", command=self.start_server)
        self.start_button.pack()
        
        self.stop_button = tk.Button(root, text="Stop Server", command=self.stop_server)
        self.stop_button.pack()
        
        self.qr_label = tk.Label(root)
        self.qr_label.pack()
        
        self.log_text = tk.Text(root, height=10)
        self.log_text.pack()
        
        self.server_process = None
        
        self.generate_qr_code()
    
    def load_code_word(self):
        with open('code.json', 'r') as file:
            data = json.load(file)
            self.code_word_entry.insert(0, data['code_word'])

    def update_code_word(self):
        new_code_word = self.code_word_entry.get()
        if not new_code_word:
            messagebox.showwarning("Warning", "Please enter a code word!")
            return

        with open('code.json', 'w') as file:
            json.dump({"code_word": new_code_word}, file)

        messagebox.showinfo("Info", "Code word updated successfully")

    def generate_qr_code(self):
        url = "http://192.168.0.101:5000/control"
        qr = qrcode.make(url)
        qr_img = ImageTk.PhotoImage(qr)
        self.qr_label.config(image=qr_img)
        self.qr_label.image = qr_img

    def start_server(self):
        code_word = self.code_word_entry.get()
        if not code_word:
            messagebox.showwarning("Warning", "Please enter a code word!")
            return

        # Start the Flask server
        self.server_process = subprocess.Popen(["python", "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Start a new thread to read logs
        threading.Thread(target=self.read_logs).start()
    
    def stop_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
    
    def read_logs(self):
        while True:
            line = self.server_process.stdout.readline()
            if not line:
                break
            self.log_text.insert(tk.END, line.decode())

root = tk.Tk()
app = App(root)
root.mainloop()
