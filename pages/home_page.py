import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageEnhance

from cfg import app_config as conf
from pages.game_page import GamePage
from pages.game import Game
from utils.games_ddbb import GamesDDBB


BASE_SEPARATION_CARDS = (4, 10)

CARD_SIZE = (200, 300)

class Games:
    def __init__(self):
        self.manager = GamesDDBB()

    def add_game(self, game):
        self.manager.add_game(game)

    def remove_game(self, game):
        self.manager.remove_game(game)

    def modify_game(self, old_game, new_game):
        self.manager.modify_game(old_game, new_game)

    def get_games(self):
        return self.manager.get_games()

class HomePage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg=conf.BGCOLOR)

        self.game_manager = Games()

        self.controller = controller
        self._images = []
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
        
        add_image = Image.open(conf.ADD_ICON_PATH).resize((32, 32), resample=Image.Resampling.NEAREST)
        add_image_tk = ImageTk.PhotoImage(add_image)

        add_game_button = tk.Button(
            toptainer,
            image=add_image_tk,
            command=self.open_add_game_page,
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

        self._games = self.game_manager.get_games()

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

        image_button = self._make_image_button(card, game.image_path, lambda: self.open_game(game), game.name)
        image_button.pack(fill="both", expand=True)

        menu = tk.Menu(
            card,
            tearoff=0,
            bg=conf.BGTOPBARCOLOR,
            fg=conf.FGCOLOR,
            activebackground=conf.HOVERCOLOR,
            activeforeground=conf.FGCOLOR,
        )
        menu.add_command(label="Open", command=lambda: self.open_game(game))
        menu.add_command(label="Edit", command=lambda: self.open_edit_game_page(game))
        menu.add_command(label="Remove", command=lambda: self.remove_game(game))

        def show_menu(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        for widget in (card, image_button):
            widget.bind("<Button-3>", show_menu)

        return card

    def _make_image_button(self, master, image_path, command, title):
        image = Image.open(image_path).resize(CARD_SIZE, resample=Image.Resampling.LANCZOS)
        image_tk = ImageTk.PhotoImage(image)
        hover_image_tk = self._build_hover_image(image, title)

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

        image_state = {"normal": image_tk, "hover": hover_image_tk}

        def show_hover(_event, widget=button):
            widget.configure(image=image_state["hover"])

        def show_normal(_event, widget=button):
            widget.configure(image=image_state["normal"])

        button.bind("<Enter>", show_hover)
        button.bind("<Leave>", show_normal)

        return button

    def _build_hover_image(self, image, title):
        hover_base = ImageEnhance.Brightness(image).enhance(0.45).convert("RGBA")
        overlay = Image.new("RGBA", CARD_SIZE, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        font = ImageFont.load_default(25)

        text = title.strip() or "Game"
        max_chars = 18
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            candidate = word if not current_line else f"{current_line} {word}"
            if len(candidate) <= max_chars:
                current_line = candidate
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        wrapped_text = "\n".join(lines[:3])
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, spacing=4, align="center")
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (CARD_SIZE[0] - text_width) // 2
        text_y = (CARD_SIZE[1] - text_height) // 2

        draw.multiline_text(
            (text_x, text_y),
            wrapped_text,
            font=font,
            fill=(255, 255, 255, 255),
            spacing=4,
            align="center",
            stroke_width=2,
            stroke_fill=(0, 0, 0, 255),
        )

        return ImageTk.PhotoImage(Image.alpha_composite(hover_base, overlay).convert("RGB"))

    def start_game(self):
        print("Game started!")

    def open_library(self):
        print("Opening game library...")

    def open_game(self, game):
        print(f"Opening {game.name} from {game.path}...")

    def open_add_game_page(self):
        GamePage(self.winfo_toplevel(), on_save=self.add_game)

    def open_edit_game_page(self, game):
        GamePage(self.winfo_toplevel(), on_save=self.add_game, game=game)

    def remove_game(self, game):
        self.game_manager.remove_game(game)
        self._games = self.game_manager.get_games()
        self._render_grid(self._current_columns)

    def add_game(self, game, old_game=None):
        if old_game:
            self.game_manager.modify_game(old_game, game)
        else:
            self.game_manager.add_game(game)
        self._games = self.game_manager.get_games()
        self._render_grid(self._current_columns)