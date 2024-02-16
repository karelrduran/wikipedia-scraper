import re
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, Process
from .country_leader import CountryLeaders


class WikipediaScraper:
    """
    A class for scraping Wikipedia data for country leaders.

    Attributes:
        country_leaders (CountryLeaders): An instance of CountryLeaders.
    """

    def __init__(self):
        """
        Initializes WikipediaScraper.
        """
        self.country_leaders: CountryLeaders = CountryLeaders()

    def clean_paragraph(self, text: str) -> str:
        """
        Clean a paragraph by removing newlines, references, and special characters.

        Args:
            text (str): The paragraph text to be cleaned.

        Returns:
            str: The cleaned paragraph text.
        """
        new_line = r'\n'
        ref = r'\[\d+\]'
        xa = r'\xa0'
        modified_text = text
        # Replace newlines, references, and special characters
        modified_text = re.sub(new_line, '', modified_text)
        modified_text = re.sub(ref, '', modified_text)
        modified_text = re.sub(xa, ' ', modified_text)
        return modified_text

    def get_first_paragraph(self, leader: object, soup: BeautifulSoup) -> None:
        """
        Get the first paragraph of the Wikipedia article for the given leader
        and assign it to the leader's 'bio_first_paragraph' attribute.

        Args:
            leader (object): The leader object for whom the first paragraph of the
                             Wikipedia article is being fetched.
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML
                                   of the Wikipedia page.
        """

        # Get all content for the div tag with id="mw-content-text".
        # This div contains all text content of the wikipedia page
        all_paragraphs = soup.find("div", id="mw-content-text").find_all('p')

        # Iterate through paragraphs to find the first paragraph with bold text
        for paragraph in all_paragraphs:
            if paragraph.b:
                # Clean the paragraph text by replacing certain characters
                paragraph_cleaned = self.clean_paragraph(paragraph.text.replace("'", '').replace('"', ''))
                # Assign the cleaned paragraph text to the leader's 'bio_first_paragraph' attribute
                leader.bio_first_paragraph = paragraph_cleaned

    def do_scrap(self):
        """
        Scrape Wikipedia data for each country leader, clean the first paragraph, and export to JSON and CSV files.
        """
        # Iterate through each country leader
        for leader in self.country_leaders.leaders_data:
            response = requests.get(leader.wikipedia_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Get the first paragraph from Wikipedia article
            self.get_first_paragraph(leader, soup)

        # Export leaders data to JSON and CSV files
        self.country_leaders.export_to_json()
        self.country_leaders.export_to_csv()
