import pandas as pd

# Add last names (extend to 20 names) and update the data dictionary accordingly

first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Evan', 'Fiona', 'George', 'Hannah', 'Ian', 'Julia',
              'Kevin', 'Laura', 'Michael', 'Nina', 'Oscar', 'Paula', 'Quentin', 'Rachel', 'Sam', 'Tina']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'White', 'Harris']

ages = [25, 30, 35, 40, 29, 31, 28, 33, 45, 38, 27, 32, 36, 41, 34, 39, 26, 37, 42, 24]
salaries = [70000, 80000, 120000, 90000, 75000, 83000, 72000, 95000, 105000, 87000,
            68000, 91000, 100000, 86000, 94000, 89000, 76000, 98000, 113000, 79000]
departments = ['HR', 'Engineering', 'Marketing', 'Finance', 'Engineering', 'HR', 'Marketing', 'Finance', 'Sales', 'Engineering',
               'Marketing', 'Finance', 'Sales', 'HR', 'Finance', 'Engineering', 'Sales', 'Marketing', 'HR', 'Finance']

data = {
    'First Name': first_names,
    'Last Name': last_names,
    'Age': ages,
    'Salary': salaries,
    'Department': departments
}

df = pd.DataFrame(data)



