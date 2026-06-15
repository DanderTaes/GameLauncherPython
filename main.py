import tkinter as tk

from cfg import app_config as conf
from pages import home_page as hp, navbar as nb


# TODO: add right click to images to remove/notes/favorites
# TODO: add overlay to images with game name on hover and heart always
# TODO: add search bar to filter games by name
# TODO: add game tags/groups
# TODO: steam game launch from steam id (steam://rungameid/APPID)
# TODO: steamgriddb API?

class GameLauncherApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Game Launcher")
        self.root.geometry("900x600")
        self.root.configure(bg=conf.BGCOLOR)

        self.navbar = nb.Navbar(self.root, controller=self)
        self.navbar.pack(side="top", fill="x")

        self.content = tk.Frame(self.root, bg=conf.BGCOLOR)
        self.content.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for frame_class in (hp.HomePage,):
            frame = frame_class(self.content, controller=self)
            self.frames[frame_class.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.show_frame("HomePage")

    def show_frame(self, frame_name: str) -> None:
        frame = self.frames[frame_name]
        frame.tkraise()

    def quit(self) -> None:
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = GameLauncherApp()
    app.run()
