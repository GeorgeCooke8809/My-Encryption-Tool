import customtkinter
from tkinter import filedialog
from tkinter import *
from matplotlib import pyplot as plt
import Encryption  
import RSAEncryption

class App(customtkinter.CTk):
    """
    This class is used to make the main window within which the rest of the app is housed.
    """
    def __init__(self):
        super().__init__()

        self.geometry("1000x600")
        self.minsize(width = 700, height = 350)
        self.title("OOP Encryptor - By George A.C. Cooke")

        self.master_frame = MasterFrame(self)

        self.mainloop()

class MasterFrame(customtkinter.CTkFrame):
    """
    This class houses the frame that is passed directly in to the main window and has the navigation menu at the top.
    It also houses the logic needed to switch between pages when the navigation menu is used.
    """
    def __init__(self, parent): # Basic Initialization
        super().__init__(parent)

        self.create_widgets()

        self.pack(anchor = "center", expand = True, fill = "both")

    def create_widgets(self): # Make the widgets that will later be drawn to the window
        self.widget_menu_buttons = customtkinter.CTkSegmentedButton(self, values = ["Directional Caesar", "Directional Polyshift", "Vernam", "RSA", "Notepad"], command  = self.switch_page, font = ("TkDefaultFont", 20))
        self.widget_menu_buttons.set("Directional Caesar")

        self.widget_learn_more = customtkinter.CTkButton(self, text = "Learn More", font = ("TkDefaultFont", 20), command = self.learn_more_page) # TODO: add command

        self.content = Basic(self, "Directional Caesar")

        self.draw_widgets()

    def draw_widgets(self): # Draw the widgets and display them on the window
        self.rowconfigure(0, weight = 1, minsize = 20)
        self.rowconfigure(1, weight = 100000, minsize = 80)
        self.columnconfigure(0, weight = 9)
        self.columnconfigure(1, weight = 1)

        self.widget_menu_buttons.grid(row = 0, column = 0, sticky = "nsw", padx = 10, pady = 10)
        self.widget_learn_more.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "nsew")
        self.content.grid(row=1, column = 0, columnspan = 2, rowspan = 1, sticky = "nsew")

    def switch_page(self, value = None): # Handles the logic of switching between different pages
        page = self.widget_menu_buttons.get()
        self.content.destroy()

        if page in ["Directional Caesar", "Directional Polyshift", "Vernam"]:
            self.content = Basic(self, page)
        elif page == "RSA":
            self.content = RSA_Page(self)
        elif page == "Notepad":
            self.content = Notepad(self)

    def learn_more_page(self):
        LearnMore(self)

