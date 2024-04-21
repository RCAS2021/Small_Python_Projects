import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

# Using stylesheet
plt.style.use('ggplot')

# Increasing max columns shown
pd.set_option('display.max_columns', 200)

# Reading dataset
df = pd.read_csv('CSV/coaster_db.csv')

# Showing shape
print(df.shape)

# Showing first rows
print(df.head())

# Showing all columns
print(df.columns)

# Showing dtypes
print(df.dtypes)

# Showing statistics about numeric data
print(df.describe())

# Step 2: Data Preparation
## Deleting irrelevant columns and rows
### Creating subset (Getting only the columns that will be used)
df = df[['coaster_name', 'Location', 'Length',
        'Status', 'Manufacturer',
        'year_introduced', 'latitude',
        'longitude', 'Type_Main',
        'opening_date_clean', 'speed_mph',
        'height_ft', 'Inversions_clean', 'Gforce_clean']].copy()

print(df.shape)

## Converting dates to datetime
df['opening_date_clean'] = pd.to_datetime(df['opening_date_clean'])

# Renaming columns
print(df.columns)
df = df.rename(columns={'coaster_name':'Coaster_Name',
                   'year_introduced':'Year_Introduced',
                   'opening_date_clean':'Opening_Date',
                   'speed_mph':'Speed_mph',
                   'height_ft':'Height_ft',
                   'Inversions_clean':'Inversions',
                   'Gforce_clean':'Gforce'})

# Identifying null values
print(df.isna().sum())

# Identifying duplicate rows
duplicated = df.loc[df.duplicated()]
print(duplicated)

# Checking for duplicate coaster name
duplicated_name = df.loc[df.duplicated(subset="Coaster_Name")]
print(duplicated_name)

# Checking duplicate name example
print(df.query('Coaster_Name == "Crystal Beach Cyclone"'))

# Removing duplicates
df = df.loc[~df.duplicated(subset=["Coaster_Name", "Location", "Opening_Date"])].reset_index(drop=True).copy()

# Feature Understanding (Univariate Analysis)

# Counting how many coasters introduced in each year
print(df['Year_Introduced'].value_counts())

# Plotting the counts for 10 most common years
year_count = df['Year_Introduced'].value_counts().head(10)
year_count.plot(kind='bar')
plt.title('Top 10 Years with Most Coasters Introduced')
plt.xlabel('Year')
plt.ylabel('Number of Coasters')
plt.show()

# Plotting speed frequency histogram, with more frequency = darker tone
data = df['Speed_mph']
num_bins = 25

# Plotting the histogram
counts, bins, patches = plt.hist(data, bins=num_bins, edgecolor='black', linewidth=0.5)

# Calculate the maximum frequency
max_count = max(counts)

# Calculate tonality of colors based on frequency
tonalities = counts / max_count

# Define custom colormap transitioning from green -> blue
colors = plt.cm.viridis_r(0.1 + 0.8 * tonalities)  # Interpolate from green to blue

# Applying colors to patches
for color, patch in zip(colors, patches):
    patch.set_facecolor(color)

# Setting title and labels
plt.title("Speed (mph) Frequency")
plt.xlabel("Speed (mph)")
plt.ylabel("Frequency")

plt.show()

# Plotting KDE (Kernel Density Estimation) for speed frequency
ax = df['Speed_mph'].plot(kind='kde')
ax.set_xlabel("Speed (mph)")
ax.set_title("KDE Speed(mph)")
plt.show()

# Feature Relationships

# Plotting a scatter plot to compare two columns (speed x height)
df.plot(kind="scatter", x="Speed_mph", y="Height_ft", title="Coaster speed x height")
plt.show()

# Now using Seaborn
# Plotting the scatter plot
sns.scatterplot(x="Speed_mph", y="Height_ft", hue='Year_Introduced', data=df)
plt.show()

# Plotting the speed frequency histogram
# Remove NaN values from the 'Speed_mph' column
data = df['Speed_mph'].dropna()

# Calculate frequency
num_bins = 25
counts, bins = np.histogram(data, bins=num_bins)

# Assign frequency values to the corresponding bins
df['Frequency'] = pd.cut(data, bins, labels=counts, include_lowest=True, ordered=False)

# Convert 'Frequency' column to numerical type
df['Frequency'] = df['Frequency'].astype(float)

# Plotting the histogram with Seaborn
sns.histplot(data=df, x='Speed_mph', bins=num_bins, kde=False, hue='Frequency', palette='viridis_r', edgecolor='black', linewidth=0.5)

