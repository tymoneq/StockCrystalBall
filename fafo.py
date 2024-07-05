import pandas as pd

# Example DataFrame
data = {'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8]}
df = pd.DataFrame(data, index=['row1', 'row2', 'row3', 'row4'])

# Find the row index using loc
row_name = 'row3'
row = df.loc[row_name]
print(row)

# Find the integer index using index.get_loc
row_name = 'row3'
row_index = df.index.get_loc(row_name)
print(row_index)

row_data = df.iloc[row_index]
print(row_data)