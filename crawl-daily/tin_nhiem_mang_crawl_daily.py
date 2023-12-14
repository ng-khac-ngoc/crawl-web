import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd

import os

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths for CSV files
csv_file_path = os.path.join(script_dir, 'data/tin-nhiem-mang.csv')
daily_csv_file_path = os.path.join(script_dir, 'data/tin-nhiem-mang-daily.csv')

# Define columns for the CSV files
columns = ['Date of Detection', 'Phishing Website URL']

# Read data from the daily file
daily_df = pd.read_csv(daily_csv_file_path)
# Retrieve the latest crawled URL
lastest_crawl_url = daily_df['Lastest URL'][0]


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

    # Remove duplicate data based on the 'Phishing Website URL' column
    combined_df = combined_df.drop_duplicates(subset=['Phishing Website URL'])
    # Save the combined DataFrame back to a CSV file
    combined_df.to_csv(csv_file_path, index=False)


# Function to crawl the website and extract data
def crawl_website():
    last_page = 6200
    # Specify the URL you want to crawl
    url = 'https://tinnhiemmang.vn/website-lua-dao'

    page = 0
    websites = []
    while True:
        print('Page ' + str(page) + ' has been crawled.')
        # Send a GET request to the URL
        response = requests.get(url + '?page=' + str(page))

        # Check if the request is successful (status code 200)
        soup = BeautifulSoup(response.content, "html.parser")

        elements = soup.find_all('li', class_='item1')
        for element in elements:
            website = []

            # Phishing Website URL
            fake_url = element.find('div', class_='sf-semibold').text.replace(' ', '')
            # Stop if the fake_url has been crawled or if crawling reaches the last page
            if (fake_url == lastest_crawl_url or page == last_page):
                if (len(websites) != 0):
                    daily_df['Lastest URL'][0] = websites[0][1]
                    daily_df['Lastest Date Crawl'][0] = date.today().strftime("%d/%m/%Y")
                    daily_df.to_csv(daily_csv_file_path, index=False)
                return websites

            # Date of Detection
            website.append(element.find('div', class_='date').text.replace('Đã phát hiện ngày ', ''))

            # Phishing Website URL
            website.append(fake_url)

            # Status
            status = element.find('div', class_='status').text

            if ('Đã xử lý' in status):
                print(fake_url)
                websites.append(website)
        page += 1


# Function to schedule the daily crawling job
def job_daily_crawl():
    data = crawl_website()
    write_to_csv(csv_file_path, columns, data)


# Main function to initiate the daily crawling process
def main():
    job_daily_crawl()


if __name__ == "__main__":
    main()
