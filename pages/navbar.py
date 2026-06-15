import tkinter as tk

from cfg import app_config as conf
from PIL import Image, ImageTk


class Navbar(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg=conf.BGTOPBARCOLOR, height=56)
        self.controller = controller
        self.pack_propagate(False)
        self._build()

    def _build(self) -> None:
        
        left_frame = tk.Frame(self, bg=conf.BGTOPBARCOLOR)
        left_frame.pack(side="left", padx="12")

        fav_button = self._nav_image_button(left_frame, conf.heart_icon_path, lambda: self.controller.show_frame("HomePage"))
        fav_button.pack(side="left", padx=4, pady=10)
        
        brand = tk.Label(
            left_frame,
            text="Game Launcher",
            bg=conf.BGTOPBARCOLOR,
            fg=conf.FGCOLOR,
            font=("TkDefaultFont", 12, "bold"),
        )
        brand.pack(side="left", padx=8)

        nav_buttons = tk.Frame(self, bg=conf.BGTOPBARCOLOR)
        nav_buttons.pack(side="right", padx=12)

        home_button = self._nav_button(nav_buttons, "Home", lambda: self.controller.show_frame("HomePage"))
        home_button.pack(side="left", padx=4, pady=10)

        quit_button = self._nav_button(nav_buttons, "Quit", self.controller.quit)
        quit_button.pack(side="left", padx=4, pady=10)

    def _nav_button(self, master, text, command):
        return tk.Button(
            master,
            text=text,
            command=command,
            bg=conf.HOVERCOLOR,
            fg=conf.FGCOLOR,
            activebackground=conf.FGSECONDARYCOLOR,
            activeforeground=conf.BGCOLOR,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            padx=14,
            pady=6,
            cursor="hand2",
        )

    def _nav_image_button(self, master, image_path, command):
        image = Image.open(image_path).resize((32, 32), resample=Image.Resampling.NEAREST)
        image_tk = ImageTk.PhotoImage(image)
        button = tk.Button(
            master,
            image=image_tk,
            command=command,
            bg=conf.BGTOPBARCOLOR,
            activebackground=conf.FGSECONDARYCOLOR,
            relief="flat",
            cursor="hand2",
            borderwidth=0,
            highlightthickness=0,
        )
        setattr(button, "_image", image_tk)  # Keep a reference to avoid garbage collection
        return button
