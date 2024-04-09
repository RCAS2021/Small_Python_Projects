import numpy as np
import matplotlib.pyplot as plt

# Creating some data
#X_data = np.random.random(50) * 100
#Y_data = np.random.random(50) * 100

# Creating scatter plot with some parameters
#plt.scatter(X_data, Y_data, marker="*", s=75, alpha=0.3)

# Preparing data for line plot
#years = [2006 + x for x in range(16)]
#weights = [80, 83, 84, 85, 86, 82, 81, 79, 83, 81, 80, 76 , 75, 80, 79, 80]

# Creating line plot with some parameters
#plt.plot(years, weights)

# Creating data for bar plot
#x = ["C++", "C#", "Python", "Java", "Go"]
#y = [20, 50, 140, 3, 45]

# Creating bar plot with some parameters
#plt.bar(x, y)

# Creating data for histogram using np.random distribution
# Mean = 20, STD = 1.5, 1000 ages
#ages = np.random.normal(20, 1.5, 1000)

# Creating histogram with some parameters
#plt.hist(ages)

# Creating histogram and specifying bins
#plt.hist(ages,
#         bins=[ages.min(), 18, 21, ages.max()])

# Another example
#plt.hist(ages,
#         bins=30)

# Creating histogram with cumulative
#plt.hist(ages,
#         bins=10,
#         cumulative=True)

# Creating data for pie chart
#x = ["C++", "C#", "Python", "Java", "Go"]
#y = [20, 50, 140, 3, 45]
#explodes =[0, 0, 0, 0.2, 0]

# Creating pie chart
#plt.pie(y, labels=x, explode=explodes, autopct="%.2f%%", startangle=90)

# Creating data for boxplot
#heights = np.random.normal(172, 8, 300)

#plt.boxplot(heights)

# Plot customization example
# Creating data
#years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
#income = [55, 56, 62, 61, 71, 72, 73, 75]

#income_ticks = list(range(50, 81, 2))

#plt.plot(years, income)
#plt.title("Income per year (in USD)", fontsize=25, fontname="Arial")
#plt.xlabel("Year")
#plt.ylabel("Yearly income in USD")
# Setting Y to plot according to income_ticks(start=50, finish=81, step=2)
# And add K to represent thousand
#plt.yticks(income_ticks, [f"${x}k" for x in income_ticks])

# Creating data for multiple plots and legends example
#stock_a = [100, 102, 99, 101, 101, 100, 102]
#stock_b = [90, 95, 102, 104, 105, 103, 109]
#stock_c = [110, 115, 100, 105, 100, 98, 95]

#ear = [2016, 2017, 2018, 2019, 2020, 2021, 2022]

#plt.plot(year, stock_a, label="Company A")
#plt.plot(year, stock_b, label="Company B")
#plt.plot(year, stock_c, label="Company C")
#plt.legend()

# Plot Styling
# Importing styles
#from matplotlib import style

# Using style
#style.use("ggplot")
# Links for style sheets
# Link Styles: https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
# Link Customizations: https://matplotlib.org/stable/tutorials/introductory/customizing.html


# Creating data for plot styling example
#votes = [10, 2, 5, 16 ,22]
#people = ["A", "B", "C", "D", "E"]

# Plotting pie chart with added style
#plt.pie(votes, labels=None)
#plt.legend(labels=people)

# Creating multiple figures
# Creating data
#x1, y1 = np.random.random(100), np.random.random(100)
#x2, y2 = np.arange(100), np.random.random(100)

# Creating and specifying figure 1
#plt.figure(1)
# Plotting a scatter plot in figure 1
#plt.scatter(x1, y1)

# Creating and specifying figure 2
#plt.figure(2)
# plotting a line plot in figure 2
#plt.plot(x2, y2)

# Creating subplots
#x = np.arange(100)

# Creating subplots with 2 x 2 grid ((0,0), (0,1), (1,0), (1,1))
# This will create 4 subplots in 1 figure
#fig, axs = plt.subplots(2, 2)

# To access the subplot
#axs[0, 0].plot(x, np.sin(x))
#axs[0, 0].set_title("Sine Wave")

#axs[0, 1].plot(x, np.cos(x))
#axs[0, 1].set_title("Cosine Wave")

#axs[1, 0].plot(x, np.log(x))
#axs[1, 0].set_title("Log Function")

#axs[1, 1].plot(x, np.random.random(100))
#xs[1, 1].set_title("Random Function")

# Adding suptitle to figure
#fig.suptitle("Four plots example")

# Setting layout to tight to remove title overlap
#plt.tight_layout()
# Exporting plot, dpi increases quality
#plt.savefig("Fourplots.png", dpi=300, transparent=True)

# 3D Plotting
#ax = plt.axes(projection="3d")

#x = np.random.random(100)
#y = np.random.random(100)
#z = np.random.random(100)

#ax.scatter(x, y, z)
#ax.set_title("3D Scatter plot")
#ax.set_xlabel("X")
#ax.set_ylabel("Y")
#ax.set_zlabel("Z")

# Plotting surface

# Creating 3D plot
ax = plt.axes(projection="3d")

# Creating data
x = np.arange(-5, 5, 0.1)
y = np.arange(-5, 5, 0.1)

# Creating mesh grid
X, Y = np.meshgrid(x, y)

Z = np.sin(X) * np.cos(Y)

# Plotting surface
ax.plot_surface(X, Y, Z, cmap="Spectral")
ax.set_title("3D Surface")

plt.show()
