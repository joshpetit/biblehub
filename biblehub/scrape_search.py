import requests
from bs4 import BeautifulSoup


def search(query: str):
    response = []
    request = requests.get("https://biblehub.net/search.php?q=%s" % query)
    page = BeautifulSoup(request.content, "lxml")
    whole = page.find("div", {"id": "leftbox"}).find_next("div").find_next("div")
    results = whole.find_all("p", {"class": "g"})
    for result in results:
        string = result.a.span.get_text()
        index = string.find(":")
        end = string.find(" ", index)
        if index == -1 or end == -1:
            continue
        reference = string[0:end]
        bshort = string[end:].lstrip()

        string = result.find_next_sibling().get_text()
        end = string.find("//biblehub.com")
        excerpt = string[0:end].strip().replace("\n", "").replace("                    ", "")
        response.append({"reference": reference, "preview": bshort, "excerpt": excerpt})
    return response


