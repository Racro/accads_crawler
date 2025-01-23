import json
import re

lst = ['adblock_germany', 'adblock_US', 'adblock_under_18', 'adblock_over_18', 'control_germany', 'control_US', 'control_under_18', 'control_over_18']

# Function to clean Unicode escape characters and non-ASCII characters
def clean_data(input_data):
    if isinstance(input_data, str):
        # Remove Unicode escape sequences
        cleaned = re.sub(r'\\u[0-9a-fA-F]{4}', '', input_data)
        # Remove non-ASCII characters
        cleaned = re.sub(r'[^\x00-\x7F]', '', cleaned)
        return cleaned
    elif isinstance(input_data, list):
        return [clean_data(item) for item in input_data]
    elif isinstance(input_data, dict):
        return {key: clean_data(value) for key, value in input_data.items()}
    else:
        return input_data

# Function to modify keys using the last segment after splitting by '/'
def modify_keys(input_data):
    if isinstance(input_data, dict):
        return {key.split('/')[-1]: modify_keys(value) for key, value in input_data.items()}
    elif isinstance(input_data, list):
        return [modify_keys(item) for item in input_data]
    else:
        return input_data

for i in lst:
    # Load the JSON file
    file_path = f'ocr_{i}.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Clean the data
    cleaned_data = clean_data(data)

    # Modify the keys
    modified_data = modify_keys(cleaned_data)

    # Save the cleaned data to a new file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(modified_data, file, ensure_ascii=False, indent=4)

    print(f"Fully cleaned file saved to: {file_path}")
