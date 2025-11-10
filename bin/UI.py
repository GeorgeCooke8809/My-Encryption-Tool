import customtkinter
from tkinter import filedialog
from tkinter import *
import Encryption

def func_open_file(widget_canvas, widget_key_box, widget_encryption_type): # Open file button in notepad page
    global file_path

    file_path = filedialog.askopenfilename(initialdir = "C:\\", title = "Create Encrypted Text File", filetypes = (("Text File", "*.txt"), ))
    file_rw = open(file_path, "r+")

    encrypted = file_rw.read()

    file_rw.close()

    key_request_root = customtkinter.CTk()

    key_request_root.title("Submit File Encryption Key:")
    key_request_root.minsize(300, 100)
    key_request_root.resizable(width = False, height = False)

    key_request_frame = customtkinter.CTkFrame(key_request_root, fg_color = "transparent")

    key_request_frame.rowconfigure(0, weight = 1)
    key_request_frame.rowconfigure(1, weight = 1)

    key_request_frame.columnconfigure(0, weight = 3)
    key_request_frame.columnconfigure(1, weight = 1)

    widget_key_request_box = customtkinter.CTkEntry(key_request_frame, placeholder_text = "Encryption Key")
    widget_key_request_box.grid(row = 0, column = 0)

    widget_encryption_type_select = customtkinter.CTkOptionMenu(key_request_frame, values = ["Lvl. 1", "Lvl. 2"])
    widget_encryption_type_select.grid(row = 0, column = 1)

    widget_submit_key_button = customtkinter.CTkButton(key_request_frame, text = "Continue", command = lambda: func_continue_open(widget_key_request_box, widget_encryption_type_select, encrypted, widget_canvas, widget_key_box, key_request_root, widget_encryption_type))
    widget_submit_key_button.grid(pady = 10, row = 1, column = 0, columnspan = 2, sticky = "nesw")

    key_request_frame.pack(padx = 10, pady = 10, anchor = "center", expand = True, fill = "both")
    key_request_root.mainloop()

def func_continue_open(widget_key_request_box, widget_encryption_type_select, encrypted_text, widget_canvas, widget_key_box, key_request_root, widget_encryption_type): # Submit button in open file get key page - Triggered on button press
    encryption_key = widget_key_request_box.get()
    encryption_type = widget_encryption_type_select.get()

    decrypted = Encryption.decrypt(encrypted_text, encryption_key, encryption_type)

    widget_canvas.delete(0.0, 'end')
    widget_canvas.insert(0.0, decrypted)

    widget_key_box.delete(0, 'end')
    widget_key_box.insert(0, encryption_key)

    widget_encryption_type.set(encryption_type)

    key_request_root.withdraw()
    key_request_root.quit()

def func_save_file(widget_canvas, widget_key_box, widget_encryption_type): # Save file button in notepad page
    global file_path

    plain_text = widget_canvas.get(0.0, 'end')
    encryption_key = widget_key_box.get()
    encryption_type = widget_encryption_type.get()

    encrypted_text = Encryption.encrypt(plain_text, encryption_key, encryption_type)

    if file_path == "": # If file has ! been created or opened --> will need to save new file location and make it
        file_path = filedialog.asksaveasfilename(initialdir = "C:\\", title = "Save As Encrypted Text File", filetypes = (("Text File", "*.txt"), ))

    if file_path != "":
        file_rw = open(file_path, "w")
        file_rw.write(encrypted_text)
        file_rw.close()   

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x600")
        self.minsize(width = 900, height = 350)
        self.title("OOP Encryptor - By George A.C. Cooke")

        self.master_frame = MasterFrame(self)

        self.mainloop()

class MasterFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_widgets()

        self.pack(anchor = "center", expand = True, fill = "both")

    def create_widgets(self):
        self.widget_menu_buttons = customtkinter.CTkSegmentedButton(self, values = ["Lvl. 1", "Lvl. 2", "Lvl. 3", "Notepad"], command  = self.switch_page, font = ("TkDefaultFont", 20))
        self.widget_menu_buttons.set("Lvl. 1")

        self.content = Basic(self, "Lvl. 1")

        self.draw_widgets()

    def draw_widgets(self):
        self.rowconfigure(0, weight = 1, minsize = 20)
        self.rowconfigure(1, weight = 100000, minsize = 80)
        self.columnconfigure(0, weight = 9)
        self.columnconfigure(1, weight = 1)

        self.widget_menu_buttons.grid(row = 0, column = 0, sticky = "nsw", padx = 10, pady = 10)
        self.content.grid(row=1, column = 0, columnspan = 2, rowspan = 1, sticky = "nsew")

    def switch_page(self, value = None):
        page = self.widget_menu_buttons.get()
        self.content.destroy()

        if page in ["Lvl. 1", "Lvl. 2"]:
            self.content = Basic(self, page)
        elif page == "Notepad":
            self.content = Notepad(self)

