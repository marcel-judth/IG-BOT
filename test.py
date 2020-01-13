import pandas as pd

# Assign spreadsheet filename to `file`
file = 'followed_users.xlsx'

# Load spreadsheet
xl = pd.ExcelFile(file)

# Print the sheet names
print(xl.sheet_names)

# Load a sheet into a DataFrame by name: df1
df = xl.parse('Sheet')
xl.
df = df.sort_values('time')

for i in range(len(df)) : 
    
  print(df.loc[i, "username"], df.loc[i, "time"]) 