# Customizing legend intervals
# Getting 10 intervals from max to min frequency
legend_intervals = np.linspace(df['Frequency'].max(), df['Frequency'].min(), num=10, dtype=int)
# Getting labels for each legend interval
legend_labels = [f'{int(j)} - {int(i)}' for i, j in zip(legend_intervals[:-1], legend_intervals[1:])]

# Manually setting legend colors
colors = sns.color_palette('viridis', len(legend_labels))
legend_handles = [plt.Line2D([0], [0], marker='o', color=color, label=label, markersize=5) for color, label in zip(colors, legend_labels)]
plt.legend(handles=legend_handles, title='Frequency')

# Setting title and labels
plt.title("Speed (mph) Frequency")
plt.xlabel("Speed (mph)")
plt.ylabel("Frequency")

plt.show()

# Comparing using Seaborn pairplot
sns.pairplot(data=df, vars=['Year_Introduced', 'Speed_mph', 'Height_ft', 'Inversions', 'Gforce'], hue="Type_Main")
plt.show()

# Getting correlation
# Removing NaN values
df_corr = df[['Year_Introduced', 'Speed_mph', 'Height_ft', 'Inversions', 'Gforce']].dropna()
# Printing correlation
df_corr = df_corr.corr()
print(df_corr)

# Visualizing by using seaborn heatmap
sns.heatmap(df_corr, annot=True)
plt.show()

# Asking questions about the data

# Q1: What are the locations with the fastest roller coasters (minimum of 10)?
# Getting fastest roller coasters groupped by location,
# by average speed where count >= 10
fastest = df.query('Location != "Other"').groupby('Location')['Speed_mph'].agg(['mean', 'count']).query('count >= 10')
# Sorting values by mean in descending order
fastest.sort_values('mean', ascending=True)

# Plotting horizontal bar plot
ax = fastest['mean'].sort_values(ascending=False).plot(kind='barh', title='Average Coaster Speed(mph) by Location')
ax.set_xlabel('Average Coaster Speed(mph)')

plt.show()

# Q2: Which are the longest roller coasters?
# By getting the longest by sorting the values using the length column there will be errors
longest = df[df['Length'].notna()].copy()
longest = df.sort_values('Length', ascending=False)
print(longest)

# It returns a wrong table, seeing why below
# The dataset has lengths that are ranges and not values,
# It also has both feet and meters, which need to be converted,
# It also has numbers that are formatted with commas and without commas

# Fixing the issues
import re

# Creating a function to process the length
def process_length(length):
    # Getting the length as a String
    length_str = str(length)
    # Using regex to find the numbers written in meters
    # \( and \) <- escaping parenthesis to match them literally
    # \d{1,3} <- matches 1 to 3 digits (thousands) at the beginning
    # (,\d{3})* <- matches zero or more occurrences of a comma followed by exactly three digits (thousands separator)
    # (\.\d+)? <- matches an optional decimal point followed by one or more digits (decimal part)
    # \s* <- matches zero or more whitespaces
    # m <- matches the letter m
    m_match = re.search(r'\((\d{1,3}(,\d{3})*(\.\d+)?)\s*m\)', length_str)
    if m_match:
        m_value = float(m_match.group(1).replace(',', ''))
        return m_value
    else:
        # Using regex to find the numbers written in feet
        ft_match = re.search(r'\((\d{1,3}(,\d{3})*(\.\d+)?)\s*ft\)', length_str)
        if ft_match:
            ft_value = float(ft_match.group(1).replace(',', ''))
            return ft_value * 0.3048
    return None

# Applying the function to the 'Length' column and storing the result in a new column 'Length_m'
df['Length_m'] = df['Length'].apply(process_length)

# Sorting the DataFrame by 'Length_m' in descending order and selecting the top 10 longest roller coasters
longest = df.sort_values('Length_m', ascending=False)
print(longest)

# Plotting a scatter plot comparing length with speed
ax = longest.plot(kind='scatter', x='Length_m', y='Speed_mph')
ax.set_xlabel('Length in meters')
ax.set_ylabel('Speed in mph')
ax.set_title('Length x Speed comparison')
plt.show()

# Plotting a heatmap to check the correlations
longest_corr = longest[['Year_Introduced', 'Height_ft', 'Inversions', 'Gforce', 'Length_m', 'Speed_mph']].corr()
sns.heatmap(longest_corr, annot=True)
plt.show()