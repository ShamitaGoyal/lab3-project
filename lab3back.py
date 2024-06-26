# Name: Shamita Goyal
# Lab 3: Web Access, Data Storage

import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from urllib.parse import urlparse

# -----------------------------------------------------
# Scrape data from the website and generate JSON file
# Part A
# -----------------------------------------------------

def scrape_and_gen_json():
    # Base URL of the website (adjust as needed)
    url = 'https://www.timeout.com/things-to-do/best-places-to-travel'

    # Parse the URL
    parsed_url = urlparse(url)

    # Extract the scheme (e.g., 'https') and the netloc (e.g., 'www.timeout.com')
    root_url = f'{parsed_url.scheme}://{parsed_url.netloc}'

    # Print the root URL
    print(root_url)

    # Send a GET request to the current page
    response = requests.get(url)

    # Initialize the variables
    month = None
    destination_name = None
    destination_summary = None
    destination_url = None

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find and extract articles
        articles = soup.find_all('article')

        extracted_data = []

        if articles:
            for month_index, article in enumerate(articles):

                # print(article.prettify())

                month_h3_tag = article.find('h3', class_='_h3_cuogz_1')
                if month_h3_tag:
                    article_month = month_h3_tag.get_text()
                    month_num = month_index + 1
                    month = f'{month_num}.{article_month}'

                # print(month)

                link = article.find('a')
                if link is not None:
                    link_href = link.get('href')
                    if link_href:
                        print(f'Link: {link_href}')
                        print('----------------------------------')

                        # Monthly Article URL
                        mthly_article_url = f'{root_url}{link_href}'
                        print(mthly_article_url)

                        mthly_response = requests.get(mthly_article_url)
                        mthly_soup = BeautifulSoup(mthly_response.content, 'html.parser')
                        location_rankings = mthly_soup.find_all('article', class_='tile _article_kc5qn_1')

                        if location_rankings:
                            for index, location_ranking in enumerate(location_rankings):

                                # print(location_ranking.prettify())

                                # Finding Destination ranking
                                destination_ranking = index + 1

                                # Finding Destination Name
                                # Find the <h3> tag with the specific class
                                h3_tag = location_ranking.find('h3', class_='_h3_cuogz_1')
                                if h3_tag:
                                    # Extract the text without the text inside <span>
                                    text_parts = [element for element in h3_tag.contents if not element.name == 'span']
                                    destination_name = ''.join([str(part) for part in text_parts]).strip()
                                else:
                                    print('H3 tag not found.')

                                # Finding Destination Summary
                                summary_div = location_ranking.find('div', class_='_summary_kc5qn_21')

                                if summary_div:

                                    # Find first instance of <p> tags within the <div>
                                    p_tags = summary_div.find('p')
                                    destination_summary = p_tags.get_text(strip=True)

                                    a_tags = summary_div.find_all('a')

                                    for a_tag in a_tags:
                                        # Check if 'discover' is in the parent tag text
                                        if a_tag.find_parent('strong'):
                                            if 'discover' in a_tag.find_parent('strong').get_text(strip=True).lower():
                                                # Print the <a> tag href attribute
                                                destination_url = a_tag['href']
                                                break  # Exit after finding the first match

                                    # Print the results
                                    # print('\n')
                                    # print(f'Destination Ranking : {destination_ranking}')
                                    # print(f'Destination Name    : {destination_name}')
                                    # print(f'Destination Summary : {destination_summary}')
                                    # print(f'Destination URL     : {destination_url}')
                                else:
                                    print('Summary div not found..')

                                # Add the data into a dictionary

                                extracted_data.append((
                                                      month, destination_name, destination_ranking, destination_summary,
                                                      destination_url))
                        else:
                            print("No Destination ranking articles found.")
        else:
            print("No articles found.")
    else:
        print(f'Failed to retrieve page. Status code: {response.status_code}')

    # Create dictionary from the tuple
    # Initialize an empty dictionary to store the destinations
    destinations_dict = {}

    # Loop through the extracted data and create nested dictionaries
    for data in extracted_data:
        month, destination_name, destination_ranking, destination_summary, destination_url = data
        ranking_info = {
            "Ranking": destination_ranking,
            "Summary": destination_summary,
            "URL": destination_url
        }

        # Check if the destination already exists in the dictionary
        if destination_name not in destinations_dict:
            destinations_dict[destination_name] = {}

        # Add the ranking info to the destination's dictionary with the month as the key
        destinations_dict[destination_name][month] = ranking_info

    # Specify the filename for the JSON file
    json_file = 'destinations.json'

    # Write the dictionary data to a JSON file
    with open(json_file, 'w') as file:
        json.dump(destinations_dict, file, indent=4)

    print(f'Dictionary data has been written to {json_file}')


# -----------------------------------------------------
# Part B
# -----------------------------------------------------

def load_json_in_db():
    # Read JSON data from file
    json_file = 'destinations.json'
    with open(json_file, 'r') as file:
        destinations_dict = json.load(file)

    # Connect to SQLite database
    conn = sqlite3.connect('destinations.db')
    cursor = conn.cursor()

    # drop table (to be commented after testing)
    cursor.execute('''
    drop  TABLE destinations
    ''')

    # Create table destinations
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS destinations (
        id INTEGER PRIMARY KEY,
        destination_name TEXT,
        month_num integer,
        month TEXT,
        ranking INTEGER,
        summary TEXT,
        url TEXT
    )''')

    # Insert data into table
    for destination_name, months in destinations_dict.items():
        for month, details in months.items():
            cursor.execute('''
            INSERT INTO destinations (destination_name, month, month_num,ranking, summary, url)
            VALUES (?, ?, ?,?, ?, ?)
            ''',
                           (destination_name, month.split('.')[1], month.split('.')[0], details['Ranking'],
                            details['Summary'], details['URL']))

    # Create table months
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS months AS
    SELECT distinct month_num, month from destinations
    '''
                   )

    # Commit and close connection
    conn.commit()
    conn.close()

    print(f'Data from {json_file} has been loaded into the database.')


# Call functions
scrape_and_gen_json()
load_json_in_db()

# End of lab3back code