class Basic(customtkinter.CTkFrame):
    """
    This class houses the windows for each of the sandbox pages and draws them to the window.
    Housed within it is also the logic for updating the input and output boxes when one of them is changed.
    """
    def __init__(self, parent, form): # Basic initialization
        super().__init__(parent)
        self.form = form

        self.create_widgets()

        self.grid(row=1, column = 0, columnspan = 2, rowspan = 1, sticky = "nsew")

    def create_widgets(self): # Create the widgets to later be drawn
        # The following selections change the header based on the encryption method being used
        if self.form == "Directional Caesar":
            self.level_label = customtkinter.CTkLabel(self, text = "Directional Caesar Encryption:", font = ("TkDefaultFont", 30, 'bold'))
        elif self.form == "Directional Polyshift":
            self.level_label = customtkinter.CTkLabel(self, text = "Directional Polyshift Encryption:", font = ("TkDefaultFont", 30, 'bold'))
        elif self.form == "Vernam":
            self.level_label = customtkinter.CTkLabel(self, text = "Vernam Cypher:", font = ("TkDefaultFont", 30, 'bold'))

        self.text_in_label = customtkinter.CTkLabel(self, text = "Plain Text In:", font = ("TkDefaultFont", 15))

        self.widget_text_in = customtkinter.CTkTextbox(self, wrap = "word")
        self.widget_text_in.bind('<KeyRelease>', self.input_change)

        self.key_frame = customtkinter.CTkFrame(self, fg_color = "transparent")
        self.key_frame.columnconfigure(0)
        self.key_frame.columnconfigure(1)
        self.key_frame.columnconfigure(3)

        self.key_label = customtkinter.CTkLabel(self.key_frame, text = "Key:", font = ("TkDefaultFont", 15))
        self.key_label.grid(row = 0, column = 0, columnspan = 1, sticky = "nse", padx = 5)

        self.key = StringVar()
        self.key.trace("w", lambda name, index, mode, key=self.key: self.input_change())

        self.widget_key_box = customtkinter.CTkEntry(self.key_frame, placeholder_text = "Key", font = ("TkDefaultFont", 20), width = 400, textvariable = self.key)
        self.widget_key_box.grid(row = 0, column = 1, padx = 5, sticky = "nsw")

        self.widget_graph_button = customtkinter.CTkButton(self.key_frame, text = "Frequency Analysis", command = self.show_frequency_graph, font = ("TkDefaultFont", 20))
        self.widget_graph_button.grid(row = 0, column = 2, padx = 5, sticky = "nsew")
        
        self.text_out_label = customtkinter.CTkLabel(self, text = "Encrypted Text Out:", font = ("TkDefaultFont", 15))
        self.widget_text_out = customtkinter.CTkTextbox(self, wrap = "word")
        self.widget_text_out.bind('<KeyRelease>', self.output_change)

        self.draw_widgets()

    def draw_widgets(self): # Draws the widgets and displays them on the window
        self.rowconfigure(0, weight = 1, minsize = 40)
        self.rowconfigure(1, weight = 1, minsize = 15)
        self.rowconfigure(2, weight = 100000, minsize = 40)
        self.rowconfigure(3, weight = 2, minsize = 20)
        self.rowconfigure(4, weight = 1, minsize = 15)
        self.rowconfigure(5, weight = 100000, minsize = 40)

        self.columnconfigure(0, weight = 1)

        self.level_label.grid(row = 0, column = 0, columnspan = 1, sticky = "nsw", padx = 10, pady = 10)
        self.text_in_label.grid(row = 1, column = 0, columnspan = 1, sticky = "nsw", padx = 10)
        self.widget_text_in.grid(row = 2, column = 0, columnspan = 1, sticky = "nsew", padx = 10)

        self.key_frame.grid(row = 3, column = 0, pady = 10)

        self.text_out_label.grid(row = 4, column = 0, columnspan = 1, sticky = "nsw", padx = 10)
        self.widget_text_out.grid(row = 5, column = 0, columnspan = 1, rowspan = 1, sticky = "nsew", padx = 10)

        self.configure(fg_color = "transparent")

    def input_change(self, value = None): # Is triggered when the input or key is changed to update the output box
        plain_text = self.widget_text_in.get(0.0, 'end')
        encryption_key = self.widget_key_box.get()

        encrypted_text = Encryption.decrypt(plain_text, encryption_key, self.form)

        self.widget_text_out.delete(0.0, 'end')
        self.widget_text_out.insert(0.0, encrypted_text)

    def output_change(self, value = None): # Is triggered when the output box is changed and updates the input box
        encrypted_text = self.widget_text_out.get(0.0, 'end')
        encryption_key = self.widget_key_box.get()

        plain_text = Encryption.decrypt(encrypted_text, encryption_key, self.form)

        self.widget_text_in.delete(0.0, 'end')
        self.widget_text_in.insert(0.0, plain_text)

    def get_graph_values(self, text):
        self.alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,<>/;:'@][-_=+1234567890!£4%^&*()]")
        values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        for char in text:
            try:
                char_index = self.alphabet.index(char)
                values[char_index] += 1
            except: pass # Triggered when item is not in the list (emoji, \n, etc.)

        return values
    
    def show_frequency_graph(self):
        encrypted_text = self.widget_text_out.get(0.0, 'end')
        letter_values = self.get_graph_values(encrypted_text)
        plt.figure(figsize = (15,5))
        plt.bar(self.alphabet, letter_values)
        

        plt.show()

