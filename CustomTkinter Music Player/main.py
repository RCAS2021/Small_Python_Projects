import pygame
from pygame import mixer
import customtkinter as ctk
from customtkinter import filedialog

class App:
    """Custom Music Player Application.

    This class implements a custom music player application using Tkinter for the GUI and Pygame for audio playback.

    Attributes:
        current_volume (float): The current volume level of the music player, ranging from 0.0 to 1.0.
        root: The root Tkinter window.
        volume_button_held (str): Indicates the direction of volume change being held, either 'increase', 'decrease', or None.
        volume_change_step (float): The step size by which the volume changes on each increment or decrement.
        frame: The main frame of the application's GUI.
        label_title: The label displaying the title of the application.
        label_select: The label prompting the user to select a music track.
        button_select: The button for selecting a music track.
        label_music_title: The label displaying the currently playing music title.
        second_frame: The secondary frame containing playback controls and volume slider.
        pause_button: The button to pause playback.
        decrease_volume_button: The button to decrease volume.
        label_volume: The label displaying the current volume level.
        increase_volume_button: The button to increase volume.
        resume_button: The button to resume playback.
        slide_volume: The slider for adjusting volume.
        exit_button: The button to exit the application.

    Methods:
        __init__: Initializes the App instance.
        close_app: Closes the application.
        select_music: Opens a file dialog for selecting a music track and plays it.
        change_volume: Changes the volume level based on the specified direction.
        start_increase_volume: Initiates continuous volume increase when the increase volume button is pressed.
        start_decrease_volume: Initiates continuous volume decrease when the decrease volume button is pressed.
        delayed_increase_volume: Performs delayed volume increase when the increase volume button is pressed.
        delayed_decrease_volume: Performs delayed volume decrease when the decrease volume button is pressed.
        stop_volume_change: Stops continuous volume change when the volume change button is released.
        continue_volume_change: Continues continuous volume change until the volume change button is released.
        pause: Pauses playback of the music track.
        resume: Resumes playback of the music track.
    """
    def __init__(self, master):
        """
        Initialize the Custom Music Player application.

        Parameters:
        - root (tkinter.Tk): The root Tkinter instance for the application.
        """
        self.current_volume = 0.5
        self.master = master

        self.volume_button_held = None
        self.volume_change_step = 0.01

        master.title("Custom Music Player")

        # Creating main frame
        self.frame = ctk.CTkFrame(master=master)
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
        self.pause_button.grid(row=0, column=0, padx=(0, 10))

        # Decrease volume button
        self.decrease_volume_button = ctk.CTkButton(master=self.second_frame, text="-", font=("Calibri", 12), width=10)
        self.decrease_volume_button.grid(row=0, column=1)
        self.decrease_volume_button.bind('<ButtonPress-1>', self.start_decrease_volume)
        self.decrease_volume_button.bind('<ButtonRelease-1>', self.stop_volume_change)

        # Volume label
        self.label_volume = ctk.CTkLabel(master=self.second_frame, text=f"{0:.0f}%", font=("Calibri", 12))
        self.label_volume.grid(row=0, column=2)

        # Increase volume button
        self.increase_volume_button = ctk.CTkButton(master=self.second_frame, text="+", font=("Calibri", 12), width=10)
        self.increase_volume_button.grid(row=0, column=3)
        self.increase_volume_button.bind('<ButtonPress-1>', self.start_increase_volume)
        self.increase_volume_button.bind('<ButtonRelease-1>', self.stop_volume_change)

        # Play button
        self.resume_button = ctk.CTkButton(master=self.second_frame, text="Resume", font=("Calibri", 12), width=55, command=self.resume)
        self.resume_button.grid(row=0, column=4, padx=(10, 0))

        # Slider volume
        self.slide_volume = ctk.CTkSlider(master=self.second_frame, from_=0, to=100, command=self.update_volume)
        self.slide_volume.grid(row=1, column=0, columnspan=5, pady=(10, 0))

        # Exit button
        self.exit_button = ctk.CTkButton(master=self.frame, text="Exit", font=("Calibri", 12), width=10, command=self.close_app)
        self.exit_button.pack(pady=10)


    def close_app(self):
        """
        Close the Custom Music Player application.
        """
        self.master.quit()

    def select_music(self) -> None:
        """
        Open a file dialog to select a music track and play it.
        """
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
            except pygame.error as e:
                print(e)
                self.label_music_title.configure(text="Error playing track")

    def change_volume(self, direction):
        """
        Change the volume of the music.

        Parameters:
        - direction (str): The direction of volume change ("increase" or "decrease").
        """
        try:
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
        except pygame.error as e:
            print(e)
            self.label_music_title.configure(text="Select the music first")

    def start_increase_volume(self, event):
        """
        Start increasing the volume when the volume increase button is pressed.

        Parameters:
        - event: The event object associated with the button press.
        """
        self.volume_button_held = "increase"
        self.change_volume("increase")
        self.after_id = self.master.after(100, self.continue_volume_change)

    def start_decrease_volume(self, event):
        """
        Start decreasing the volume when the volume decrease button is pressed.

        Parameters:
        - event: The event object associated with the button press.
        """
        self.volume_button_held = "decrease"
        self.change_volume("decrease")
        self.after_id = self.master.after(100, self.continue_volume_change)

    def delayed_increase_volume(self):
        """
        Increase the volume after a short delay if the volume increase button is held.
        """
        if self.volume_button_held == "increase":
            self.change_volume("increase")
            self.after_id = self.master.after(80, self.continue_volume_change)

    def delayed_decrease_volume(self):
        """
        Decrease the volume after a short delay if the volume decrease button is held.
        """
        if self.volume_button_held == "decrease":
            self.change_volume("decrease")
            self.after_id = self.master.after(80, self.continue_volume_change)

    def stop_volume_change(self, event):
        """
        Stop changing the volume when the volume increase/decrease button is released.

        Parameters:
        - event: The event object associated with the button release.
        """
        self.volume_button_held = None
        if hasattr(self, 'after_id'):
            self.master.after_cancel(self.after_id)

    def continue_volume_change(self):
        """
        Continue changing the volume if the volume increase/decrease button is held.
        """
        if self.volume_button_held:
            self.change_volume(self.volume_button_held)
            self.after_id = self.master.after(60, self.continue_volume_change)

    def update_volume(self, value):
        """
        Update the volume of the music based on the slider value.

        Parameters:
        - value (float): The new volume value selected by the user on the slider.
        """
        try:
            # Convert slider value from 0-100 to 0.0-1.0
            self.current_volume = float(value) / 100
            mixer.music.set_volume(self.current_volume)
            if self.current_volume <= 0.009:
                self.label_volume.configure(text_color="red", text="Muted")
            else:
                self.label_volume.configure(text_color="white", text=f"{self.current_volume*100:.0f}%")
        except pygame.error as e:
            print(e)
            self.label_music_title.configure(text="Select the music first")

    def pause(self):
        """
        Pause the currently playing music.
        """
        try:
            mixer.music.pause()
        except pygame.error as e:
            print(e)
            self.label_music_title.configure(text="Select the music first")

    def resume(self):
        """
        Resume playing the paused music.
        """
        try:
            mixer.music.unpause()
        except pygame.error as e:
            print(e)
            self.label_music_title.configure(text="Select the music first")


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