class Basic(customtkinter.CTkFrame):
    def __init__(self, parent, form):
        super().__init__(parent)
        self.form = form

        self.create_widgets()

        self.grid(row=1, column = 0, columnspan = 2, rowspan = 1, sticky = "nsew")

    def create_widgets(self):
        if self.form == "Lvl. 1":
            self.level_label = customtkinter.CTkLabel(self, text = "Level 1 Encryption - Caesar:", font = ("TkDefaultFont", 30, 'bold'))
        elif self.form == "Lvl. 2":
            self.level_label = customtkinter.CTkLabel(self, text = "Level 2 Encryption - Directional Polyshift:", font = ("TkDefaultFont", 30, 'bold'))

        self.text_in_label = customtkinter.CTkLabel(self, text = "Plain Text In:", font = ("TkDefaultFont", 15))

        self.widget_text_in = customtkinter.CTkTextbox(self, wrap = "word")
        self.widget_text_in.bind('<KeyRelease>', self.input_change)

        self.key_frame = customtkinter.CTkFrame(self, fg_color = "transparent")
        self.key_frame.columnconfigure(0)
        self.key_frame.columnconfigure(1)

        self.key_label = customtkinter.CTkLabel(self.key_frame, text = "Key:", font = ("TkDefaultFont", 15))
        self.key_label.grid(row = 0, column = 0, columnspan = 1, sticky = "nse", padx = 5)

        self.key = StringVar()
        self.key.trace("w", lambda name, index, mode, key=self.key: self.input_change())

        self.widget_key_box = customtkinter.CTkEntry(self.key_frame, placeholder_text = "Key", font = ("TkDefaultFont", 20), width = 400, textvariable = self.key)
        self.widget_key_box.grid(row = 0, column = 1, padx = 5, sticky = "nsw")

        
        self.text_out_label = customtkinter.CTkLabel(self, text = "Encrypted Text Out:", font = ("TkDefaultFont", 15))
        self.widget_text_out = customtkinter.CTkTextbox(self, wrap = "word")
        self.widget_text_out.bind('<KeyRelease>', self.output_change)

        self.draw_widgets()

    def draw_widgets(self):
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

    def input_change(self, value = None):
        plain_text = self.widget_text_in.get(0.0, 'end')
        encryption_key = self.widget_key_box.get()

        if self.form == "Lvl. 1":
            encrypted_text = Encryption.decrypt(plain_text, encryption_key, "Lvl. 1")
        elif self.form == "Lvl. 2":
            encrypted_text = Encryption.decrypt(plain_text, encryption_key, "Lvl. 2")

        self.widget_text_out.delete(0.0, 'end')
        self.widget_text_out.insert(0.0, encrypted_text)

    def output_change(self, value = None):
        encrypted_text = self.widget_text_out.get(0.0, 'end')
        encryption_key = self.widget_key_box.get()

        if self.form == "Lvl. 1":
            plain_text = Encryption.decrypt(encrypted_text, encryption_key, "Lvl. 1")
        elif self.form == "Lvl. 2":
            plain_text = Encryption.decrypt(encrypted_text, encryption_key, "Lvl. 2")

        self.widget_text_in.delete(0.0, 'end')
        self.widget_text_in.insert(0.0, plain_text)

class Notepad(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.file_path = ""

        self.create_widgets()

        self.grid(row=1, column = 0, columnspan = 2, rowspan = 1, sticky = "nsew")

    def create_widgets(self):
        self.canvas = customtkinter.CTkTextbox(self, wrap = "word")
        self.widget_key_box = customtkinter.CTkEntry(self, placeholder_text = "Key", font = ("TkDefaultFont", 20), width = 400)
        self.widget_encryption_type = customtkinter.CTkOptionMenu(self, values = ["Lvl. 1", "Lvl. 2"], font = ("TkDefaultFont", 20))
        self.widget_new_file_button = customtkinter.CTkButton(self, text = "New File", font = ("TkDefaultFont", 20), command = self.new_file)
        self.widget_open_file_button = customtkinter.CTkButton(self, text = "Open File", font = ("TkDefaultFont", 20), command = self.open_file)
        self.widget_save_file_button = customtkinter.CTkButton(self, text = "Save File", font = ("TkDefaultFont", 20), command = self.save_file)
        self.middle_filler = customtkinter.CTkLabel(self, text = "Key:", font = ("TkDefaultFont", 20))
        
        self.draw_widgets()

    def draw_widgets(self):
        self.rowconfigure(0, weight = 1, minsize = 20)
        self.rowconfigure(1, weight = 10000)

        self.columnconfigure(0, weight = 1, minsize = 120)
        self.columnconfigure(1, weight = 1, minsize = 120)
        self.columnconfigure(2, weight = 1, minsize = 120)
        self.columnconfigure(3, weight = 1000000, minsize = 75)
        self.columnconfigure(4, weight = 1, minsize = 300)
        self.columnconfigure(5, weight = 1, minsize = 120)

        self.canvas.grid(row = 1, column = 0, columnspan = 6, rowspan = 1, sticky = "nsew", padx = 10, pady = 10)
        self.widget_key_box.grid(row = 0, column = 4, sticky = "nsew")
        self.widget_encryption_type.grid(row = 0, column = 5, sticky = "nsew", padx = 10)
        self.widget_new_file_button.grid(row = 0, column = 0, sticky = "nsew", padx = 10)
        self.widget_open_file_button.grid(row = 0, column = 1, sticky = "nsew")
        self.widget_save_file_button.grid(row = 0, column = 2, sticky = "nsew", padx = 10)
        self.middle_filler.grid(row = 0, column = 3, sticky = "nse", padx = 10)

        self.configure(fg_color = "transparent")


    def new_file(self): # TODO: Implement this
        file = filedialog.asksaveasfilename(initialdir = "C:\\", title = "Create Encrypted Text File", filetypes = (("Text File", "*.txt"), ))

        try:
            self.file_path = file + ".txt"
            file_rw = open(file_path, "w")
            file_rw.close()

            self.canvas.delete(0.0, 'end')
            self.key_box.delete()
        except:
            self.file_path = ""

    def open_file(self): # TODO: Implement this
        pass

    def save_file(self): # TODO: Implement this
        pass


customtkinter.set_appearance_mode("dark")

App()