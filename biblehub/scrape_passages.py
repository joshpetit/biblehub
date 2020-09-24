import re
import requests
from bs4 import BeautifulSoup


def find_passage(reference: str, version='niv'):
    """
    Find multiple verses in a single chapter, or an entire chapter
    :param reference: The reference to find on biblehub
    :param version: The version to return
    :return: A dictionary with a nested dictionary of the verses
    """
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
    print(response)


def parse_str(reference: str) -> dict:
    response = {}
    parsed = re.search('(\\d? ?\\w+) (\\d)(:(\\d)-(\\d))?', reference)
    response['book'] = parsed.group(1).lower()
    response['chapter'] = int(parsed.group(2))
    response['start_verse'] = 1
    response['end_verse'] = -1
    if len(parsed.groups()) == 5:
        response['start_verse'] = int(parsed.group(4))
        response['end_verse'] = int(parsed.group(5))
    return response
