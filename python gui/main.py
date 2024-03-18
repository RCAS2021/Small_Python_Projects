import customtkinter

# Creating App class with labels, checkbox, textarea and button
class App:

    def __init__(self, master) -> None:
        self.master = master

        # Creating method
        def login():
            print("Test")

        # Creating frame
        frame = customtkinter.CTkFrame(master=self.master)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Adding label, textarea, button and checkbox to frame
        label = customtkinter.CTkLabel(master=frame, text="Login System", font=("Roboto", 24))
        label.pack(pady=12, padx=10)

        entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
        entry1.pack(pady=12, padx=10)

        entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
        entry2.pack(pady=12, padx=10)

        button = customtkinter.CTkButton(master=frame, text="Login", command=login)
        button.pack(pady=12, padx=10)

        checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
        checkbox.pack(pady=12, padx=10)


if __name__ == "__main__":
    # Setting appearance mode (light, dark or system)
    customtkinter.set_appearance_mode("system")

    # Seting color theme (blue, green or dark-blue)
    customtkinter.set_default_color_theme("dark-blue")

    # Creating root
    root = customtkinter.CTk()

    # Setting title
    root.title("Login UI")

    # Setting dimensions
    root.geometry("500x350")

    # Calling App
    app = App(root)

    # Mainloop which will cause this toplevel to run infinitely
    root.mainloop()