class RSA_Page(customtkinter.CTkFrame): # TODO: add RSA encryption window and loading for when encrypting, generating keys, decrypting # TODO: split into three different classes, one for overall, and then one for each key frame
    def __init__(self, parent):
        super().__init__(parent)

        self.create_widgets()

        self.grid(row=1, column = 0, columnspan = 2, rowspan = 1, sticky = "nsew")

    def create_widgets(self):
        self.key_frame = customtkinter.CTkFrame(self)

        self.key_frame.rowconfigure((0,2), weight = 1)
        self.key_frame.rowconfigure((1,3), weight = 1000)
        self.key_frame.columnconfigure((0,1,2,3), weight = 1)

        self.key_generation_label = customtkinter.CTkLabel(self.key_frame, text = "Generate Keys:", font = ("TkDefaultFont", 30, "bold"))
        self.min_prime_label = customtkinter.CTkLabel(self.key_frame, text = "Minimum Prime:", font = ("TkDefaultFont", 15))
        self.min_prime_entry = customtkinter.CTkEntry(self.key_frame, placeholder_text = "3", font = ("TkDefaultFont", 15))

        self.max_prime_label = customtkinter.CTkLabel(self.key_frame, text = "Maximum Prime:", font = ("TkDefaultFont", 15))
        self.max_prime_entry = customtkinter.CTkEntry(self.key_frame, placeholder_text = "997", font = ("TkDefaultFont", 15))

        self.generate_key_button = customtkinter.CTkButton(self.key_frame, text = "Generate Key", font = ("TkDefaultFont", 15), command = self.generate_key)

        self.public_key_label = customtkinter.CTkLabel(self.key_frame, text = "Public Key: ", font = ("TkDefaultFont", 15))
        self.public_key_frame = customtkinter.CTkFrame(self.key_frame, fg_color = "transparent")
        self.public_key_frame.rowconfigure(0, weight = 1)
        self.public_key_frame.columnconfigure(0, weight = 1000)
        self.public_key_frame.columnconfigure(1, weight = 1)
        self.public_key_entry = customtkinter.CTkEntry(self.public_key_frame, placeholder_text = "Public Key", font = ("TkDefaultFont", 15), corner_radius = 0)
        self.public_key_copy_button = customtkinter.CTkButton(self.public_key_frame, text = "Copy", corner_radius = 0, font = ("TkDefaultFont", 15)) # TODO: add command

        self.n_label = customtkinter.CTkLabel(self.key_frame, text = "N: ", font = ("TkDefaultFont", 15))
        self.n_frame = customtkinter.CTkFrame(self.key_frame, fg_color = "transparent")
        self.n_frame.rowconfigure(0, weight = 1)
        self.n_frame.columnconfigure(0, weight = 1000)
        self.n_frame.columnconfigure(1, weight = 1)
        self.n_entry = customtkinter.CTkEntry(self.n_frame, placeholder_text = "N", font = ("TkDefaultFont", 15), corner_radius = 0)
        self.n_copy_button = customtkinter.CTkButton(self.n_frame, text = "Copy", corner_radius = 0, font = ("TkDefaultFont", 15)) # TODO: add command

        self.private_key_label = customtkinter.CTkLabel(self.key_frame, text = "Private Key: ", font = ("TkDefaultFont", 15))
        self.private_key_frame = customtkinter.CTkFrame(self.key_frame, fg_color = "transparent")
        self.private_key_frame.rowconfigure(0, weight = 1)
        self.private_key_frame.columnconfigure(0, weight = 1000)
        self.private_key_frame.columnconfigure(1, weight = 1)
        self.private_key_entry = customtkinter.CTkEntry(self.private_key_frame, placeholder_text = "Private Key", font = ("TkDefaultFont", 15), corner_radius = 0)
        self.private_key_copy_button = customtkinter.CTkButton(self.private_key_frame, text = "Copy", corner_radius = 0, font = ("TkDefaultFont", 15)) # TODO: add command

        self.encryption_frame = customtkinter.CTkFrame(self)

        self.draw_widgets()

    def draw_widgets(self):
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1000)
        self.columnconfigure(0, weight = 1)

        self.key_generation_label.grid(row = 0, column = 0, columnspan = 4, sticky = "nsw", padx = 10, pady = 5)

        self.min_prime_label.grid(row = 1, column = 0, columnspan = 1, sticky = "nsw", padx = 10, pady = 5)
        self.min_prime_entry.grid(row = 1, column = 1, columnspan = 1, sticky = "nsew", padx = 10, pady = 5)
        self.max_prime_label.grid(row = 2, column = 0, columnspan = 1, sticky = "nsw", padx = 10, pady = 5)
        self.max_prime_entry.grid(row = 2, column = 1, columnspan = 1, sticky = "nsew", padx = 10, pady = 5)

        self.generate_key_button.grid(row = 3, column = 0, columnspan = 2, sticky = "nsew", padx = 10, pady = 5)

        self.public_key_label.grid(row = 1, column = 2, columnspan = 1, sticky = "nsw", padx = 10, pady = 5)
        self.public_key_entry.grid(row = 0, column = 0, columnspan = 1, sticky = "nsew")
        self.public_key_copy_button.grid(row = 0, column = 1, columnspan = 1, sticky = "nsew")
        self.public_key_frame.grid(row = 1, column = 3, columnspan = 1, sticky = "nsew", padx = 10, pady = 5)

        self.n_label.grid(row = 2, column = 2, columnspan = 1, sticky = "nsw", padx = 10, pady = 5)
        self.n_entry.grid(row = 0, column = 0, columnspan = 1, sticky = "nsew")
        self.n_copy_button.grid(row = 0, column = 1, columnspan = 1, sticky = "nsew")
        self.n_frame.grid(row = 2, column = 3, columnspan = 1, sticky = "nsew", padx = 10, pady = 5)

        self.private_key_label.grid(row = 3, column = 2, columnspan = 1, sticky = "nsw", padx = 10, pady = 5)
        self.private_key_entry.grid(row = 0, column = 0, columnspan = 1, sticky = "nsew")
        self.private_key_copy_button.grid(row = 0, column = 1, columnspan = 1, sticky = "nsew")
        self.private_key_frame.grid(row = 3, column = 3, columnspan = 1, sticky = "nsew", padx = 10, pady = 5)

        self.key_frame.grid(row = 0, column = 0, columnspan = 1, padx = 10, pady = 10, sticky = "nsew")

    def generate_key(self):
        pass

