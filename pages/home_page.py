import tkinter as tk
from PIL import Image, ImageTk

from cfg import app_config as conf
from pages.game import Game

BASE_SEPARATION_CARDS = (4, 10)

CARD_SIZE = (200, 300)

class HomePage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg=conf.BGCOLOR)
        self.controller = controller
        self._images = []
        self._games = []
        self._grid = None
        self._grid_window = None
        self._scrollable_canvas = None
        self._current_columns = 0
        self._layout_width = 0
        self._column_breakpoint = CARD_SIZE[0] + BASE_SEPARATION_CARDS[0] * 2
        self.create_widgets()

    @staticmethod
    def update_scrollregion(canvas, _event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
    
    @staticmethod
    def on_mousewheel(canvas, event):
        event_num = getattr(event, "num", None)
        delta = getattr(event, "delta", 0)

        if event_num == 4 or delta > 0:
            canvas.yview_scroll(-1, "units")
        elif event_num == 5 or delta < 0:
            canvas.yview_scroll(1, "units")

    def match_canvas_width(self, canvas, event):
        if self._grid_window is not None:
            canvas.itemconfigure(self._grid_window, width=event.width)
        columns = max(1, event.width // self._column_breakpoint)
        if self._games and self._grid is not None and (columns != self._current_columns or event.width != self._layout_width or not self._grid.winfo_children()):
            self._render_grid(columns)



    def create_widgets(self):
        container = tk.Frame(self, bg=conf.BGCOLOR, padx=28, pady=24)
        container.pack(fill="both", expand=True)

        toptainer = tk.Frame(container, bg=conf.BGCOLOR)
        toptainer.pack(fill="x", pady=(0, 12), anchor="w")

        titleiner = tk.Frame(toptainer, bg=conf.BGCOLOR)
        titleiner.pack(side="left", anchor="w")

        title = tk.Label(
            titleiner,
            text="Game Library",
            bg=conf.BGCOLOR,
            fg=conf.FGCOLOR,
            font=("TkDefaultFont", 13, "bold"),
        )
        title.pack(anchor="w", pady=(0, 2))

        subtitle = tk.Label(
            titleiner,
            text="Pick a game, open it, or edit the entry",
            bg=conf.BGCOLOR,
            fg=conf.FGSECONDARYCOLOR,
        )
        subtitle.pack(anchor="w", pady=(2, 0))
        
        add_image = Image.open(conf.add_icon_path).resize((32, 32), resample=Image.Resampling.NEAREST)
        add_image_tk = ImageTk.PhotoImage(add_image)

        add_game_button = tk.Button(
            toptainer,
            image=add_image_tk,
            command="",
            bg=conf.BGTOPBARCOLOR,
            activebackground=conf.FGSECONDARYCOLOR,
            relief="flat",
            cursor="hand2",
            borderwidth=0,
            highlightthickness=0,
        )
        self._images.append(add_image_tk)
        add_game_button.pack(side="right", padx=4, pady=10)

        scroll_area = tk.Frame(container, bg=conf.BGCOLOR)
        scroll_area.pack(fill="both", expand=True)

        canvas = tk.Canvas(scroll_area, bg=conf.BGCOLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_area, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._grid = tk.Frame(canvas, bg=conf.BGCOLOR)
        self._grid_window = canvas.create_window((0, 0), window=self._grid, anchor="nw")
        self._scrollable_canvas = canvas

        self._grid.bind("<Configure>", lambda e: self.update_scrollregion(self._scrollable_canvas, e))
        self._scrollable_canvas.bind("<Configure>", lambda e: self.match_canvas_width(self._scrollable_canvas, e))
        self._scrollable_canvas.bind_all("<MouseWheel>", lambda e: self.on_mousewheel(self._scrollable_canvas, e))
        self._scrollable_canvas.bind_all("<Button-4>", lambda e: self.on_mousewheel(self._scrollable_canvas, e))
        self._scrollable_canvas.bind_all("<Button-5>", lambda e: self.on_mousewheel(self._scrollable_canvas, e))

        self._games = [
            Game("Adventure Quest", "", conf.sample_grid_image_path),
            Game("Space Runner", "", conf.sample_grid_image_path),
            Game("Pixel Farm", "", conf.sample_grid_image_path),
            Game("Boss Raid", "", conf.sample_grid_image_path),
            Game("Sky Drift", "", conf.sample_grid_image_path),
            Game("Night Forge", "", conf.sample_grid_image_path),
        ]

        self._render_grid(3)

    def _render_grid(self, columns):
        if not self._grid:
            return

        columns = max(1, min(columns, len(self._games)))

        self._current_columns = columns
        base_padx = BASE_SEPARATION_CARDS[0]
        if self._scrollable_canvas is not None:
            canvas_width = max(0, self._scrollable_canvas.winfo_width())
            if canvas_width > 1:
                extra_space = max(0, canvas_width - (columns * CARD_SIZE[0]))
                base_padx = max(base_padx, extra_space // (2 * columns))

        cell_width = CARD_SIZE[0] + (base_padx * 2)
        self._layout_width = columns * cell_width

        for child in self._grid.winfo_children():
            child.destroy()

        for index, game in enumerate(self._games):
            row = index // columns
            column = index % columns
            card = self._build_game_card(self._grid, game)
            card.grid(row=row, column=column, padx=base_padx, pady=BASE_SEPARATION_CARDS[1], sticky="n")

        for column in range(columns):
            self._grid.grid_columnconfigure(column, weight=0, minsize=cell_width)

    def _build_game_card(self, master, game):
        card = tk.Frame(
            master,
            bg=conf.BGTOPBARCOLOR,
            width=CARD_SIZE[0],
            height=CARD_SIZE[1],
        )
        card.pack_propagate(False)
        card.grid_propagate(False)

        image_button = self._make_image_button(card, game.image_path, lambda: self.open_game(game))
        image_button.pack(fill="both", expand=True)

        return card

    def _make_image_button(self, master, image_path, command):
        image = Image.open(image_path).resize(CARD_SIZE, resample=Image.Resampling.LANCZOS)
        image_tk = ImageTk.PhotoImage(image)
        self._images.append(image_tk)

        button = tk.Button(
            master,
            image=image_tk,
            command=command,
            bg=conf.HOVERCOLOR,
            activebackground=conf.FGSECONDARYCOLOR,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
        )
        return button

    def start_game(self):
        print("Game started!")

    def open_library(self):
        print("Opening game library...")

    def open_game(self, game):
        print(f"Opening {game.name} from {game.path}...")