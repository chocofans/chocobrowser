import requests
import os
import sys
import subprocess
import win32gui
import win32con

required_modules = ['faker', 'tkinter', 'datetime', 'requests', 'subprocess', 'pillow', 'beautifulsoup4']

for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"{module} ChocoModule not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            print(f"{module} successfully installed.")
        except subprocess.CalledProcessError:
            print(f"Error installing {module}. Please install it manually. ``pip install <module_name>``")
            sys.exit(1)

import tkinter as tk
from tkinter import ttk, Label, Button, Frame
from tkinter import Canvas
from datetime import datetime
import requests
from faker import Faker
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
from chocores.chocoengine import HTMLDocument

current_dir = os.path.dirname(os.path.realpath(__file__))
customtk_dir = os.path.join(current_dir, "CustomTkinter")
sys.path.append(customtk_dir)

try:
    import customtkinter as customtk
except ImportError:
    print("customtkinter module not found. Please make sure it is installed. ``git clone https://github.com/TomSchimansky/CustomTkinter``")
    sys.exit(1)
#pip darkdetect into launcher

try:
    import darkdetect
except ImportError:
    print("darkdetect module not found. Installing...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "darkdetect"])
        print("darkdetect successfully installed.")
    except subprocess.CalledProcessError:
        print("Error installing darkdetect. Please install it manually. ``pip install darkdetect``")
        sys.exit(1)

import darkdetect

class ChocoBrowserTab:
    def __init__(self, master, tab_name, notebook):
        self.tab = ttk.Frame(master)
        self.tab_name = tab_name
        self.notebook = notebook
        self.url_history = []
        self.current_index = -1  
        self.create_widgets()

    def create_widgets(self):
        url_frame = customtk.CTkFrame(self.tab)
        url_frame.pack(side=tk.TOP, fill=tk.X)

        image_path = os.path.join(os.path.dirname(__file__), "chocoitem", "bg.png")
        entry_bg_image = tk.PhotoImage(file=image_path)

        self.back_button = customtk.CTkButton(url_frame, text="Back", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.forward_button = customtk.CTkButton(url_frame, text="Forward", command=self.go_forward)
        self.forward_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.entry = customtk.CTkEntry(url_frame, width=690)
        self.entry.pack(side=tk.LEFT, padx=5, pady=10)

        self.go_button = customtk.CTkButton(url_frame, text="Go", command=self.open_url)
        self.go_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.text_area = customtk.CTkTextbox(self.tab, wrap=tk.WORD, height=20, width=80)
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def open_url(self):
        url = self.entry.get()
        if url.strip() != "":
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url
            try:
                fake = Faker()
                ip_address = fake.ipv4_public()

                headers = {'X-Forwarded-For': ip_address}

                response = requests.get(url, headers=headers)
                content = response.text

                self.text_area.delete(1.0, tk.END)

                self.text_area.insert(tk.END, content)

                if 'text/html' in response.headers['Content-Type']:
                    html_doc = HTMLDocument(url, content)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to open ChocoURL: {e}")

    def go_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.url_history[self.current_index])
            self.open_url()

    def go_forward(self):
        if self.current_index < len(self.url_history) - 1:
           self.current_index += 1
           self.entry.delete(0, tk.END)
           self.entry.insert(0, self.url_history[self.current_index])
           self.open_url()

def add_tab(notebook):
    tab_name = f"ChocoTab {notebook.index('end') + 1}"
    browser_tab = ChocoBrowserTab(notebook, tab_name, notebook)
    notebook.add(browser_tab.tab, text=tab_name)

def remove_tab(notebook):
    current_tab = notebook.select()
    notebook.forget(current_tab)\
    
def main():
    root = tk.Tk() 
#  root.overrideredirect(True)  (DEFUNT TO HIDE MAIN TITLEBARR)

    build_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    root.title(f"ChocoBrowser 0.87_AutoBuild_PY_WINDOWSAUTOBUILD_OSCEREGRESS_Encrypt_DEVWINRELEASE_{build_time}")
    
    chocoico_path = os.path.join(os.path.dirname(__file__), "chocoitem", "chocoico.ico")
    root.iconbitmap(chocoico_path)
    
    root.geometry("1024x768")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    for i in range(3):
        add_tab(notebook)

    add_tab_button = tk.Button(root, text="Add Tab", command=lambda: add_tab(notebook))
    add_tab_button.pack(side=tk.LEFT)

    remove_tab_button = tk.Button(root, text="Remove Tab", command=lambda: remove_tab(notebook))
    remove_tab_button.pack(side=tk.LEFT)

    root.mainloop()

if __name__ == "__main__":
    main()