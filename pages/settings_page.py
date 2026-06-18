import tkinter as tk
from tkinter import filedialog

from cfg import app_config as conf

class SettingsPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg=conf.BGCOLOR)

        # Create a label for the settings page
        label = tk.Label(self, text="Settings", font=("Arial", 24), bg=conf.BGCOLOR, fg=conf.FGCOLOR)
        label.pack(pady=20)

        self.build_ui()
    
    def build_ui(self):
        # Create a frame for the settings options
        options_frame = tk.Frame(self, bg=conf.BGCOLOR)
        options_frame.pack(pady=10)

        # Open Steam save file path button
        path_label = tk.Label(options_frame, text="Steam Save File Path:", bg=conf.BGCOLOR, fg=conf.FGCOLOR)
        path_label.pack(pady=10)

        self.path = tk.Label(options_frame, text="", bg=conf.BGCOLOR, fg=conf.FGCOLOR)
        self.path.pack(pady=10)

        open_savefile_button = tk.Button(
            options_frame,
            text="Open Steam Save File Path",
            command=self._choose_steam_folder_path,
            bg=conf.HOVERCOLOR,
            fg=conf.FGCOLOR
        )
        open_savefile_button.pack(pady=10)

        # Save button
        save_button = tk.Button(self, text="Save", command=self.save_settings, bg=conf.HOVERCOLOR, fg=conf.FGCOLOR)
        save_button.pack(pady=20)
    
    def _choose_steam_folder_path(self):
        selected_path = filedialog.askdirectory(
            parent=self,
            title="Select Steam Folder",
        )
        if not selected_path:
            return

        self._selected_steam_folder_path = selected_path
        self.path.configure(text=selected_path)
    
    def save_settings(self):
        # Save the settings (e.g., Steam save file path) to a configuration file or database
        # You can implement the logic to save the settings here
        print("Settings saved!")
        self.destroy()  # Close the settings page after saving