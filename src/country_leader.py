import requests
from requests import Session
import json
import csv
from typing import List, Dict
from .leader import Leader


class CountryLeaders:
    """
        A class for managing country leaders' data.

        Attributes:
            root_url (str): The root URL for the API.
            status_endpoint (str): The endpoint for checking the API status.
            leaders_endpoint (str): The endpoint for getting leaders data.
            countries_endpoint (str): The endpoint for getting countries data.
            cookie_endpoint (str): The endpoint for managing cookies.
            leaders_data (List[Leader]): List of Leader objects.
            countries_data (List): List of country data.
            cookies_data (str): Cookies data for authentication.
            output_json_file (str): Path to the output JSON file.
            output_csv_file (str): Path to the output CSV file.
        """

    def __init__(self):
        """
            Initializes CountryLeaders instance and fetches countries and leaders data.
        """
        self.root_url = "https://country-leaders.onrender.com"
        self.status_endpoint = "/status/"
        self.leaders_endpoint = "/leaders"
        self.countries_endpoint = "/countries/"
        self.cookie_endpoint = "/cookie"

        # Initialize variables
        self.leaders_data: List[Leader] = []
        self.countries_data: List = []
        self.cookies_data: str = ''

        # Output file paths
        self.output_json_file = './output/leaders_per_country.json'
        self.output_csv_file = './output/leaders_per_country.csv'
        self.session = Session()

        # Fetch initial data
        self.get_countries()
        self.get_leaders()

    def refresh_cookies(self):
        with self.session as session:
            try:
                self.cookies_data = session.get(url=f"{self.root_url}{self.cookie_endpoint}").cookies
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
                self.refresh_cookies()

    def check_status(self):
        """
        Check the status of the API.

        Returns:
            bool: True if API status is okay, False otherwise.
        """
        with self.session as session:
            try:
                # Send a GET request to the status endpoint
                response = session.get(f"{self.root_url}{self.status_endpoint}")
                # Check if the response status code is 200 (OK)
                return response.status_code == 200
            except requests.exceptions.HTTPError as errh:
                # Handle HTTP errors (e.g., 404, 500, etc.)
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                # Handle connection errors (e.g., DNS resolution failure, connection refused, etc.)
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                # Handle timeout errors (e.g., server not responding within the specified timeout)
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                # Handle any other request exception that may occur
                print("OOps: Something Else", err)

    def get_countries(self) -> List:
        """
        Get countries data from the API.

        Returns:
            List: List of countries data.
        """
        temp_country_data: List = []
        # Check for API status, if it's okay return countries data, otherwise returns None
        with self.session as session:
            if self.check_status():
                # Fetch cookies
                self.refresh_cookies()
                attempt = 1
                try:
                    # Fetch countries data
                    response = session.get(url=f"{self.root_url}{self.countries_endpoint}", cookies=self.cookies_data)
                    self.countries_data = response.json()
                    temp_country_data = self.countries_data
                    return temp_country_data
                except requests.exceptions.RequestException as e:
                    if hasattr(e, 'response') and e.response.status_code == 401:
                        # Handling the case of expired cookies
                        print("Cookies have expired!")
                        print("Refreshing")
                        print(f"Attempt {attempt}")
                        attempt += 1
                        if attempt <= 5:
                            self.refresh_cookies()
                            # Retry getting countries
                            self.get_countries()
                        else:
                            print("Too many attempts.")
                    elif hasattr(e, 'response') and e.response.status_code == 403:
                        # Handling expired cookies or other access restrictions
                        print("Access prohibited. Cookies may have expired.")
                        print("Refreshing")
                        print(f"Attempt {attempt}")
                        attempt += 1
                        if attempt <= 5:
                            self.refresh_cookies()
                            # Retry getting countries
                            self.get_countries()
                        else:
                            print("Too many attempts.")
                    else:
                        # Handling other types of request errors
                        print("An error occurred during the request:", e)
                finally:
                    return temp_country_data

            else:
                return temp_country_data

    def get_leaders(self):
        """
        Get leaders data from the API.
        """
        with self.session as session:
            # Check if API status is okay
            if self.check_status():
                # Iterate through countries' data. Extract JSON data

                for country in self.countries_data:
                    attempt = 1
                    try:
                        response = session.get(url=f"{self.root_url}{self.leaders_endpoint}", cookies=self.cookies_data,
                                               params={'country': country})
                        leaders_raw_data = response.json()
                        # leaders_sorted = sorted(leaders_raw_data, key=lambda x: x['id'], reverse=True)

                        # Iterate through leaders data for the country. Create Leader object and append to leaders_data
                        for leader in leaders_raw_data:
                            self.leaders_data.append(Leader(leader, country=country))
                    except requests.exceptions.RequestException as e:
                        if hasattr(e, 'response') and e.response.status_code == 401:
                            # Handling the case of expired cookies
                            print("Cookies have expired!")
                            print("Refreshing")
                            print(f"Attempt {attempt}")
                            attempt += 1
                            if attempt <= 5:
                                self.refresh_cookies()
                                self.get_leaders()
                            else:
                                print("Too many attempts.")

                        elif hasattr(e, 'response') and e.response.status_code == 403:
                            # Handling expired cookies or other access restrictions
                            print("Access prohibited. Cookies may have expired.")
                            print("Refreshing")
                            print(f"Attempt {attempt}")
                            attempt += 1
                            if attempt <= 5:
                                self.refresh_cookies()
                                self.get_leaders()
                            else:
                                print("Too many attempts.")
                        else:
                            # Handling other types of request errors
                            print("An error occurred during the request:", e)

    def print_leaders(self):
        """
        Print the leaders' data.
        """
        for leader in self.leaders_data:
            print(leader)

    def export_to_json(self):
        """
        Export leaders data to a JSON file.
        """

        leaders_per_country: Dict[str:List] = {}
        try:
            # Initialize dictionary with countries as keys
            for country in self.countries_data:
                leaders_per_country[country] = []

            # Populate leaders for each country
            for leader in self.leaders_data:
                leaders_per_country[leader.country].append(leader.to_json())

            # Write to JSON file
            with open(self.output_json_file, 'w') as json_output_file:
                json.dump(obj=leaders_per_country, fp=json_output_file, ensure_ascii=False, indent=4)
        except TypeError as e:
            print(f"Error when serializing data as JSON: {e}")
        except FileNotFoundError as e:
            print(f"Error opening JSON file: {e}")
        except PermissionError as e:
            print(f"Permissions error when writing to JSON file: {e}")
        except IOError as e:
            print(f"I/O error when writing to JSON file: {e}")
        except Exception as e:
            print(f"Unexpected error when exporting to JSON: {e}")

    def export_to_csv(self):
        """
        Export leaders data to a CSV file.
        """
        try:
            # Get headers from leaders' data
            headers = self.leaders_data[0].to_json().keys()

            # Write to CSV file
            with open(self.output_csv_file, 'w') as output_csv_file:
                writer = csv.DictWriter(output_csv_file, fieldnames=headers)
                writer.writeheader()
                for leader in self.leaders_data:
                    try:
                        writer.writerow(leader.to_json())
                    except Exception as e:
                        print(f"Error converting leader to JSON: {e}")

        except Exception as e:
            print("Error exporting to CSV: ", e)
