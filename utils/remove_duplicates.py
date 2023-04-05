import pandas as pd

# TODO: make these functions commands in the CLI
def remove_duplicates(input_file: str, output_file: str) -> None:
    # Load the JSON file into a pandas DataFrame
    try:
        df = pd.read_json(input_file, lines=True)
    except ValueError:
        raise ValueError(f"Error reading JSON file: {input_file}")
    
    # Remove duplicate rows based on the specified column
    df = df.drop_duplicates(subset='idiom')
    
    # Save the resulting DataFrame to a new JSON file
    try:
        df.to_json(output_file, orient='records', lines=True)
    except ValueError:
        raise ValueError(f"Error writing JSON file: {output_file}")

if __name__ == '__main__':
    raw_data = "/Users/davidmcsharry/Documents/idiom_search/idiom_search/output.json"
    unique_data = "/Users/davidmcsharry/Documents/idiom_search/idiom_search/unique_output.json"
    remove_duplicates(raw_data, unique_data)

