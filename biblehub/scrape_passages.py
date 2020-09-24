import re


def find_passage(reference: str, version='niv'):
    parsed = parse_str(reference)
    url = 'https://biblehub.com/%s/%s/%s.htm' % (version, parsed['book'], parsed['chapter'])
    print(url)


def parse_str(reference: str) -> dict:
    response = {}
    parsed = re.search('(\d? ?\w+) (\d):(\d)-(\d)', reference)
    response['book'] = parsed.group(1).replace(' ', '_').lower()
    response['chapter'] = parsed.group(2)
    if parsed.groups() == 4:
        response['start_verse'] = parsed.group(3)
        response['end_verse'] = parsed.group(4)
    return response

# verse[0:verse.index(thing.group(1)) -1]
find_passage('1 Corinthians 3:4-5')