class Notepad(customtkinter.CTkFrame):
    """
    This class houses the window for the notepad page of the app which saves and reads encrypted text from .txt files.
    Also housed within this class is the logic of opening, saving, and creating the .txt files.
    """
    def __init__(self, parent): # Basic initialization
        super().__init__(parent)

        self.file_path = ""

        self.create_widgets()

        self.grid(row=1, column = 0, columnspan = 2, rowspan = 1, sticky = "nsew")

    def create_widgets(self): # Creates the widgets which will later be drawn to the window
        self.widget_canvas = customtkinter.CTkTextbox(self, wrap = "word")
        self.widget_key_box = customtkinter.CTkEntry(self, placeholder_text = "Key", font = ("TkDefaultFont", 20), width = 400)
        self.widget_encryption_type = customtkinter.CTkOptionMenu(self, values = ["Directional Caesar", "Directional Polyshift", "Vernam"], font = ("TkDefaultFont", 20))
        self.widget_new_file_button = customtkinter.CTkButton(self, text = "New File", font = ("TkDefaultFont", 20), command = self.new_file)
        self.widget_open_file_button = customtkinter.CTkButton(self, text = "Open File", font = ("TkDefaultFont", 20), command = self.open_file)
        self.widget_save_file_button = customtkinter.CTkButton(self, text = "Save File", font = ("TkDefaultFont", 20), command = self.save_file)
        self.middle_filler = customtkinter.CTkLabel(self, text = "Key:", font = ("TkDefaultFont", 20))
        
        self.draw_widgets()

    def draw_widgets(self): # Draws the widgets to the window to be displayed on the screen.
        self.rowconfigure(0, weight = 1, minsize = 20)
        self.rowconfigure(1, weight = 10000)

        self.columnconfigure(0, weight = 1, minsize = 120)
        self.columnconfigure(1, weight = 1, minsize = 120)
        self.columnconfigure(2, weight = 1, minsize = 120)
        self.columnconfigure(3, weight = 1000000, minsize = 75)
        self.columnconfigure(4, weight = 1, minsize = 300)
        self.columnconfigure(5, weight = 1, minsize = 120)

        self.widget_canvas.grid(row = 1, column = 0, columnspan = 6, rowspan = 1, sticky = "nsew", padx = 10, pady = 10)
        self.widget_key_box.grid(row = 0, column = 4, sticky = "nsew")
        self.widget_encryption_type.grid(row = 0, column = 5, sticky = "nsew", padx = 10)
        self.widget_new_file_button.grid(row = 0, column = 0, sticky = "nsew", padx = 10)
        self.widget_open_file_button.grid(row = 0, column = 1, sticky = "nsew")
        self.widget_save_file_button.grid(row = 0, column = 2, sticky = "nsew", padx = 10)
        self.middle_filler.grid(row = 0, column = 3, sticky = "nse", padx = 10)

        self.configure(fg_color = "transparent")


    def new_file(self): # Triggered when the "New File" button in pressed in the notepad page, asks user for file location then creates new file
        file = filedialog.asksaveasfilename(initialdir = "C:\\", title = "Create Encrypted Text File", filetypes = (("Text File", "*.txt"), ))

        try:
            self.file_path = file + ".txt"
            file_rw = open(self.file_path, "w")
            file_rw.close()

            self.canvas.delete(0.0, 'end')
            self.key_box.delete()
        except: # Triggered when user closes file selection window without choosing
            self.file_path = ""

    def open_file(self): # Triggered when "Open" button is pressed in the notepad page, asks user for file location then moves on to asking for decryption key
        self.file_path = filedialog.askopenfilename(initialdir = "C:\\", title = "Create Encrypted Text File", filetypes = (("Text File", "*.txt"), ))
        file_rw = open(self.file_path, "r+")

        self.encrypted = file_rw.read()

        file_rw.close()

        self.key_request_box = OpenFileKeyRequest(self)

    def save_file(self): # Triggered when "Save" button is pressed, overwrites old data in file with new encrypted text.
        plain_text = self.widget_canvas.get(0.0, 'end')
        encryption_key = self.widget_key_box.get()
        encryption_type = self.widget_encryption_type.get()

        encrypted_text = Encryption.encrypt(plain_text, encryption_key, encryption_type)

        if self.file_path == "": # If file has not been created or opened --> will need to save new file location and make it
            self.file_path = filedialog.asksaveasfilename(initialdir = "C:\\", title = "Save As Encrypted Text File", filetypes = (("Text File", "*.txt"), ))

        if self.file_path != "": # Still necessary if user closes create file window before entering location and name
            file_rw = open(self.file_path, "w")
            file_rw.write(encrypted_text)
            file_rw.close()

