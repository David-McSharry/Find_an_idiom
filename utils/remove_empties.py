import pandas as pd

# TODO: make these functions commands in the CLI

def remove_empty_lines(input_file: str, output_file: str) -> None:
    # Read the input file into a pandas dataframe
    try:
        df = pd.read_json(input_file, lines=True)
    except ValueError as e:
        print(f"Error reading input file: {e}")
        return

    # Remove any rows where the idiom or description field is empty
    df = df[df['idiom'].notna() & (df['description'] != '')]

    # Write the resulting data to the output file
    try:
        df.to_json(output_file, orient='records', lines=True)
    except Exception as e:
        print(f"Error writing to output file: {e}")

if __name__ == '__main__':
    raw_data = "/Users/davidmcsharry/Documents/idiom_search/test.json"
    clean_data = "/Users/davidmcsharry/Documents/idiom_search/test_no_empties.json"
    remove_empty_lines(raw_data, clean_data)