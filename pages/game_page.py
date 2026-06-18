import tkinter as tk
import os
import shutil
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

from cfg import app_config as conf
from pages.game import Game

POPUP_SIZE = (200, 300)


class GamePage(tk.Toplevel):
    def __init__(self, parent, on_save=None, game=None):
        super().__init__(parent)
        self.on_save = on_save
        self._preview_image = None
        self._selected_image_path = conf.SAMPLE_GRID_IMAGE_PATH
        self._selected_game_path = ""

        self.game = game
        self.existing_game = game is not None

        self.title("Edit Game" if self.existing_game else "Add Game")

        self.configure(bg=conf.BGCOLOR)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self._build_ui()

        if self.existing_game:
            assert self.game is not None
            self.name_var.set(self.game.name)
            self._selected_image_path = self.game.image_path
            self._selected_game_path = self.game.path
            self.path_display.configure(text=self._selected_game_path)
            self._refresh_preview()

        self._center_window()

    def _build_ui(self):
        """ Builds the UI for the game page, including the form for adding/editing a game."""
        container = tk.Frame(self, bg=conf.BGCOLOR, padx=20, pady=20)
        container.pack(fill="both", expand=True)

        header = tk.Label(
            container,
            text="Add a New Game" if not self.existing_game else "Edit Game",
            bg=conf.BGCOLOR,
            fg=conf.FGCOLOR,
            font=("TkDefaultFont", 14, "bold"),
        )
        header.pack(anchor="w", pady=(0, 14))

        content = tk.Frame(container, bg=conf.BGCOLOR)
        content.pack(fill="both", expand=True)

        preview_frame = tk.Frame(content, bg=conf.BGTOPBARCOLOR, padx=10, pady=10)
        preview_frame.pack(side="left", padx=(0, 18))

        self.preview_button = tk.Button(
            preview_frame,
            command=self._choose_image,
            bg=conf.HOVERCOLOR,
            activebackground=conf.FGSECONDARYCOLOR,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
        )
        self.preview_button.pack()
        self._refresh_preview()

        preview_hint = tk.Label(
            preview_frame,
            text="Click image to add",
            bg=conf.BGTOPBARCOLOR,
            fg=conf.FGSECONDARYCOLOR,
        )
        preview_hint.pack(pady=(8, 0))

        form = tk.Frame(content, bg=conf.BGCOLOR)
        form.pack(side="left", fill="both", expand=True)

        name_label = tk.Label(form, text="Name", bg=conf.BGCOLOR, fg=conf.FGCOLOR)
        name_label.pack(anchor="w")
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(form, textvariable=self.name_var)
        name_entry.pack(fill="x", pady=(4, 12))

        path_label = tk.Label(form, text="Game Path", bg=conf.BGCOLOR, fg=conf.FGCOLOR)
        path_label.pack(anchor="w")

        path_row = tk.Frame(form, bg=conf.BGCOLOR)
        path_row.pack(fill="x", pady=(4, 12))

        self.path_display = tk.Label(
            path_row,
            text="No path selected",
            bg=conf.BGCOLOR,
            fg=conf.FGSECONDARYCOLOR,
            anchor="w",
        )
        self.path_display.pack(side="left", fill="x", expand=True)

        path_button = tk.Button(
            path_row,
            text="Add Path",
            command=self._choose_path,
            bg=conf.HOVERCOLOR,
            fg=conf.FGCOLOR,
            activebackground=conf.FGSECONDARYCOLOR,
            activeforeground=conf.BGCOLOR,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            padx=12,
            pady=4,
        )
        path_button.pack(side="right", padx=(10, 0))

        type_label = tk.Label(form, text="Game Type", bg=conf.BGCOLOR, fg=conf.FGCOLOR)
        type_label.pack(anchor="w")

        self.type_var = tk.StringVar(value="Steam")
        type_dropdown = ttk.Combobox(
            form,
            textvariable=self.type_var,
            state="readonly",
            values=("Steam", "Exe", "Other"),
        )
        type_dropdown.pack(fill="x", pady=(4, 0))

        actions = tk.Frame(container, bg=conf.BGCOLOR)
        actions.pack(fill="x", pady=(18, 0))

        cancel_button = tk.Button(
            actions,
            text="Cancel",
            command=self.destroy,
            bg=conf.HOVERCOLOR,
            fg=conf.FGCOLOR,
            activebackground=conf.FGSECONDARYCOLOR,
            activeforeground=conf.BGCOLOR,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            padx=14,
            pady=6,
        )
        cancel_button.pack(side="right", padx=(8, 0))

        save_button = tk.Button(
            actions,
            text="Save",
            command=self._save,
            bg=conf.HOVERCOLOR,
            fg=conf.FGCOLOR,
            activebackground=conf.FGSECONDARYCOLOR,
            activeforeground=conf.BGCOLOR,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            padx=14,
            pady=6,
        )
        save_button.pack(side="right")

    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        parent = self.master
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{max(0, x)}+{max(0, y)}")

    def _refresh_preview(self):
        image = Image.open(self._selected_image_path).resize(POPUP_SIZE, resample=Image.Resampling.LANCZOS)
        self._preview_image = ImageTk.PhotoImage(image)
        self.preview_button.configure(image=self._preview_image)

    def _choose_image(self):
        selected_path = filedialog.askopenfilename(
            parent=self,
            title="Select Game Image",
            filetypes=(("Image files", "*.png *.jpg *.jpeg *.gif *.webp"), ("All files", "*.*")),
        )
        if not selected_path:
            return

        self._selected_image_path = selected_path
        self._refresh_preview()

    def _choose_path(self):
        selected_path = filedialog.askopenfilename(
            parent=self,
            title="Select Game Path",
            filetypes=(("All files", "*.*"),),
        )
        if not selected_path:
            return

        self._selected_game_path = selected_path
        self.path_display.configure(text=selected_path)

    def _copy_image_to_assets(self, source_path):
        if not os.path.exists(conf.GAME_IMAGES_PATH):
            os.makedirs(conf.GAME_IMAGES_PATH, exist_ok=True)

        dest_path = os.path.join(conf.GAME_IMAGES_PATH, os.path.basename(source_path))
        if os.path.abspath(source_path) != os.path.abspath(dest_path):
            shutil.copy(source_path, dest_path)
        return dest_path

    def _save(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing name", "Please enter a game name.", parent=self)
            return

        if not self._selected_game_path:
            messagebox.showwarning("Missing path", "Please select a game path.", parent=self)
            return

        game_type = {"Steam": 0, "Exe": 1, "Other": 2}.get(self.type_var.get(), 2)
        self._selected_image_path = self._copy_image_to_assets(self._selected_image_path)
        game = Game(name, self._selected_game_path, self._selected_image_path, game_type)

        if self.on_save:
            self.on_save(game, self.game)

        self.destroy()
