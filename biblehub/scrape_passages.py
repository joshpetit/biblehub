import requests
from bs4 import BeautifulSoup
from biblehub.scrape_utils import parse_str


# TODO: Optimize with obj parameter
def find_passage(reference: str, version='niv') -> dict:
    """
    Find multiple verses in a single chapter, or an entire chapter
    :param reference: The reference to find on biblehub
    :param version: The version to return
    :return: A dictionary with a nested dictionary of the verses
    """
    version = version.lower()
    response = {'verses': {}, 'reference': reference.title()}
    reference = parse_str(reference)
    response['bnc'] = reference['book'].title() + ' ' + str(reference['chapter'])
    url = 'https://biblehub.com/%s/%s/%d.htm' % (version, reference['book'].replace(" ", "_"), reference['chapter'])
    request = requests.get(url)
    page = BeautifulSoup(request.content, "lxml")
    chap = page.find("div", {"class": "chap"})
    verses = chap.find_all("span", {"class": "reftext"})
    if reference['end_verse'] != -1:
        verses = verses[reference['start_verse'] - 1:]
        verses = verses[0: reference['end_verse'] - reference['start_verse'] + 1]
    for verse in verses:
        num = int(verse.get_text())
        verse = verse.next_sibling.strip()
        response['verses'][num] = verse
    return response
