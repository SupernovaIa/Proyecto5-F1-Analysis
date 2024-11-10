from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import random
import pandas as pd
import re
import requests


def get_dotd(current_year = '2024'):
    """
    Fetches and returns the HTML content of the "Driver of the Day" page.

    This function uses a web driver to navigate to the Formula 1 "Driver of the Day" page. It handles cookie acceptance by interacting with the cookie iframe, navigates to the desired section, and retrieves the HTML content of the page.

    Parameters:
    - current_year (str, optional): Year for which to retrieve the "Driver of the Day" page content. Default is '2024' but it should be current year since it's the only way to get into the data.

    Returns:
    - BeautifulSoup or None: Parsed HTML content of the "Driver of the Day" page if successful, otherwise `None` if an error occurs.
    """

    url = "https://www.formula1.com/en/results/awards"

    # Open browser and get url
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        driver.maximize_window()

        sleep(random.uniform(1,2))

        # We need to locate an iframe to accept cookies
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located(('xpath', '//*[@id="sp_message_iframe_1149950"]')))
        driver.switch_to.frame(iframe)
        # Accept cookies
        try:
            driver.find_element('css selector', '#notice > div.message-component.message-row.unstack > button.message-component.message-button.no-children.focusable.sp_choice_type_11').click()
        except Exception as e:
            print("Can't find cookies:", e)

        # Come back to default content
        driver.switch_to.default_content()

        # Go to driver of the day page
        sleep(random.uniform(1,2))
        driver.find_element(By.XPATH, f"//p[text()='Driver of the Day {current_year}']").click()

        # Get content
        sleep(random.uniform(1,2))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

    except Exception as e:
        print("An error occurred while trying to scrape the page:", e)
        soup = None

    finally:
        # Close driver
        driver.close()

    return soup


def get_df_dotd(soup: BeautifulSoup):
    """
    Parses HTML content to extract race data and returns a formatted DataFrame.

    This function extracts tables from an HTML document, where each table contains data for a particular racing season. It iterates through the rows of each table, retrieves information about individual races, drivers, and teams, and appends this data to a final DataFrame. Each row in the DataFrame represents a race, and the 'year' column is populated with the season year.

    Parameters:
    - soup (BeautifulSoup): Parsed HTML content containing race tables.

    Returns:
    - pd.DataFrame: DataFrame with columns 'race', 'driver', 'team', and 'year', containing race data across multiple seasons.
    """

    # Get tables from the soup
    tables = soup.findAll("table")

    # Build an empty dataframe to store the data
    df_final = pd.DataFrame()

    for table in tables:
        # Find rows for every season (table)
        races = table.findAll("tr")

        list_races = []
        
        for race in races:
            # Find values for every race (row)
            values = race.findAll("td")
            list_values = [value.text for value in values]

            list_races.append(list_values)

        df = pd.DataFrame(list_races)
        # Get the season and add it to the dataframe
        year = re.match(r'\d+', table.find("th").text).group()
        df['year'] = year
        
        df_final = pd.concat([df, df_final])

    # Drop null values (index = 0) and rename columns
    df_final = df_final.drop(0).rename(columns={0: 'race', 1: 'driver', 2: 'team'})

    return df_final


def get_add_circuit_info(url: str):
    """
    Fetches and extracts specific information about a circuit from a given URL.

    Parameters:
    - url (str): The URL of the web page to scrape for circuit information.

    Returns:
    - (tuple): A tuple containing:
        - capacity (str): The seating capacity of the circuit or 'NA' if not found.
        - website (str): The official website of the circuit or 'NA' if not found.
        - architect (str): The name of the architect or 'NA' if not found.
    """
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

    else:
        print(f"Error: {response.status_code}")
        return

    # Find table
    table = soup.find("table", {"class": "infobox vcard"})

    # If table was found, extract the info
    if table:
        rows = table.findAll("tr")

        # Set default values
        capacity = 'NA'
        website = 'NA'
        architect = 'NA'

        # Go through rows
        for row in rows:
            header_cell = row.find("th")
            if header_cell:
                # Look for specific items
                text = header_cell.text.strip().lower()

                if text == 'capacity':
                    capacity = row.find("td").text

                elif text == 'website':
                    website = row.find("td").text

                elif text == 'architect':
                    architect = row.find("td").text

        return capacity, website, architect
    
    # If table was not found, look for proper link
    else:
        # Find link
        url = soup.find('a', string=re.compile('Circuit', re.IGNORECASE)).get("href")
        root = 'https://en.wikipedia.org'
        # Add link root in case it's not added
        if root not in url:
            url = root + url

        # Call function again with corrected link
        return get_add_circuit_info(url)
    

