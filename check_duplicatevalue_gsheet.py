import pandas as pd

def find_duplicate_values(csv_file, column_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Check for duplicate values in the specified column
    duplicate_values = df[df.duplicated(column_name, keep=False)]

    if not duplicate_values.empty:
        print(f'Duplicate values in column "{column_name}":')
        print(duplicate_values)
    else:
        print(f'No duplicate values found in column "{column_name}".')

# Example usage
csv_file_path = 'path/to/your/file.csv'
column_to_check = 'your_column_name'

find_duplicate_values(csv_file_path, column_to_check)
