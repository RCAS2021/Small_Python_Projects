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
df = df[['coaster_name', 'Location',
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

# Plotting the histogram with Seaborn
sns.histplot(data=df, x='Speed_mph', bins=num_bins, kde=False, hue='Frequency', palette='viridis_r', edgecolor='black', linewidth=0.5)

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

# Using seaborn heatmap
sns.heatmap(df_corr, annot=True)
plt.show()