import requests
from bs4 import BeautifulSoup


def _query_site(url) -> BeautifulSoup:
    result = requests.get(url)
    return BeautifulSoup(result.content, "lxml")


def search(query: str):
    response = []
    page = _query_site("https://biblehub.net/search.php?q=%s" % query)
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
    print(response)


search("jude")