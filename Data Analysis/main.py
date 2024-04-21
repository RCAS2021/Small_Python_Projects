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
