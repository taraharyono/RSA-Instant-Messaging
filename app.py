
import tkinter as tk
import base64
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
## from PIL import Image, ImageTk
## from cryptography.fernet import Fernet
import pyperclip
import RSA

from primePy import primes

class EncryptionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat App")
        self.padding = 2
        
        # Alice Section
        self.alice_label = ttk.Label(master, text="ALICE", font=("Helvetica", 16, "bold"))
        self.alice_label.grid(row=0, column=0, columnspan=2, padx=self.padding, pady=self.padding, sticky="w")

        self.input_p_label_alice = ttk.Label(master, text="Input P:")
        self.input_p_label_alice.grid(row=1, column=0, padx=self.padding, pady=self.padding, sticky="w")
        
        self.input_p_entry_alice = ttk.Entry(master)
        self.input_p_entry_alice.grid(row=1, column=1, padx=self.padding, pady=self.padding, sticky="w")
        
        self.input_q_label_alice = ttk.Label(master, text="Input Q:")
        self.input_q_label_alice.grid(row=2, column=0, padx=self.padding, pady=self.padding, sticky="w")
        
        self.input_q_entry_alice = ttk.Entry(master)
        self.input_q_entry_alice.grid(row=2, column=1, padx=self.padding, pady=self.padding, sticky="w")

        self.generate_key_button_alice = ttk.Button(master, text="Generate Key", command=self.generate_key_alice)
        self.generate_key_button_alice.grid(row=3, column=0, padx=self.padding, pady=self.padding, sticky="w")

        self.send_public_key_button_alice = ttk.Button(master, text="Send Public Key", command=self.send_public_key_alice)
        self.send_public_key_button_alice.grid(row=4, column=0, padx=self.padding, pady=self.padding, sticky="w")

        # Bob Section
        self.bob_label = ttk.Label(master, text="Bob", font=("Helvetica", 16, "bold"))
        self.bob_label.grid(row=0, column=2, columnspan=2, padx=self.padding, pady=self.padding, sticky="w")

        self.input_p_label_bob = ttk.Label(master, text="Input P:")
        self.input_p_label_bob.grid(row=1, column=2, padx=self.padding, pady=self.padding, sticky="w")
        
        self.input_p_entry_bob = ttk.Entry(master)
        self.input_p_entry_bob.grid(row=1, column=3, padx=self.padding, pady=self.padding, sticky="w")
        
        self.input_q_label_bob = ttk.Label(master, text="Input Q:")
        self.input_q_label_bob.grid(row=2, column=2, padx=self.padding, pady=self.padding, sticky="w")
        
        self.input_q_entry_bob = ttk.Entry(master)
        self.input_q_entry_bob.grid(row=2, column=3, padx=self.padding, pady=self.padding, sticky="w")

        self.generate_key_button_bob = ttk.Button(master, text="Generate Key", command=self.generate_key_bob)
        self.generate_key_button_bob.grid(row=3, column=2, padx=self.padding, pady=self.padding, sticky="w")

        self.send_public_key_button_bob = ttk.Button(master, text="Send Public Key", command=self.send_public_key_bob)
        self.send_public_key_button_bob.grid(row=4, column=2, padx=self.padding, pady=self.padding, sticky="w")

        # Alice Input Section
        self.select_input_label_alice = ttk.Label(master, text="Select Input Type (Alice):")
        self.select_input_label_alice.grid(row=5, column=0, padx=self.padding, pady=self.padding, sticky="w")

        self.input_type_var_alice = tk.StringVar()
        self.input_type_var_alice.set("Text")
        self.input_type_menu_alice = ttk.OptionMenu(master, self.input_type_var_alice, "Text", "Text", "File", command=self.toggle_input_alice)
        self.input_type_menu_alice.grid(row=5, column=1, padx=self.padding, pady=self.padding, sticky="w")

        self.message_label_alice = ttk.Label(master, text="Input Message (Alice):")
        self.message_label_alice.grid(row=6, column=0, padx=self.padding, pady=self.padding, sticky="w")

        self.upload_button_alice = ttk.Button(master, text="Upload File", command=self.upload_file_alice)
        self.upload_button_alice.grid(row=6, column=1, padx=self.padding, pady=self.padding, sticky="w")

        self.input_text_alice = tk.Text(master, height=5, width=40)
        self.input_text_alice.grid(row=7, column=0, padx=self.padding, pady=self.padding, columnspan=2, sticky="w")

        self.chatbox_label_alice = ttk.Label(master, text="Chatbox (Alice Sent and Bob Received Messages):")
        self.chatbox_label_alice.grid(row=8, column=0, padx=self.padding, pady=self.padding, sticky="w")

        self.chatbox_text_alice = tk.Text(master, height=10, width=60)
        self.chatbox_text_alice.grid(row=9, column=0, columnspan=3, padx=self.padding, pady=self.padding)

        # Bob Input Section
        self.select_input_label_bob = ttk.Label(master, text="Select Input Type (Bob):")
        self.select_input_label_bob.grid(row=5, column=2, padx=self.padding, pady=self.padding, sticky="w")

        self.input_type_var_bob = tk.StringVar()
        self.input_type_var_bob.set("Text")
        self.input_type_menu_bob = ttk.OptionMenu(master, self.input_type_var_bob, "Text", "Text", "File", command=self.toggle_input_bob)
        self.input_type_menu_bob.grid(row=5, column=3, padx=self.padding, pady=self.padding, sticky="w")

        self.message_label_bob = ttk.Label(master, text="Input Message (Bob):")
        self.message_label_bob.grid(row=6, column=2, padx=self.padding, pady=self.padding, sticky="w")

        self.upload_button_bob = ttk.Button(master, text="Upload File", command=self.upload_file_bob)
        self.upload_button_bob.grid(row=6, column=3, padx=self.padding, pady=self.padding, sticky="w")

        self.input_text_bob = tk.Text(master, height=5, width=40)
        self.input_text_bob.grid(row=7, column=2, padx=self.padding, pady=self.padding, columnspan=2, sticky="w")

        self.chatbox_label_bob = ttk.Label(master, text="Chatbox (Bob Sent and Alice Received Messages):")
        self.chatbox_label_bob.grid(row=8, column=2, padx=self.padding, pady=self.padding, sticky="w")

        self.chatbox_text_bob = tk.Text(master, height=10, width=60)
        self.chatbox_text_bob.grid(row=9, column=2, columnspan=3, padx=self.padding, pady=self.padding)

    def generate_key_alice(self):
        p = int(self.input_p_entry_alice.get())
        q = int(self.input_q_entry_alice.get())
        if primes.check(p) and primes.check(q):
            self.alice_public_key, self.alice_private_key, self.alice_n = RSA.generateKey(p, q)
            with open("alice.pub", "w") as file:
                file.write(f"{self.alice_public_key} {self.alice_n}")
            with open("alice.pri", "w") as file:
                file.write(f"{self.alice_private_key} {self.alice_n}")
            messagebox.showinfo("Success", "Keys generated and saved successfully.")

    def send_public_key_alice(self):
        # Add logic to send public key from Alice
        pass

    def generate_key_bob(self):
        p = int(self.input_p_entry_bob.get())
        q = int(self.input_q_entry_bob.get())
        if primes.check(p) and primes.check(q):
            self.bob_public_key, self.bob_private_key, self.bob_n = RSA.generateKey(p, q)
            with open("bob.pub", "w") as file:
                file.write(f"{self.bob_public_key} {self.bob_n}")
            with open("bob.pri", "w") as file:
                file.write(f"{self.bob_private_key} {self.bob_n}")
            messagebox.showinfo("Success", "Keys generated and saved successfully.")
        pass
    def send_public_key_bob(self):
        # Add logic to send public key from Bob
        pass

    def toggle_input_alice(self, *args):
        input_type = self.input_type_var_alice.get()
        if input_type == "Text":
            self.input_text_alice.grid(row=7, column=0, padx=self.padding, pady=self.padding, columnspan=2, sticky="w")
            self.upload_button_alice.grid_remove()
        elif input_type == "File":
            self.input_text_alice.grid_remove()
            self.upload_button_alice.grid(row=6, column=1, padx=self.padding, pady=self.padding, sticky="w")

    def toggle_input_bob(self, *args):
        input_type = self.input_type_var_bob.get()
        if input_type == "Text":
            self.input_text_bob.grid(row=7, column=2, padx=self.padding, pady=self.padding, columnspan=2, sticky="w")
            self.upload_button_bob.grid_remove()
        elif input_type == "File":
            self.input_text_bob.grid_remove()
            self.upload_button_bob.grid(row=6, column=3, padx=self.padding, pady=self.padding, sticky="w")

    def upload_file_alice(self):
        file_path = filedialog.askopenfilename()
        if file_path[-4:] != ".txt":
            self.isBinary = True
            self.defaultExtension = file_path[-4:]
        if file_path and not self.isBinary:
            with open(file_path, "r") as file:
                content = file.read()
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", content)
                ## print("base64" + base64_content)
        elif self.isBinary:
            with open(file_path, "rb") as file:
                content = file.read()
                ## base64_content = base64.b64encode(content).decode('utf-8')
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", content)

                self.content = content

            
            # Update file label to display the filename
            self.file_label.config(text="File: " + file_path)

    def upload_file_bob(self):
        file_path = filedialog.askopenfilename()
        if file_path[-4:] != ".txt":
            self.isBinary = True
            self.defaultExtension = file_path[-4:]
        if file_path and not self.isBinary:
            with open(file_path, "r") as file:
                content = file.read()
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", content)
                ## print("base64" + base64_content)
        elif self.isBinary:
            with open(file_path, "rb") as file:
                content = file.read()
                ## base64_content = base64.b64encode(content).decode('utf-8')
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", content)

                self.content = content

            
            # Update file label to display the filename
            self.file_label.config(text="File: " + file_path)
    
    def save_file_types(self):
        filetypes = []
        print("coba")
        if not self.isBinary:
            filetypes.append(("Text files", "*.txt"))
        elif self.defaultExtension == ".png":
            filetypes.append(("PNG", "*.png"))
        elif self.defaultExtension == ".pdf":
            filetypes.append(("PDF", "*.pdf"))
        elif self.defaultExtension == ".csv":
            filetypes.append(("CSV", "*.csv"))
        elif self.defaultExtension == ".gif":
            filetypes.append(("GIF", "*.gif"))
        elif self.defaultExtension == ".mp4":
            filetypes.append(("MP4", "*.mp4"))
        else:
            filetypes.append(("All files", "*.*"))
        return filetypes

    def save_output(self):
        output_text = self.output_text.get("1.0", "end-1c")
        if not output_text and not self.isBinary:
            messagebox.showerror("Error", "No output to save.")
            return
        file_types = self.save_file_types()
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=file_types)
        if file_path:
            if not self.isBinary:  # If the data is text
                with open(file_path, "w") as file:
                    file.write(output_text)
            else:  # If the data is binary
                with open(file_path, "wb") as file:
                    file.write(self.byteArray)

            messagebox.showinfo("Success", "Output saved successfully.")
        else:
            self.file_label.grid_remove()

                
    def process(self):
        input_text = self.input_text.get("1.0", "end-1c")
        choice = self.choice_var.get()
        technique = self.technique_var.get()
        key = self.key_entry.get()

        if not input_text and not self.content:
            messagebox.showerror("Error", "Please enter some text.")
            return

        if not key:
            messagebox.showerror("Error", "Please enter a key.")
            return

        
def main():
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()