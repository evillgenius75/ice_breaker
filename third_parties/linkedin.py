import os

import requests


def scrape_linkedin_profile(linkedin_profile_url: str):
    """
    Scrapes a LinkedIn profile and returns a dictionary of the profile's data.

    Args:
        linkedin_profile_url (str): The URL of the LinkedIn profile to scrape.

    Returns:
        dict: A dictionary of the profile's data.
    """
    header_dict = {'Authorization': f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    if os.environ.get("ENVIRONMENT") == "prod" or os.environ.get("ENVIRONMENT") == "dev":
        response = requests.get(api_endpoint, params={'url': linkedin_profile_url}, headers=header_dict)
        data = response.json()
        data = {
            k: v
            for k, v in data.items()
            if v not in ([], "", "", None)
               and k not in ["people_also_viewed", "certifications"]
        }
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url")

        return data
    elif os.environ.get("ENVIRONMENT") == "test" or os.environ.get("Environment") is None:
        response = requests.get("https://gist.githubusercontent.com/evillgenius75/a4afe97f0f8a233b5ee738167a5fefa5/raw"
                                "/7028b8eef25dce9887440d21dc743afb7466af1d/linkedin.json")
        data = response.json()
        data = {
            k: v
            for k, v in data.items()
            if v not in ([], "", "", None)
               and k not in ["people_also_viewed", "certifications"]
        }
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url")

        return data
