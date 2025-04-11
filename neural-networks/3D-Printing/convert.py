import pandas as pd

def convert_json_to_csv(printer_data_log.json, csv_filepath):
    try:
        df = pd.read_json(json_filepath)
        df.to_csv(csv_filepath, index=False, encoding='utf-8')
        print(f"Successfully converted '{json_filepath}' to '{csv_filepath}'")
    except FileNotFoundError:
        print(f"Error: JSON file '{json_filepath}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
json_file = 'data.json'
csv_file = 'data.csv'
convert_json_to_csv(json_file, csv_file)