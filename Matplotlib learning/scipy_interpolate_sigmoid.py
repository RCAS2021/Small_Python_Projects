import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import pchip_interpolate

# Given data points
x_data = np.array([-7.3, -6.3, -6, -5.3, -5, -4.3, -4, -3.45])
y_data = np.array([12.75, 16.5, 25.5, 72, 135.5, 266.5, 279, 279])

# Remove duplicate y-values by taking the unique elements
unique_indices = np.unique(y_data, return_index=True)[1]
x_data_unique = np.array(x_data)[unique_indices]
y_data_unique = np.array(y_data)[unique_indices]

# Value of y for which we want to find x
target_y = 139.5

# Perform piecewise cubic Hermite interpolating polynomial (PCHIP) interpolation
target_x_pchip = pchip_interpolate(y_data_unique, x_data_unique, target_y)

# Plotting the original data points
plt.scatter(x_data, y_data, label='Log concentração X Resposta(mm)')

# Plotting the target point
plt.scatter(target_x_pchip, target_y, color='red', label=f'CE50% = ({target_x_pchip:.2f}, {target_y})')
plt.annotate(f'({target_x_pchip:.2f}, {target_y})', (target_x_pchip, target_y), textcoords="offset points", xytext=(0,10), ha='center')

# Plotting the interpolation curve
y_interp = np.linspace(min(y_data_unique), max(y_data_unique), 1000)
x_interp = pchip_interpolate(y_data_unique, x_data_unique, y_interp)

# Append the point (-3.45, 279) to extend the interpolation curve
x_interp = np.append(x_interp, -3.45)
y_interp = np.append(y_interp, 279)

plt.plot(x_interp, y_interp, label='Função sigmóide')

# Plotting dashed lines
plt.plot([target_x_pchip, target_x_pchip], [plt.ylim()[0], target_y], 'k--', lw=1)  # dashed line from x to y axis
plt.plot([plt.xlim()[0], target_x_pchip], [target_y, target_y], 'k--', lw=1)  # dashed line from y to x axis

# Plotting lines from target point to x and y axes
plt.plot([target_x_pchip, target_x_pchip], [0, target_y], color='gray', linestyle='--', lw=1)  # vertical line to y-axis
plt.plot([-7.5, target_x_pchip], [target_y, target_y], color='gray', linestyle='--', lw=1)  # horizontal line to x-axis

# Adding text for the value on the axes
plt.text(target_x_pchip, -10, f'{target_x_pchip:.2f}', ha='center', va='top')
plt.text(-7.5, target_y, f'{target_y}', ha='right', va='center')

xlabel = "Log Concentração"
ylabel = "Resposta(mm)"
# Adding labels and title
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(f'Relação {xlabel} x {ylabel}')

# Displaying the legend
plt.legend()
# Setting axis limits
plt.xlim(-7.5, plt.xlim()[1])  # Adjusting x-axis limit to start from -7.5
plt.ylim(0, plt.ylim()[1])     # Adjusting y-axis limit to start from 0
plt.grid(True)

# Displaying the plot
plt.show()

print("PCHIP Interpolation - Interpolated value for x:", target_x_pchip)