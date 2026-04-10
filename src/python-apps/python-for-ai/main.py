import pandas as pd

# Create a sample dataframe for data analysis tutorial
data = {
    'First_Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'] * 4,
    'Last_Name': ['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson'] * 4,
    'Age': [25, 30, 35, 28, 32] * 4,
    'Salary': [50000, 60000, 75000, 55000, 70000] * 4,
    'Department': ['Sales', 'IT', 'HR', 'Sales', 'IT'] * 4
}

df = pd.DataFrame(data)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.colheader_justify', 'left')

print(df.to_string(index=False))
