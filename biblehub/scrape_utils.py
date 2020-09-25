import re


def parse_str(reference: str) -> dict:
    response = {}
    parsed = re.search('(\\d? ?\\w+) (\\d)(:(\\d+)-(\\d+))?', reference)
    response['book'] = parsed.group(1).lower()
    response['chapter'] = int(parsed.group(2))
    response['start_verse'] = 1
    response['end_verse'] = -1
    if len(parsed.groups()) == 5 and parsed.group(4) is not None and parsed.group(5) is not None:
        response['start_verse'] = int(parsed.group(4))
        response['end_verse'] = int(parsed.group(5))
    return response