def transform_circuits_df(df: pd.DataFrame):
    """
    Transforms the input DataFrame by extracting and formatting additional information from circuit URLs and the location column.

    Parameters:
    - df (pd.DataFrame): The original DataFrame containing circuit data with columns including 'url' and 'Location'.

    Returns:
    - (pd.DataFrame): The transformed DataFrame with additional columns for 'capacity', 'website', 'architect', and separate location information, while removing the original 'Location' column.
    """
    # Get additional info from circuit Wikipedia link
    df_add_info = df['url'].apply(get_add_circuit_info).apply(pd.Series)

    # Renaming columns
    df_add_info = df_add_info.rename(columns={0: 'capacity', 1: 'website', 2: 'architect'})
    # Formatting values properly
    df_add_info['capacity'] = df_add_info['capacity'].apply(lambda x: int(re.sub(r'[^0-9]', '', re.sub(r'\[.*?\]', '', x.split('(')[0]))) if re.search(r'\d+', x) else None)
    df_add_info['website'] = df_add_info['website'].apply(lambda x: re.search(r'http[s]?://\S+|www\.\S+', x).group(0) if re.search(r'http[s]?://\S+|www\.\S+', x) else None)
    df_add_info['architect'] = df_add_info['architect'].apply(lambda x: re.sub(r'\[.*?\]', '', x).strip() if pd.notnull(x) else None)

    # Extraction location info
    df_location = df['Location'].apply(pd.Series)
    # Now we don't need location column
    df.drop(columns='Location', inplace=True)

    # Putting everything together
    df = pd.concat([df, df_add_info, df_location], axis=1)

    return df


def get_df_circuit(year: int):
    """
    Fetches circuit data for a specified Formula 1 season and returns it as a transformed DataFrame.

    Parameters:
    - year (int): The year of the Formula 1 season to retrieve circuit data for.

    Returns:
    - (pd.DataFrame): A DataFrame containing the transformed circuit data for the specified year.
    """

    # Get F1 circuit information from ergast API
    url = f'http://ergast.com/api/f1/{str(year)}/circuits.json'

    response = requests.get(url)

    if response.status_code == 200:

        content = response.json()
        circuits = content['MRData']['CircuitTable']['Circuits']
        df_circ = pd.DataFrame(circuits)
        df = transform_circuits_df(df_circ)
        return df

    else:
        print(f"Error: {response.status_code}")
        return


def get_df_drivers(year:int):
    """
    Fetches driver data for a specified Formula 1 season and returns it as a DataFrame with renamed columns.

    Parameters:
    - year (int): The year of the Formula 1 season to retrieve driver data for.

    Returns:
    - (pd.DataFrame): A DataFrame containing driver data with columns 'first_name' and 'last_name'.
    """

    url = f"http://ergast.com/api/f1/{str(year)}/drivers.json"

    response = requests.get(url)

    if response.status_code == 200:

        content = response.json()
        drivers = content['MRData']['DriverTable']['Drivers']
        df_drivers = pd.DataFrame(drivers)
        df_drivers.rename(columns={'givenName': 'first_name', 'familyName': 'last_name'}, inplace=True)
        return df_drivers

    else:
        print(f"Error: {response.status_code}")
        return