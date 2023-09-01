import pandas as pd

# Function to clean up the names
def clean_name(name):
    # Remove comma
    name = name.replace(',', '')
   
    # Split the name into words
    words = name.split()
   
    # If the name has more than two words, remove the third word
    if len(words) > 2:
        words = words[:2]
   
    # Join the words back together into one name
    name = ' '.join(words)
   
    return name

# Let's start by reading the Excel files again
df1 = pd.read_excel('name_id_dict.xlsx')
df2 = pd.read_excel('threefour.xlsx')

# Clean the names in df2
df2['Cleaned Name'] = df2['Name'].apply(clean_name)

# Set 'Cleaned Name' as index for both dataframes for easy referencing
df1.set_index('Cleaned Name', inplace=True)
df2.set_index('Cleaned Name', inplace=True)

# For each cleaned name in df2, if it exists in df1, copy the 'ID' from df1 to '3/4 ID' in df2
for name in df2.index:
    if name in df1.index:
        df2.loc[name, '3/4 ID'] = df1.loc[name, 'ID']

# Reset index to make 'Cleaned Name' a column again
df2.reset_index(inplace=True)

# Drop the 'Cleaned Name' column
df2 = df2.drop(columns='Cleaned Name')

# Save the updated DataFrame to a new Excel file
df2.to_excel('threefour_updated.xlsx', index=False)

df2.head()
