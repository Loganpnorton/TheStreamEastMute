import tkinter as tk
from tkinter import ttk
import os
import subprocess
import threading

class TheStreamMutedApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("TheStreamMuted")
        self.geometry("600x400")

        self.create_main_screen()

    def create_main_screen(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill="both")

        # On/Off Toggle
        self.toggle_var = tk.BooleanVar()
        toggle_button = ttk.Checkbutton(main_frame, text="Toggle", variable=self.toggle_var, command=self.toggle_mute)
        toggle_button.pack(pady=20)

        # Status Text
        self.status_label = ttk.Label(main_frame, text="Status: Click on where TSE is playing!")
        self.status_label.pack()

        # Console Text
        self.console_text = tk.Text(main_frame, height=10)
        self.console_text.pack(fill="both", expand=True)

        # Settings Button
        settings_button = ttk.Button(main_frame, text="Settings", command=self.open_settings)
        settings_button.pack(pady=20)

    def toggle_mute(self):
        if self.toggle_var.get():
            self.tnt_process = subprocess.Popen(["python", "tnt.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = self.tnt_process.communicate()
            if stdout:
                self.console_text.insert("end", stdout)
                self.console_text.see("end")
            if stderr:
                self.console_text.insert("end", stderr)
                self.console_text.see("end")
            self.status_label.config(text="Status: Muted")
        else:
            if hasattr(self, 'tnt_process'):
                self.tnt_process.terminate()  # Terminate the subprocess
            self.status_label.config(text="Status: Unmuted")

    def read_stream(self):
        while True:
            line = self.tnt_process.stdout.readline()
            if not line:
                break
            print("stdout:", line)  # Debug print
            self.console_text.insert("end", line)
            self.console_text.see("end")

            line = self.tnt_process.stderr.readline()
            if not line:
                break
            print("stderr:", line)  # Debug print
            self.console_text.insert("end", line)
            self.console_text.see("end")

    def open_settings(self):
        settings_window = SettingsWindow(self)


class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Settings")
        self.geometry("300x200")

        self.parent = parent

        self.create_settings()

    def create_settings(self):
        settings_frame = ttk.Frame(self)
        settings_frame.pack(expand=True, fill="both")

        # Spotify Play/Pause Keybind
        spotify_keybind_label = ttk.Label(settings_frame, text="Spotify Play/Pause Keybind:")
        spotify_keybind_label.grid(row=0, column=0, padx=10, pady=10)
        self.spotify_keybind_entry = ttk.Entry(settings_frame)
        self.spotify_keybind_entry.grid(row=0, column=1, padx=10, pady=10)

        # Browser Choice
        browser_label = ttk.Label(settings_frame, text="Browser Choice:")
        browser_label.grid(row=1, column=0, padx=10, pady=10)
        self.browser_choice = ttk.Combobox(settings_frame, values=["Firefox", "Chrome", "Edge"])
        self.browser_choice.grid(row=1, column=1, padx=10, pady=10)

        # Add Images To Seek
        images_label = ttk.Label(settings_frame, text="Add Images To Seek:")
        images_label.grid(row=2, column=0, padx=10, pady=10)
        images_button = ttk.Button(settings_frame, text="Browse", command=self.open_image_folder)
        images_button.grid(row=2, column=1, padx=10, pady=10)

        # Save Button
        save_button = ttk.Button(settings_frame, text="Save", command=self.save_settings)
        save_button.grid(row=3, column=0, columnspan=2, pady=20)

    def open_image_folder(self):
        folder_path = filedialog.askdirectory(initialdir=os.path.expanduser("~"),
                                               title="Select Image Folder")
        if folder_path:
            os.startfile(folder_path)

    def save_settings(self):
        # Save Spotify Play/Pause Keybind
        spotify_keybind = self.spotify_keybind_entry.get()
        # Save Browser Choice
        browser_choice = self.browser_choice.get()
        # Write settings to file
        settings_path = os.path.join(os.path.dirname(__file__), "Internal", "settings.txt")
        with open(settings_path, "w") as file:
            file.write(f"Spotify Play/Pause Keybind: {spotify_keybind}\n")
            file.write(f"Browser: {browser_choice}\n")

        # Close settings window
        self.destroy()

if __name__ == "__main__":
    app = TheStreamMutedApp()
    app.mainloop()
