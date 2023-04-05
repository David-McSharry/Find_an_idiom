import pandas as pd
import re

# TODO: make these functions commands in the CLI
def remove_html(input_file: str, output_file: str) -> None:
    # Read the file into a pandas dataframe
    df = pd.read_json(input_file, lines=True)

    # Replace " <span class="illustration">" with "Example: "
    df['description'] = df['description'].apply(lambda x: x.replace(' <span class="illustration">', ' Example: '))

    # Remove the contents of the "<i>" tag
    df['description'] = df['description'].apply(lambda x: re.sub('<i>.*?<\/i>', '', x))

    # Remove the remaining HTML tags
    df['idiom'] = df['idiom'].apply(lambda x: re.sub('<[^<]+?>', '', x))
    df['description'] = df['description'].apply(lambda x: re.sub('<[^<]+?>', '', x))

    # Save the dataframe back to a new JSON file
    df.to_json(output_file, orient='records', lines=True)

if __name__ == '__main__':
    raw_data = "/Users/davidmcsharry/Documents/idiom_search/idiom_search/unique_output.json"
    clean_data = "/Users/davidmcsharry/Documents/idiom_search/output_no_HTML.json"
    remove_html(raw_data, clean_data)
