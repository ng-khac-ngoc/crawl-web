import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd

import os

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths for CSV files
csv_file_path = os.path.join(script_dir, 'data/tin-nhiem-mang.csv')

# Define columns for the CSV file
columns = ['Date of Detection', 'Phishing Website URL']


# Function to write data to a CSV file
def write_to_csv(csv_file_path, columns, data):
    try:
        # Read the current CSV file into a DataFrame
        existing_data_df = pd.read_csv(csv_file_path)

        # Create a Pandas DataFrame from new data
        new_data_df = pd.DataFrame(data, columns=columns)

        # Combine the current DataFrame with the new DataFrame
        combined_df = pd.concat([existing_data_df, new_data_df], ignore_index=True)

    except FileNotFoundError:
        # If the file does not exist, create a new DataFrame with the provided data
        combined_df = pd.DataFrame(data, columns=columns)

    # Remove duplicate data
    combined_df = combined_df.drop_duplicates()
    # Save the combined DataFrame back to a CSV file
    combined_df.to_csv(csv_file_path, index=False)


# Function to crawl a page and extract data
def crawl_page(soup):
    elements = soup.find_all('li', class_='item1')
    websites = []
    for element in elements:
        website = []

        # Date of Detection
        website.append(element.find('div', class_='date').text.replace('Đã phát hiện ngày ', ''))
        # Phishing Website URL
        website.append(element.find('div', class_='sf-semibold').text.replace(' ', ''))

        # Status
        status = element.find('div', class_='status').text

        # Filter "Đã xử lý" Status
        if ('Đã xử lý' in status):
            websites.append(website)
    return websites


# Function to crawl the website within a given range of pages
def crawl_website(start_page, last_page):
    # Specify the URL
    url = 'https://tinnhiemmang.vn/website-lua-dao'

    for i in range(start_page, last_page + 1):
        if (i == 1426):
            continue
        print('Page ' + str(i) + ' crawl được ')
        # Send a GET request to the URL
        response = requests.get(url + '?page=' + str(i))

        # Check if the request is successful (status code 200)
        soup = BeautifulSoup(response.content, "html.parser")

        data = crawl_page(soup)

        write_to_csv(csv_file_path, columns, data)


# Crawl to page 6200
def main():
    crawl_website(0, 6200)


if __name__ == "__main__":
    main()
