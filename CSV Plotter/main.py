import customtkinter as ctk
from customtkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class CSVPlotter:
    def __init__(self, root):
        self.root = root
        root.title("CSV Plotter")

        # Creating a master frame
        self.scrollable_frame = ctk.CTkScrollableFrame(master=self.root, fg_color="#48494a", border_width=15)
        self.scrollable_frame.pack(fill='both', expand=True)

        # Creating a content frame
        self.frame = ctk.CTkFrame(master=self.scrollable_frame, fg_color="grey", border_width=5, border_color="brown")
        self.frame.pack(fill='both', expand=True)

        # Drop down menu
        self.plot_types = ["Line Plot", "Bar Plot", "Scatter Plot", "Pie"]
        self.plot_type_var = ctk.StringVar(value=self.plot_types[0])
        self.old_plot="Line Plot"
        plot_menu = ctk.CTkOptionMenu(master=self.frame, values=[*self.plot_types], variable=self.plot_type_var, command=self.update_plot)
        plot_menu.pack(padx=10, pady=10)

        # Creating load CSV button
        load_button = ctk.CTkButton(master=self.frame, text="Load CSV", command=self.load_csv)
        load_button.pack(padx=10, pady=10)

        # Creating fig ax
        self.fig, self.ax = plt.subplots()

        # Creating canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(padx=10, pady=10)

        self.df = None

        # Creating statistics button
        stat_button = ctk.CTkButton(master=self.frame, text="Show statistics", command=self.show_statistics)
        stat_button.pack(padx=10, pady=10)
        # Creating statistics textbox
        self.textbox = ctk.CTkTextbox(master=self.frame, width=550, font=("roboto", 24), wrap='word')
        self.textbox.pack(padx=10, pady=10)
        self.textbox.configure(state="disabled")

        # Creating exit button
        exit_button = ctk.CTkButton(master=self.frame, text="Exit", command=self.close_app)
        exit_button.pack(side="bottom", padx=10, pady=10)

    def close_app(self):
        self.root.quit()

    def load_csv(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.df = pd.read_csv(file_path)
            self.update_plot()

    def plot_pie(self, x, y):
        explode = (0, 0.05, 0, 0)
        self.ax.pie(self.df[y], labels=self.df[x], autopct='%1.1f%%', explode=explode, shadow=True, startangle=90, labeldistance=0.45, pctdistance=0.63, textprops={'horizontalalignment': 'center', 'verticalalignment': 'center'}, wedgeprops={'linewidth': 1}, radius=0.5, center=(0.5, 0.5))
        self.ax.legend(loc="lower right", ncol=len(self.df.columns))
        self.ax.axis("equal")
        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y)

    def plot_bar(self, x, y, z):
        # Recreate the ax2 object dynamically
        self.ax2 = self.ax.twinx()
        # Setting y-axis range to be the same for both axes
        ## Getting maximum Y axis value
        ## Next, set_ylim
        max_y = max(self.df.iloc[:,1].max(), self.df.iloc[:,2].max())
        # Plotting first dataset on y-axis
        self.ax.set_title("Animals X Quantity X Average_Age")
        self.df.iloc[:,1].plot(kind="bar", color="red", ax=self.ax, width=0.4, position=1)
        self.ax.legend(loc="upper left")
        self.ax.set_ylim(0, max_y+10)

        # Plotting second dataset on second y-axis
        self.df.iloc[:,2].plot(kind="bar", color="blue", ax=self.ax2, width=0.4, position=0)
        self.ax2.legend(loc="upper right")
        self.ax2.set_ylim(0, max_y+10)

        # Setting labels
        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y)
        self.ax2.set_ylabel(z)
        # Aligning the y-axis to the left
        self.ax.yaxis.set_label_position("left")
        self.ax.yaxis.set_ticks_position("left")
        # Aligning the secondary y-axis to the right
        self.ax2.yaxis.set_label_position("right")
        self.ax2.yaxis.set_ticks_position("right")
        # Returning the x labels to animal names instead of index
        x_values = range(len(self.df))
        self.ax.set_xticks(x_values)  # Set x-ticks at each index
        self.ax.set_xticklabels(self.df[x], rotation=0)  # Set x-tick labels to animal names   

    def plot_line(self, x, y, z):
        self.ax.plot(self.df[x], self.df[y], label=f"{y} vs {x}")
        self.ax.plot(self.df[x], self.df[z], label=f"{x} vs {z}")
        self.ax.legend(loc="best")
        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y)

    def plot_scatter(self, x, y, z):
        self.ax.scatter(self.df[x], self.df[y], label=f"{y} vs {x}")
        self.ax.scatter(self.df[x], self.df[z], label=f"{x} vs {z}")
        self.ax.legend(loc="best")
        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y)

    def update_plot(self, event=None):
        if self.df is not None:
            plot_type = self.plot_type_var.get()
            x = self.df.columns[0]
            y = self.df.columns[1]
            z = self.df.columns[2]

            # Clear the figure and all axes
            self.fig.clear()

            # Add new Axes object
            self.ax = self.fig.add_subplot(111)

            if plot_type == "Line Plot":
                self.plot_line(x, y, z)
            elif plot_type == "Bar Plot":
                self.plot_bar(x, y, z)
            elif plot_type == "Scatter Plot":
                self.plot_scatter(x, y, z)
            elif plot_type == "Pie":
                self.plot_pie(x, y)

            # Set aspect ratio to auto
            self.ax.set_aspect('auto')
            # Draws canvas
            self.canvas.draw()

    def show_statistics(self):
        self.textbox.configure(state="normal")
        biggest_average_age = max(self.df.Avg_Age)
        most_quantity = max(self.df.Qtt)
        most_animal = self.df.loc[self.df.Qtt == most_quantity]
        most_animal = str(most_animal['Animals'].values).strip('[]').strip("'")
        total_animal = sum(self.df.Qtt)
        total_average = np.mean(self.df.Avg_Age)
        self.textbox.insert("0.0", f"The biggest average age is: {biggest_average_age}\nThe animal type with most animals is: {most_animal} with {most_quantity} total\n" +
                            f"There are {total_animal} animals in total\nThe average of all average ages is: {total_average}")
        self.textbox.configure(state="disabled")

if __name__ == "__main__":
    # Setting appearance mode (light, dark or system)
    ctk.set_appearance_mode("system")

    # Seting color theme (blue, green or dark-blue)
    ctk.set_default_color_theme("dark-blue")

    # Creating root
    root = ctk.CTk()

    # Calling App
    app = CSVPlotter(root)

    # Setting dimensions
    root.minsize(500, 750)

    # Setting resizable
    root.resizable(True, True)

    # Mainloop which will cause this toplevel to run infinitely
    root.mainloop()
