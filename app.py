
import tkinter as tk
import base64
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import RSA

from primePy import primes

class EncryptionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat App")
        self.padding = 2
        
        self.alice_public_key = None
        self.alice_n = None
        self.alice_private_key = None
        
        self.bob_public_key = None
        self.bob_n = None
        self.bob_private_key = None
        self.isBinary_alice = False
        self.isBinary_bob = False
        self.defaultExtension = None
        
        # Title
        self.alice_label = ttk.Label(master, text="ALICE", font=("Helvetica", 16, "bold"))
        self.alice_label.grid(row=0, column=0, columnspan=2, padx=self.padding, pady=self.padding, sticky="w")

        self.bob_label = ttk.Label(master, text="Bob", font=("Helvetica", 16, "bold"))
        self.bob_label.grid(row=0, column=2, columnspan=2, padx=self.padding, pady=self.padding, sticky="w")
        
        # Input P
        self.input_p_label_alice = ttk.Label(master, text="Input P:")
        self.input_p_label_alice.grid(row=1, column=0, padx=self.padding, pady=self.padding, sticky="w")
        
        self.input_p_entry_alice = ttk.Entry(master)
        self.input_p_entry_alice.grid(row=1, column=1, padx=self.padding, pady=self.padding, sticky="w")
        
        self.input_p_label_bob = ttk.Label(master, text="Input P:")
        self.input_p_label_bob.grid(row=1, column=2, padx=self.padding, pady=self.padding, sticky="w")
        
        self.input_p_entry_bob = ttk.Entry(master)
        self.input_p_entry_bob.grid(row=1, column=3, padx=self.padding, pady=self.padding, sticky="w")
        
        # Input Q
        self.input_q_label_alice = ttk.Label(master, text="Input Q:")
        self.input_q_label_alice.grid(row=2, column=0, padx=self.padding, pady=self.padding, sticky="w")
        
        self.input_q_entry_alice = ttk.Entry(master)
        self.input_q_entry_alice.grid(row=2, column=1, padx=self.padding, pady=self.padding, sticky="w")

        self.input_q_label_bob = ttk.Label(master, text="Input Q:")
        self.input_q_label_bob.grid(row=2, column=2, padx=self.padding, pady=self.padding, sticky="w")
        
        self.input_q_entry_bob = ttk.Entry(master)
        self.input_q_entry_bob.grid(row=2, column=3, padx=self.padding, pady=self.padding, sticky="w")
        
        # Generate Key
        self.generate_key_button_alice = ttk.Button(master, text="Generate Key", command=self.generate_key_alice)
        self.generate_key_button_alice.grid(row=3, column=0, padx=self.padding, pady=self.padding, sticky="w")

        self.generate_key_button_bob = ttk.Button(master, text="Generate Key", command=self.generate_key_bob)
        self.generate_key_button_bob.grid(row=3, column=2, padx=self.padding, pady=self.padding, sticky="w")
        
        # Send Public Key
        self.send_public_key_button_alice = ttk.Button(master, text="Send Public Key", command=self.send_public_key_alice)
        self.send_public_key_button_alice.grid(row=4, column=0, padx=self.padding, pady=self.padding, sticky="w")
        
        self.send_public_key_button_bob = ttk.Button(master, text="Send Public Key", command=self.send_public_key_bob)
        self.send_public_key_button_bob.grid(row=4, column=2, padx=self.padding, pady=self.padding, sticky="w")
        
        # Input Message
        self.input_type_var_alice = tk.StringVar()
        self.input_type_var_alice.set("Text")
        
        self.input_type_label_alice = ttk.Label(master, text="Select Input Type:")
        self.input_type_label_alice.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.input_type_menu_alice = ttk.OptionMenu(master, self.input_type_var_alice, "Text", "Text", "File", command=self.toggle_input_alice)
        self.input_type_menu_alice.grid(row=5, column=1, padx=5, pady=5)
        
        self.message_label_alice = ttk.Label(master, text="Input Message (Alice):")
        self.message_label_alice.grid(row=6, column=0, padx=self.padding, pady=self.padding, sticky="w")

        self.input_file_button_alice = ttk.Button(master, text="Open File", command=self.open_file_alice)
        # self.upload_button_alice.grid(row=6, column=1, padx=self.padding, pady=self.padding, sticky="w")
        
        
        self.input_text_alice = tk.Text(master, height=5, width=40)
        self.input_text_alice.grid(row=7, column=0, padx=self.padding, pady=self.padding, columnspan=2, sticky="w")

        self.input_type_var_bob = tk.StringVar()
        self.input_type_var_bob.set("Text")
        
        self.input_type_label_bob = ttk.Label(master, text="Select Input Type:")
        self.input_type_label_bob.grid(row=5, column=2, padx=5, pady=5, sticky="w")
        
        self.input_type_menu_bob = ttk.OptionMenu(master, self.input_type_var_bob, "Text", "Text", "File", command=self.toggle_input_bob)
        self.input_type_menu_bob.grid(row=5, column=3, padx=5, pady=5)
        
        self.message_label_bob = ttk.Label(master, text="Input Message (Bob):")
        self.message_label_bob.grid(row=6, column=2, padx=self.padding, pady=self.padding, sticky="w")

        self.input_file_button_bob = ttk.Button(master, text="Open File", command=self.open_file_bob)
        # self.upload_button_bob.grid(row=6, column=3, padx=self.padding, pady=self.padding, sticky="w")
        
        self.file_label_alice = ttk.Label(master, text="")
        self.file_label_alice.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        
        self.file_label_bob = ttk.Label(master, text="")
        self.file_label_bob.grid(row=6, column=3, padx=5, pady=5, sticky="w")
        
        self.input_text_bob = tk.Text(master, height=5, width=40)
        self.input_text_bob.grid(row=7, column=2, padx=self.padding, pady=self.padding, columnspan=2, sticky="w")
        
        # Send Button
        self.send_button_alice = ttk.Button(master, text="Send", command=self.send_message_alice)
        self.send_button_alice.grid(row=8, column=0, columnspan=2, padx=self.padding, pady=self.padding, sticky="w")

        self.send_button_bob = ttk.Button(master, text="Send", command=self.send_message_bob)
        self.send_button_bob.grid(row=8, column=2, columnspan=2, padx=self.padding, pady=self.padding, sticky="w")        
        
        # Chatbox
        self.chatbox_label_alice = ttk.Label(master, text="Chat Inbox from Bob:")
        self.chatbox_label_alice.grid(row=9, column=0, padx=self.padding, pady=self.padding, sticky="w")

        self.save_encrypted_file_button_alice = ttk.Button(master, text="Save Encrypted File", command=self.save_encrypted_file_alice)

        self.chatbox_text_alice = tk.Text(master, height=8, width=60)
        self.chatbox_text_alice.grid(row=10, column=0, columnspan=2, padx=self.padding, pady=self.padding)

        self.chatbox_label_bob = ttk.Label(master, text="Chat Inbox from Alice:")
        self.chatbox_label_bob.grid(row=9, column=2, padx=self.padding, pady=self.padding, sticky="w")

        self.save_encrypted_file_button_bob = ttk.Button(master, text="Save Encrypted File", command=self.save_encrypted_file_bob)

        self.chatbox_text_bob = tk.Text(master, height=8, width=60)
        self.chatbox_text_bob.grid(row=10, column=2, columnspan=2, padx=self.padding, pady=self.padding)

        # Decrypt Button
        self.decrypt_button_alice = ttk.Button(master, text="decrypt", command=self.decrypt_message_alice)
        self.decrypt_button_alice.grid(row=11, column=0, columnspan=2, padx=self.padding, pady=self.padding, sticky="w")

        self.decrypt_button_bob = ttk.Button(master, text="decrypt", command=self.decrypt_message_bob)
        self.decrypt_button_bob.grid(row=11, column=2, columnspan=2, padx=self.padding, pady=self.padding, sticky="w")
        
        # Decrypted Result
        self.save_decrypted_file_button_alice = ttk.Button(master, text="Save Decrypted File", command=self.save_decrypted_file_alice)

        self.decrypted_chatbox_alice = tk.Text(master, height=5, width=60)
        self.decrypted_chatbox_alice.grid(row=12, column=0, columnspan=2, padx=self.padding, pady=self.padding)

        self.save_decrypted_file_button_bob = ttk.Button(master, text="Save Decrypted File", command=self.save_decrypted_file_bob)

        self.decrypted_chatbox_bob = tk.Text(master, height=5, width=60)
        self.decrypted_chatbox_bob.grid(row=12, column=2, columnspan=2, padx=self.padding, pady=self.padding)        

        # # Save Button
        # self.save_button_alice = ttk.Button(master, text="save", command=self.save_output_alice)
        # self.save_button_alice.grid(row=13, column=0, columnspan=2, padx=self.padding, pady=self.padding, sticky="w")

        # self.save_button_bob = ttk.Button(master, text="save", command=self.save_output_bob)
        # self.save_button_bob.grid(row=13, column=2, columnspan=2, padx=self.padding, pady=self.padding, sticky="w")
        
    def generate_key_alice(self):
        p = int(self.input_p_entry_alice.get())
        q = int(self.input_q_entry_alice.get())
        print(p)
        print(q)
        print("tes")
        if primes.check(p) and primes.check(q):
            self.alice_public_key, self.alice_private_key, self.alice_n = RSA.generateKey(p, q)
            print("tes")
            with open("alice.pub", "w") as file:
                file.write(f"{self.alice_public_key} {self.alice_n}")
            with open("alice.pri", "w") as file:
                file.write(f"{self.alice_private_key} {self.alice_n}")
            messagebox.showinfo("Success", "Keys generated and saved successfully.")
        else:
            messagebox.showinfo("Failed", "Keys failed to generate")

    def generate_key_bob(self):
        p = int(self.input_p_entry_bob.get())
        q = int(self.input_q_entry_bob.get())
        if primes.check(p) and primes.check(q):
            self.bob_public_key, self.bob_private_key, self.bob_n = RSA.generateKey(p, q)
            with open("bob.pub", "w") as file:
                file.write(f"{self.bob_public_key} {self.bob_n}")
            with open("bob.pri", "w") as file:
                file.write(f"{self.bob_private_key} {self.bob_n}")
            messagebox.showinfo("Success", "Bob key generated and saved successfully.")
            
    def send_public_key_alice(self):
        try:
            # Read Public Key
            with open("alice.pub", "r") as file:
                file_content = file.read().strip().split()
                if len(file_content) != 2:
                    messagebox.showerror("Error", "Cek lagi file!")
                self.alice_public_key, self.alice_n = int(file_content[0]), int(file_content[1])
            
            # Read Private Key
            with open("alice.pri", "r") as file:
                file_content = file.read().strip().split()
                if len(file_content) != 2:
                    messagebox.showerror("Error", "Cek lagi file!")
                self.alice_private_key, self.alice_n = int(file_content[0]), int(file_content[1])
                
            messagebox.showinfo("Success", "Public key successfully sent!")
            
        except FileNotFoundError:
            messagebox.showerror("Error", "alice.pub not found!")
    
    def send_public_key_bob(self):
        try:
            # Read Public Key
            with open("bob.pub", "r") as file:
                file_content = file.read().strip().split()
                if len(file_content) != 2:
                    messagebox.showerror("Error", "Cek lagi file!")
                self.bob_public_key, self.bob_n = int(file_content[0]), int(file_content[1])
            
            # Read Private Key
            with open("bob.pri", "r") as file:
                file_content = file.read().strip().split()
                if len(file_content) != 2:
                    messagebox.showerror("Error", "Cek lagi file!")
                self.bob_private_key, self.bob_n = int(file_content[0]), int(file_content[1])
                
            messagebox.showinfo("Success", "Public key successfully sent!")
            
        except FileNotFoundError:
            messagebox.showerror("Error", "alice.pub not found!")
        pass

    def toggle_input_alice(self, *args):
        input_type = self.input_type_var_alice.get()
        if input_type == "Text":
            self.isBinary_alice = False
            self.input_text_alice.grid(row=7, column=0, padx=5, pady=5, columnspan=2)
            self.input_file_button_alice.grid_remove()
            self.file_label_alice.grid_remove()
            self.input_text_alice.delete("1.0", tk.END)
            self.file_label_alice.grid_remove()
        elif input_type == "File":
            self.isBinary = True
            self.input_text_alice.grid_remove()
            # self.input_label.grid_remove()
            self.input_file_button_alice.grid(row=7, column=0, padx=5, pady=5, columnspan=2)

    def toggle_input_bob(self, *args):
        input_type = self.input_type_var_bob.get()
        if input_type == "Text":
            self.isBinary_bob = False
            self.input_text_bob.grid(row=7, column=2, padx=5, pady=5, columnspan=2)
            self.input_file_button_bob.grid_remove()
            self.file_label_bob.grid_remove()
            self.input_text_bob.delete("1.0", tk.END)
            self.file_label_bob.grid_remove()
        elif input_type == "File":
            self.isBinary_bob = True
            self.input_text_bob.grid_remove()
            # self.file_label_bob.grid_remove()
            self.input_file_button_bob.grid(row=7, column=2, padx=5, pady=5, columnspan=2)

    def open_file_alice(self):
        self.isBinary_alice = True
        file_path = filedialog.askopenfilename()
        file_byteintarray = RSA.read_file_bytes(file_path)
        self.content_alice = file_byteintarray
        messagebox.showinfo("Success", "Upload file " + file_path + " berhasil")
        self.file_label_alice.config(text="File: " + file_path)
        
        # if file_path[-4:] != ".txt":
        #     self.isBinary = True
        #     self.defaultExtension = file_path[-4:]
        # if file_path and not self.isBinary:
        #     with open(file_path, "r") as file:
        #         content = file.read()
        #         self.input_text.delete("1.0", tk.END)
        #         self.input_text.insert("1.0", content)
        # elif self.isBinary:
            # with open(file_path, "rb") as file:
            #     content = file.read()
            #     ## base64_content = base64.b64encode(content).decode('utf-8')
            #     self.input_text.delete("1.0", tk.END)
            #     self.input_text.insert("1.0", content)

            #     self.content = content
            # # Update file label to display the filename
            # self.file_label.config(text="File: " + file_path)

    def open_file_bob(self):
        self.isBinary_bob = True
        file_path = filedialog.askopenfilename()
        file_byteintarray = RSA.read_file_bytes(file_path)
        self.content_bob = file_byteintarray
        messagebox.showinfo("Success", "Upload file " + file_path + " berhasil")
        self.file_label_bob.config(text="File: " + file_path)

    def send_message_alice(self):
        if not self.isBinary_alice:
            input_text_alice = self.input_text_alice.get("1.0", "end-1c")
            is_file = False
        else:
            is_file = True
        bob_public_key = self.bob_public_key
        bob_n = self.bob_n
        block_size = 1
        
        if self.bob_public_key == None:
            messagebox.showerror("Error", "Bob has not sent public key yet!")
            return

        if not self.isBinary_alice:
            self.encrypted_text_alice = RSA.encrypt(input_text_alice, bob_public_key, bob_n, block_size, is_file)
            
            print(self.encrypted_text_alice)
            self.chatbox_text_bob.grid(row=10, column=2, padx=5, pady=5, columnspan=2)
            self.save_encrypted_file_button_bob.grid_remove()
            self.chatbox_text_bob.delete("1.0", tk.END)
            self.chatbox_text_bob.insert(tk.END, base64.b64encode(self.encrypted_text_alice.encode()).decode())
        else:
            self.chatbox_text_bob.grid_remove()
            self.save_encrypted_file_button_bob.grid(row=10, column=2, padx=5, pady=5, columnspan=2)

            encrypted_file = RSA.encrypt(self.content_alice, bob_public_key, bob_n, block_size, is_file)
            self.encrypted_content_bob = RSA.HexStringToByteIntArray(encrypted_file)
    
    def send_message_bob(self):
        if not self.isBinary_bob:
            input_text_bob = self.input_text_bob.get("1.0", "end-1c")
            is_file = False
        else:
            is_file = True
        alice_public_key = self.alice_public_key
        alice_n = self.alice_n
        block_size = 1
        
        print("iasdas")
        if self.alice_public_key == None:
            messagebox.showerror("Error", "Alice has not sent public key yet!")
            return

        if not self.isBinary_bob:
            self.encrypted_text_bob = RSA.encrypt(input_text_bob, alice_public_key, alice_n, block_size, is_file)
            print("tes")
            print(self.encrypted_text_bob)
            self.chatbox_text_alice.grid(row=10, column=0, padx=5, pady=5, columnspan=2)
            self.save_encrypted_file_button_alice.grid_remove()
            self.chatbox_text_alice.delete("1.0", tk.END)
            self.chatbox_text_alice.insert(tk.END, base64.b64encode(self.encrypted_text_bob.encode()).decode())
        else:
            print("masuk lagi ga")
            self.chatbox_text_alice.grid_remove()
            self.save_encrypted_file_button_alice.grid(row=10, column=0, padx=5, pady=5, columnspan=2)
            
            encrypted_file = RSA.encrypt(self.content_bob, alice_public_key, alice_n, block_size, is_file)
            self.encrypted_content_alice = RSA.HexStringToByteIntArray(encrypted_file)
         
    def decrypt_message_alice(self):
        print("isBinaryBob: " + str(self.isBinary_bob))
        if not self.isBinary_bob:
            decrypted_message = RSA.decrypt(self.encrypted_text_bob, self.alice_private_key, self.alice_n)
            print(decrypted_message)
            self.save_decrypted_file_button_alice.grid_remove()
            self.decrypted_chatbox_alice.grid(row=12, column=0, padx=5, pady=5, columnspan=2)
            self.decrypted_chatbox_alice.delete("1.0", tk.END)
            self.decrypted_chatbox_alice.insert(tk.END, bytes(decrypted_message))
        else:
            self.decrypted_chatbox_alice.grid_remove()
            self.save_decrypted_file_button_alice.grid(row=12, column=0, padx=5, pady=5, columnspan=2)
            decrypted_file_hex = RSA.ByteIntArrayToHexString(self.encrypted_content_alice)
            self.decrypted_content_alice = RSA.decrypt(decrypted_file_hex, self.alice_private_key, self.alice_n)

    def decrypt_message_bob(self):
        if not self.isBinary_alice:
            decrypted_message = RSA.decrypt(self.encrypted_text_alice, self.bob_private_key, self.bob_n)
            self.save_decrypted_file_button_bob.grid_remove()
            self.decrypted_chatbox_bob.grid(row=12, column=2, padx=5, pady=5, columnspan=2)
            self.decrypted_chatbox_bob.delete("1.0", tk.END)
            self.decrypted_chatbox_bob.insert(tk.END, bytes(decrypted_message))
        else:
            self.decrypted_chatbox_bob.grid_remove()
            self.save_decrypted_file_button_bob.grid(row=12, column=2, padx=5, pady=5, columnspan=2)
            decrypted_file_hex = RSA.ByteIntArrayToHexString(self.encrypted_content_bob)
            self.decrypted_content_bob = RSA.decrypt(decrypted_file_hex, self.bob_private_key, self.bob_n)
   
    def save_file_types_alice(self):
        filetypes = []
        print("coba")
        if not self.isBinary_bob:
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
    
    def save_file_types_bob(self):
        filetypes = []
        print("coba")
        if not self.isBinary_alice:
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
        file_types = self.save_file_types_bob()
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

    def save_encrypted_file_alice(self):
        file_types = self.save_file_types_alice()
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=file_types)
        if file_path:
            with open(file_path, "wb") as file:
                for byteint in self.encrypted_content_alice:
                    file.write(byteint.to_bytes(1, byteorder='little'))
            messagebox.showinfo("Success", "Encrypted File downloaded succesfully!")
    
    def save_encrypted_file_bob(self):
        file_types = self.save_file_types_bob()
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=file_types)
        if file_path:
            with open(file_path, "wb") as file:
                for byteint in self.encrypted_content_alice:
                    file.write(byteint.to_bytes(1, byteorder='little'))
            messagebox.showinfo("Success", "Encrypted File downloaded succesfully!")
    
    def save_decrypted_file_alice(self):
        print("tes1")
        file_types = self.save_file_types_alice()
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=file_types)
        print("tes2")
        if file_path:
            print("tes3")
            with open(file_path, "wb") as file:
                for byteint in self.decrypted_content_alice:
                    file.write(byteint.to_bytes(1, byteorder='little'))
            messagebox.showinfo("Success", "Decrypted File downloaded succesfully!")

    def save_decrypted_file_bob(self):
        print("tes1")
        file_types = self.save_file_types_bob()
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=file_types)
        print("tes2")
        if file_path:
            print("tes3")
            with open(file_path, "wb") as file:
                for byteint in self.decrypted_content_bob:
                    file.write(byteint.to_bytes(1, byteorder='little'))
            messagebox.showinfo("Success", "Decrypted File downloaded succesfully!")

    
    def save_output_alice(self):
        pass
    
    def save_output_bob(self):
        pass
        
def main():
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()