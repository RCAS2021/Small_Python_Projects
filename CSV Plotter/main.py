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
        plot_menu = ctk.CTkOptionMenu(master=self.frame, values=[*self.plot_types], variable=self.plot_type_var, command=self.update_plot)
        plot_menu.pack(padx=10, pady=10)

        # Pie Attributes drop down menu
        self.attribute = ["Qtt", "Avg_Age"]
        self.attribute_var = ctk.StringVar(value=self.attribute[0])
        self.attribute_options = []

        # Creating load CSV button
        self.load_button = ctk.CTkButton(master=self.frame, text="Load CSV", command=self.load_csv)
        self.load_button.pack(padx=10, pady=10)

        # Creating fig ax
        self.fig, self.ax = plt.subplots()

        # Creating canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(padx=10, pady=10)

        self.df = None

        # Creating statistics textbox
        self.textbox = ctk.CTkTextbox(master=self.frame, width=550, font=("roboto", 24), wrap='word')
        self.textbox.pack(padx=10, pady=10)
        self.textbox.configure(state="disabled")

        # Creating statistics button
        self.stat_button = ctk.CTkButton(master=self.frame, text="Show statistics", command=self.show_statistics)
        self.stat_button.pack(before=self.textbox, padx=10, pady=10)

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
        self.ax.axis("equal")
    
    def create_attribute_menu(self):
        # Creating attribute menu
        self.attribute_menu = ctk.CTkOptionMenu(master=self.frame, values=[*self.attribute_options], variable=self.attribute_var)
        self.attribute_menu.pack(after=self.load_button, padx=10, pady=10)

    def plot_bar(self, columns):
        # Recreate the ax2 object dynamically
        self.ax2 = self.ax.twinx()
        # Plotting first dataset on y-axis
        self.df.iloc[:,1].plot(kind="bar", color="red", ax=self.ax, width=0.4, position=1)

        # Plotting second dataset on second y-axis
        self.df.iloc[:,2].plot(kind="bar", color="blue", ax=self.ax2, width=0.4, position=0) 

    def plot_line(self, columns):
        self.ax2 = self.ax.twinx()  # Create a secondary y-axis
        # Plotting first dataset on y-axis
        self.df.iloc[:,1].plot(kind="line", color="red", ax=self.ax)

        # Plotting second dataset on second y-axis
        self.df.iloc[:,2].plot(kind="line", color="blue", ax=self.ax2)


    def plot_scatter(self, columns):
        self.ax2 = self.ax.twinx()  # Create a secondary y-axis
        # Plotting first dataset on y-axis
        self.df.plot(kind="scatter", x=self.df.columns[0], y=self.df.columns[1], label=f"{columns[1]}", color="red", ax=self.ax)

        # Plotting second dataset on second y-axis
        self.df.plot(kind="scatter", x=self.df.columns[0], y=self.df.columns[2], label=f"{columns[2]}", color="blue", ax=self.ax)

    def set_labels(self):
        self.ax.set_xlabel(self.df.columns[0])
        self.ax.set_ylabel(self.df.columns[1])
        self.ax2.set_ylabel(self.df.columns[2])

    def synchronize_y_axes(self, df, y_columns):
        # Calculate the maximum y value from the specified columns in the DataFrame
        max_y = max(df[y_columns].max())

        # Adjust the y-axis limits for both axes
        self.ax.set_ylim(0, max_y + 10)
        self.ax2.set_ylim(0, max_y + 10)

    def set_x_axis_labels(self, x_values, x_labels):
        self.ax.set_xticks(x_values)  # Set x-ticks at each index
        self.ax.set_xticklabels(x_labels, rotation=0)  # Set x-tick labels to animal names

    def create_combined_legends(self):
        # Creating combined legends
        # Get handles and labels for both axes
        handles1, labels1 = self.ax.get_legend_handles_labels()
        handles2, labels2 = self.ax2.get_legend_handles_labels()

        # Combine handles and labels
        all_handles = handles1 + handles2
        all_labels = labels1 + labels2

        # Create a single legend
        self.ax.legend(all_handles, all_labels, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)

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

            # Destroy the attribute menu if it exists
            if hasattr(self, 'attribute_menu') and self.attribute_menu.winfo_exists():
                self.attribute_menu.destroy()

            if plot_type == "Line Plot":
                self.plot_line(list(self.df.columns))
            elif plot_type == "Bar Plot":
                self.plot_bar(list(self.df.columns))
            elif plot_type == "Scatter Plot":
                self.plot_scatter(list(self.df.columns))
            elif plot_type == "Pie":
                # Setting options to be columns then create attribute menu
                self.attribute_options = list(self.df.columns[1:])
                self.create_attribute_menu()
                self.plot_pie(x, y)

            # Creating combined legends
            self.create_combined_legends()

            if plot_type != "Pie":
                # Setting title
                self.ax.set_title("Animals X Quantity X Average_Age")

                self.synchronize_y_axes(self.df, self.df.columns[1:])
                # Set x-axis labels
                x_values = range(len(self.df))
                self.set_x_axis_labels(x_values, self.df[x])

            # Setting labels
            self.set_labels()

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
