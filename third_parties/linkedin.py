import requests


def scrape_linkedin_profile(linkedin_profile_url: str):
    # Uncomment for real proxycurl api calls
    # header_dict = {'Authorization': f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
    # api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    # response = requests.get(api_endpoint, params={'url': linkedin_profile_url}, headers=header_dict)

    response = requests.get(linkedin_profile_url)

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