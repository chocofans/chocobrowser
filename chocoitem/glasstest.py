import tkinter as tk
from tkinter import ttk

class DraggableWindow:
    def __init__(self, root):
        self.root = root
        self.x = 0
        self.y = 0
        self.titlebar_frame = None

        self.create_titlebar()
        self.bind_events()

    def create_titlebar(self):
        self.titlebar_frame = ttk.Frame(self.root, style="Titlebar.TFrame")
        self.titlebar_frame.pack(side="top", fill="x")

        title_label = ttk.Label(self.titlebar_frame, text="Glass Titlebar Example", style="Title.TLabel")
        title_label.pack(side="left", padx=10, pady=5)

        close_button = ttk.Button(self.titlebar_frame, text="Close", command=self.root.destroy)
        close_button.pack(side="right", padx=10, pady=5)

    def bind_events(self):
        self.titlebar_frame.bind("<ButtonPress-1>", self.start_move)
        self.titlebar_frame.bind("<B1-Motion>", self.on_drag)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

def main():
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry("400x300")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Titlebar.TFrame", background="#B3FFFFFF", borderwidth=0)

    draggable_window = DraggableWindow(root)

    root.attributes('-transparentcolor', 'white')
    root.attributes('-alpha', 0.9)

    root.mainloop()

if __name__ == "__main__":
    main()
