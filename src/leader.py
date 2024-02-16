import datetime
from typing import Dict


class Leader:
    """
        A class representing a leader.

        Attributes:
            id (int): The ID of the leader.
            first_name (str): The first name of the leader.
            last_name (str): The last name of the leader.
            birth_date (str): The birthdate of the leader.
            death_date (str): The death date of the leader.
            place_of_birth (str): The place of birth of the leader.
            wikipedia_url (str): The Wikipedia URL of the leader.
            start_mandate (str): The start date of the leader's mandate.
            end_mandate (str): The end date of the leader's mandate.
            country (str): The country the leader belongs to.
            bio_first_paragraph (str): The first paragraph of the leader's biography.
        """

    def __init__(self, leader_dict: Dict, country: str = '') -> None:
        """
        Initialize a Leader instance.

        Args:
            leader_dict (Dict): A dictionary containing leader information.
            country (str, optional): The country the leader belongs to. Defaults to ''.
        """
        self.id: str = leader_dict['id']
        self.first_name: str = leader_dict['first_name']
        self.last_name: str = leader_dict['last_name']
        self.birth_date: str = leader_dict['birth_date']
        self.death_date: str = leader_dict['death_date']
        self.place_of_birth: str = leader_dict['place_of_birth']
        self.wikipedia_url: str = leader_dict['wikipedia_url']
        self.start_mandate: str = leader_dict['start_mandate']
        self.end_mandate: str = leader_dict['end_mandate']
        self.country: str = country
        self.bio_first_paragraph: str = ''

    def __str__(self):
        """
        Get a string representation of the leader.

        Returns:
            str: A string representation of the leader.
        """
        return (
            f"{self.first_name} {self.last_name if self.last_name != 'None' else ''} president of "
            f"{self.country.upper()} from {self.start_mandate} to "
            f"{self.end_mandate if self.end_mandate else datetime.date.today()}")

    def to_json(self) -> dict:
        """
        Convert the leader object to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary representation of the leader.
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'death_date': self.death_date,
            'place_of_birth': self.place_of_birth,
            'wikipedia_url': self.wikipedia_url,
            'start_mandate': self.start_mandate,
            'end_mandate': self.end_mandate,
            'country': self.country,
            'bio_first_paragraph': self.bio_first_paragraph
        }