class OpenFileKeyRequest(customtkinter.CTkToplevel):
    """
    Window used to ask the user for the encryption key when opening an encrypted text file.
    Triggered in "open_file" function of "Notepad" class.
    """
    def __init__(self, master): # Basic initialization
        super().__init__()

        self.master = master # Refers to master class (Notepad) so that data can be pushed into it

        self.title("Submit File Encryption Key:")
        self.minsize(300, 100)
        self.resizable(width = False, height = False)

        self.create_widgets()

        self.mainloop()

    def create_widgets(self): # Creates the basic widgets to later be drawn to the screen
        self.key_request_frame = customtkinter.CTkFrame(self, fg_color = "transparent")
        self.widget_key_request_box = customtkinter.CTkEntry(self.key_request_frame, placeholder_text = "Encryption Key")
        self.widget_encryption_type_select = customtkinter.CTkOptionMenu(self.key_request_frame, values = ["Directional Caesar", "Directional Polyshift", "Vernam"])
        self.widget_submit_key_button = customtkinter.CTkButton(self.key_request_frame, text = "Continue", command = self.open_file_submit_key)
        self.widget_submit_key_button.grid(pady = 10, row = 1, column = 0, columnspan = 2, sticky = "nesw")

        self.draw_widgets()

    def draw_widgets(self): # Draws the widgets already made to the screen
        self.key_request_frame.rowconfigure((0,1), weight = 1)

        self.key_request_frame.columnconfigure(0, weight = 3)
        self.key_request_frame.columnconfigure(1, weight = 1)

        self.widget_key_request_box.grid(row = 0, column = 0)
        self.widget_encryption_type_select.grid(row = 0, column = 1)
        self.widget_submit_key_button.grid(pady = 10, row = 1, column = 0, columnspan = 2, sticky = "nesw")

        self.key_request_frame.pack(padx = 10, pady = 10, anchor = "center", expand = True, fill = "both")

    def open_file_submit_key(self): # Triggered when "Continue" button is pressed, uses the specified key to decrypt the encrypted .txt file and push it into the canvas
        encryption_key = self.widget_key_request_box.get()
        encryption_type = self.widget_encryption_type_select.get()

        decrypted = Encryption.decrypt(self.master.encrypted, encryption_key, encryption_type)

        self.master.widget_canvas.delete(0.0, 'end')
        self.master.widget_canvas.insert(0.0, decrypted)

        self.master.widget_key_box.delete(0, 'end')
        self.master.widget_key_box.insert(0, encryption_key)

        self.master.widget_encryption_type.set(encryption_type)

        self.destroy()

