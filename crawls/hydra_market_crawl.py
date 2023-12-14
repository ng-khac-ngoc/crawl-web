import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd

import os

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths for CSV files
csv_file_path = os.path.join(script_dir, 'data/hydra-market.csv')

# Define columns for the CSV file
columns = ['URL', 'Date of crawl']


# Function to write data to a CSV file
def write_to_csv(csv_file_path, columns, data):
    try:
        # Read the current CSV file into a DataFrame
        existing_data_df = pd.read_csv(csv_file_path)

        # Create a Pandas DataFrame from new data
        new_data_df = pd.DataFrame(data, columns=columns)

        # Combine the current DataFrame with the new DataFrame
        combined_df = pd.concat([new_data_df, existing_data_df], ignore_index=True)
    except FileNotFoundError:
        # If the file does not exist, create a new DataFrame with the provided data
        combined_df = pd.DataFrame(data, columns=columns)

    # Remove duplicate data based on the 'URL' column
    combined_df = combined_df.drop_duplicates(subset=['URL'])

    # Save the combined DataFrame back to a CSV file
    combined_df.to_csv(csv_file_path, index=False)


# Function to crawl the website and extract data
def crawl_website():
    # Specify the URL you want to crawl
    # url = 'https://hydramarket.org/phishing/en/active-phishing-today-list.php'
    url = 'https://hydramarket.org/phishing/en/active-phishing-list.php'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request is successful (status code 200) and parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    urls = []

    # Split the HTML content by '<br/>' to separate different elements
    elements = str(soup).split('<br/>')
    for element in elements:
        url = []
        url.append(element.replace('\n', '').replace(' ', ''))
        url.append(date.today().strftime("%d/%m/%Y"))
        # Only append non-empty elements to the list
        if (len(element.replace('\n', ''))):
            urls.append(url)
    return urls


# Function to schedule crawl
def crawl():
    data = crawl_website()
    write_to_csv(csv_file_path, columns, data)


# Main function to initiate crawl process
def main():
    crawl()


if __name__ == "__main__":
    main()
