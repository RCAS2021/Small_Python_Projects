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
heights = np.random.normal(172, 8, 300)

plt.boxplot(heights)


plt.show()