class LearnMore(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__()

        self.title("Learn More")
        self.geometry('500x225')
        self.resizable(width = False, height = False)
        self.wm_transient(master)

        self.create_widgets()

        self.mainloop()

    def create_widgets(self):
        self.frame = customtkinter.CTkFrame(self)
        self.widget_info_label = customtkinter.CTkLabel(self.frame, text = "Symmetric encryption is the version of encryption in which the key to encrypt and decrypt is the same. In asymmetric encryption, the encryption and decryption key are different with users having public and private keys. The public key is used to encrypt the data but cannot be used to decrypt it. As such, the user will share their public key with the person who is sharing data with them and then use their own public key to decrypt it. This is secure because it does not matter if the public key is intercepted. The public key should not be shared at any point.", font = ("TkDefaultFont", 15), wraplength = 450)
        self.widget_close = customtkinter.CTkButton(self.frame, text = "Close", font = ("TkDefaultFont", 15), command = self.close)

        self.draw_widgets()

    def draw_widgets(self):
        self.frame.rowconfigure(0)
        self.frame.rowconfigure(1)

        self.frame.columnconfigure(0, weight = 1)

        self.widget_info_label.grid(row = 0, column = 0, pady = 5, sticky = "nsew")
        self.widget_close.grid(row = 1, column = 0, pady = 5, sticky = "nsew")

        self.frame.pack(padx = 10, pady = 5, anchor = "center", expand = True, fill = "both")

    def close(self):
        self.destroy()


customtkinter.set_appearance_mode("dark")

App()