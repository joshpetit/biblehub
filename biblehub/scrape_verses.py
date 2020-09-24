#!/usr/bin/python3.8

import requests
from bs4 import BeautifulSoup

from biblehub import styling


class BibleHubQuery:
    """A Biblehub.com query, contains a passage with the text and the version.
    Can optionally contain Treasury of Scriptures(tsks), cross references(crfs) and lexicons
    Use the \"query\" function to create these objects. """

    def __init__(self, passage: str, text: str, version: str, crfs: list = None, tsks: list = None,
                 lexicons: list = None):
        if lexicons is None:
            lexicons = []
        if tsks is None:
            tsks = []
        if crfs is None:
            crfs = []
        self.passage = passage
        self.text = text
        self.version = version
        self.crfs = crfs
        self.tsks = tsks
        self.lexicons = lexicons
        self._init_info()

    def _init_info(self) -> None:
        response = self.format_verse()
        if self.crfs:
            response += "{header}{crfs}".format(header=styling.format_header("Cross References"),
                                                crfs=self.format_crfs())
        if self.tsks:
            response += "{header}{tsks}".format(header=styling.format_header("Treasury Of Scripture"),
                                                tsks=self.format_tsks())
        if self.lexicons:
            response += "{header}{lexicon}".format(header=styling.format_header("Lexicon"),
                                                   lexicon=self.format_lexicons())
        self.info = response

    def __str__(self) -> str:
        return self.info

    def format_crfs(self) -> str:
        response = ''
        for crf in self.crfs:
            response += styling.format_verse(crf['reference'], crf['text'])
        return response

    def format_tsks(self) -> str:
        response = []
        for tsk in self.tsks:
            response.append(tsk)
        return '\n'.join(response) + '\n'

    def format_verse(self) -> str:
        return styling.format_verse('{reference} ({version})'.format(reference=self.passage, version=self.version),
                                    self.text)

    def format_lexicons(self) -> str:
        response = []
        for lexicon in self.lexicons:
            response.append(lexicon.__str__())
        return '\n\n'.join(response)


class _Lexicon:
    def __init__(self, text, lang, translit, parse, strong, definition):
        self.text = text
        self.lang = lang
        self.translit = translit
        self.parse = parse
        self.strong = strong
        self.definition = definition

    def __str__(self):
        return """\
%s
%s %s
%s
%s %s """ % (self.text, self.lang, self.translit, self.parse, self.strong, self.definition)


def _query_site(url) -> BeautifulSoup.find:
    result = requests.get(url)
    return BeautifulSoup(result.content, "lxml")


def _format_query(text) -> str:
    if isinstance(text, str):
        arr = text.split(sep=" ")
    else:
        arr = text
    if len(arr) == 3:
        book = arr[0].lower() + "_" + arr[1].lower()
        index = 2
    elif len(arr) == 2:
        book = arr[0].lower()
        index = 1
    else:
        raise ValueError("Invalid Query")
    verses = arr[index].split(sep=":")
    return "https://biblehub.com/%s/%s-%s.htm" % (book, verses[0], verses[1])


def _get_crfs(whole) -> list:
    response = []
    crf_section = whole.find("div", {"id": "crf"})
    crfs_list = crf_section.find_all("span", {"class": "crossverse"})
    text = crf_section.get_text()
    assert isinstance(text, str)
    crfs = []
    for crf in crfs_list:
        crfs.append(crf.get_text())
    # May Create edge cases, look for a better way sometime
    for i in range(len(crfs)):
        begin = text.find(crfs[i]) + len(crfs[i])
        if i < len(crfs) - 1:
            end = text.find(crfs[i + 1])
        else:
            end = len(text)
        response.append({"reference": crfs[i], "text": text[begin:end]})
    return response


def _get_lexicon(page) -> list:
    lexicon = page.find("div", {"id": "combox"}).find("div")
    words = lexicon.find_all("span", {"class": "word"})
    lexicons = []
    for word in words:
        lexicons.append(_Lexicon(word.get_text().strip(),
                                 word.find_next("span", class_=['heb', 'grk']).get_text().strip("\n"),
                                 word.find_next("span", {"class": "translit"}).get_text().strip("\n"),
                                 word.find_next("span", {"class": "parse"}).get_text().strip("\n"),
                                 word.find_next("span", {"class": "str"}).get_text().strip("\n"),
                                 word.find_next("span", {"class": "str2"}).get_text().strip("\n")
                                 ))
    return lexicons


def _get_tsks(page) -> list:
    tsks_list = page.find_all("p", {"class": "tskverse"})
    tsks = []
    for tsk in tsks_list:
        tsks.append(tsk.get_text())
    return tsks


def _find_version(whole, ver) -> BeautifulSoup:
    versions = whole.find_all_next("span", "versiontext")
    for version in versions:
        if version.a.attrs['href'].startswith(ver):
            return version
    return versions[0]


def _get_passage(whole, version) -> str:
    version_formatted = "/%s/" % version.lower()
    first = _find_version(whole, version_formatted)
    second = first.find_next_sibling("span", {"class": "versiontext"})
    beg = first.get_text()
    block = whole.get_text()
    if second is None:
        verse = block[str.find(block, beg) + len(beg):]
    else:
        end = second.get_text()
        verse = block[str.find(block, beg) + len(beg): str.find(block, end)]
    return verse


def find_verse(reference: str, version="niv", get_tsks=True, get_crfs=True, get_lexicons=True) -> BibleHubQuery:
    """Returns up to **one** verse along with the information provided by Biblehub

    :param reference: The reference to be parsed (i.e Genesis 1:1)
    :param version: The abbreviation of the version to be parsed (i.e esv or niv), defaults to niv
    :param get_tsks: Whether to fetch the Treasury of Scripture(tsk) (Contains references and texts), defaults to True
    :param get_crfs: Whether to fetch cross references (Only contains reference), defaults to True
    :param get_lexicons: Whether to fetch the lexicons, defaults to True

    :return: A BibleHubQuery
    :rtype: BibleHubScrapper.BibleHubQuery
    """
    url = _format_query(reference)
    page = _query_site(url)
    whole = page.find("div", {"id": "par"})
    verse = _get_passage(whole, version)
    lexicons = None
    if get_lexicons:
        lexicons = _get_lexicon(page)
    tsks = None
    if get_tsks:
        tsks = _get_tsks(page)
    crfs = None
    if get_crfs:
        crfs = _get_crfs(page)
    hub_query = BibleHubQuery(reference.title(), verse, version.upper(), crfs, tsks, lexicons)
    return hub_query


def get_versions(reference: str, recolor=True) -> list:
    """ Returns all the versions for a particular verse

   :param reference: The passage to look for
   :param recolor: Whether to color the verses (soon to be deprecated)

   :return A list of all the versions
   :rtype: list
    """
    response = []
    url = _format_query(reference)
    page = _query_site(url)
    whole = page.find("div", {"id": "par"})
    versions = whole.find_all_next("span", "versiontext")
    for version in versions:
        version = version.a.attrs['href'][1:4]
        passage = _get_passage(whole, version)
        version = version.upper()
        if recolor:
            version = styling.format_reference(version)
            reference = styling.format_header(reference).strip()
        response.append({"version": version, "passage": passage, "reference": reference})
    return response
