from pygame import mixer
import customtkinter as ctk
from customtkinter import filedialog

class App:
    def __init__(self, root):
        self.current_volume = 0.5
        self.root = root

        self.volume_button_held = None
        self.volume_change_step = 0.01

        root.title("Custom Music Player")

        # Creating main frame
        self.frame = ctk.CTkFrame(master=root)
        self.frame.pack(pady=10, padx=10, fill="none", expand=True)

        # Adding widgets to main frame
        # Label app title
        self.label_title = ctk.CTkLabel(master=self.frame, text="Custom Music Player", font=("Calibri", 17), width=120)
        self.label_title.pack(padx=10)
        # Label select music
        self.label_select = ctk.CTkLabel(master=self.frame, text="Select a music track", font=("Calibri", 12))
        self.label_select.pack(padx=10)
        # Select music button
        self.button_select = ctk.CTkButton(master=self.frame, text="Select music", font=("Calibri", 12), command=self.select_music)
        self.button_select.pack(padx=10, pady=5)
        # Label music title
        self.label_music_title = ctk.CTkLabel(master=self.frame, text="", font=("Calibri", 12))
        self.label_music_title.pack(padx=10, pady=10)

        # Creating play/pause/volume frame
        self.second_frame = ctk.CTkFrame(master=self.frame)
        self.second_frame.pack(after=self.label_music_title, padx=10, fill="none", expand=True)
    
        # Adding widgets to second frame
        # Pause button
        self.pause_button = ctk.CTkButton(master=self.second_frame, text="Pause", font=("Calibri", 12), width=55, command=self.pause)
        self.pause_button.pack(pady=10, side="left")
        # Play button
        self.resume_button = ctk.CTkButton(master=self.second_frame, text="Resume", font=("Calibri", 12), width=55, command=self.resume)
        self.resume_button.pack(pady=10, side="right")
        # Increase volume
        self.increase_volume_button = ctk.CTkButton(master=self.second_frame, text="+", font=("Calibri", 12), width=10)
        self.increase_volume_button.pack(pady=10, side="right")
        self.increase_volume_button.bind('<ButtonPress-1>', self.start_increase_volume)
        self.increase_volume_button.bind('<ButtonRelease-1>', self.stop_volume_change)
        # Decrease volume
        self.decrease_volume_button = ctk.CTkButton(master=self.second_frame, text="-", font=("Calibri", 12), width=10)
        self.decrease_volume_button.pack(pady=10, side="left")
        self.decrease_volume_button.bind('<ButtonPress-1>', self.start_decrease_volume)
        self.decrease_volume_button.bind('<ButtonRelease-1>', self.stop_volume_change)
        # Label volume
        self.label_volume = ctk.CTkLabel(master=self.second_frame, text=f"{0:.0f}%", font=("Calibri", 12))
        self.label_volume.pack(padx=10, pady=10, side="right")
        # Exit button
        self.exit_button = ctk.CTkButton(master=self.frame, text="Exit", font=("Calibri", 12), width=10, command=self.close_app)
        self.exit_button.pack(pady=10)


    def close_app(self):
        """ Function for closing app when clicking exit button """
        self.root.quit()

    def select_music(self) -> None:
        filepath = filedialog.askopenfilename(title="Select a music")
        if filepath:
            current_music = filepath
            music_title = filepath.split("/")
            music_title = music_title[-1]

            try:
                mixer.init()
                mixer.music.load(current_music)
                mixer.music.set_volume(self.current_volume)
                mixer.music.play()
                self.label_music_title.configure(text=f"Now Playing: {str(music_title)}")
                self.label_volume.configure(text=f"{self.current_volume*100:.0f}%")
            except Exception as e:
                print(e)
                self.label_music_title.configure(text="Error playing track")

    def change_volume(self, direction):
        if direction == "increase":
            self.current_volume += self.volume_change_step
        elif direction == "decrease":
            self.current_volume -= self.volume_change_step

        # Clamp volume to [0, 1]
        self.current_volume = max(0, min(1, self.current_volume))

        mixer.music.set_volume(self.current_volume)
        # Set volume
        if self.current_volume <= 0.009:
            self.label_volume.configure(text_color="red", text="Muted")
        else:
            self.label_volume.configure(text_color="white", text=f"{self.current_volume*100:.0f}%")

    def start_increase_volume(self, event):
        self.volume_button_held = "increase"
        self.change_volume("increase")
        self.after_id = self.root.after(80, self.continue_volume_change)

    def start_decrease_volume(self, event):
        self.volume_button_held = "decrease"
        self.change_volume("decrease")
        self.after_id = self.root.after(80, self.continue_volume_change)

    def stop_volume_change(self, event):
        self.volume_button_held = None
        if hasattr(self, 'after_id'):
            self.root.after_cancel(self.after_id)

    def continue_volume_change(self):
        if self.volume_button_held:
            self.change_volume(self.volume_button_held)
            self.after_id = self.root.after(100, self.continue_volume_change)

    def pause(self):
        try:
            mixer.music.pause()
        except Exception as e:
            print(e)

    def resume(self):
        try:
            mixer.music.unpause()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # Setting appearance mode (light, dark or system)
    ctk.set_appearance_mode("system")

    # Seting color theme (blue, green or dark-blue)
    ctk.set_default_color_theme("green")

    # Creating root
    root = ctk.CTk()

    # Calling App
    app = App(root)

    # Setting resizable
    root.resizable(True, True)

    # Mainloop which will cause this toplevel to run infinitely
    root.mainloop()
