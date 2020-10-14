import re


def parse_str(reference: str) -> dict:
    response = {}
    parsed = re.search('([1-3]?[^\\s]+[A-Za-z ]+[^\\d ]) ?(\\d+)?:?(\\d+)?-?(\\d+)?', reference)
    response['book'] = parsed.group(1).lower()
    response['chapter'] = int(parsed.group(2))
    response['start_verse'] = 1
    response['end_verse'] = None
    if parsed.group(3) is not None:
        response['start_verse'] = int(parsed.group(3))
    if parsed.group(4) is not None:
        response['end_verse'] = int(parsed.group(4))
    return response

