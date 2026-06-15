import tkinter as tk

from cfg import app_config as conf

class HomePage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg=conf.BGCOLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        card = tk.Frame(self, bg=conf.BGTOPBARCOLOR, padx=24, pady=24)
        card.place(relx=0.5, rely=0.5, anchor="center")

        self.label = tk.Label(
            card,
            text="Welcome to the Game Launcher!",
            bg=conf.BGTOPBARCOLOR,
            fg=conf.FGCOLOR,
            font=("TkDefaultFont", 16, "bold"),
        )
        self.label.pack(pady=(0, 12))

        self.subtitle = tk.Label(
            card,
            text="Choose an action below",
            bg=conf.BGTOPBARCOLOR,
            fg=conf.FGSECONDARYCOLOR,
        )
        self.subtitle.pack(pady=(0, 16))

        button_row = tk.Frame(card, bg=conf.BGTOPBARCOLOR)
        button_row.pack()

        self.start_button = tk.Button(
            button_row,
            text="Start Game",
            command=self.start_game,
            bg=conf.HOVERCOLOR,
            fg=conf.FGCOLOR,
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
        )
        self.start_button.pack(side="left", padx=6)

        self.library_button = tk.Button(
            button_row,
            text="Game Library",
            command=self.open_library,
            bg=conf.HOVERCOLOR,
            fg=conf.FGCOLOR,
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
        )
        self.library_button.pack(side="left", padx=6)

        self.quit_button = tk.Button(
            button_row,
            text="Quit",
            command=self.controller.quit,
            bg=conf.HOVERCOLOR,
            fg=conf.FGCOLOR,
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
        )
        self.quit_button.pack(side="left", padx=6)

    def start_game(self):
        print("Game started!")

    def open_library(self):
        print("Opening game library...")