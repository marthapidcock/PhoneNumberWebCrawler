from collections import defaultdict
from html.parser import HTMLParser
from modulefinder import AddPackagePath
from urllib.request import urlopen
from urllib.parse import urljoin, urlparse
from urllib.error import HTTPError
from http.client import InvalidURL
from ssl import _create_unverified_context
from pprint import pprint
import re

# Parser for achor tags to extract page links from a base URL
class Parser(HTMLParser):
    def __init__(self, baseURL = ""):
        HTMLParser.__init__(self)
        self.pageLinks = set()
        self.phoneNumbers = set()
        self.baseURL = baseURL
    
    def getLinks(self):
        return self.pageLinks
    
    def getPhoneNumbers(self):
        return self.phoneNumbers
    
    # Parse http/https hrefs from anchor tags
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attribute, value in attrs:
                if attribute.lower() == "href":
                    absoluteUrl = urljoin(self.baseURL, value)
                    if urlparse(absoluteUrl).scheme in ["http", "https"]:
                        self.pageLinks.add(absoluteUrl)
    
    # Parse numbers from data using very basic regex
    def handle_data(self, data):
        phone_number = re.findall("([0-9]{3}[- ][0-9]{3}[- ][0-9]{4})+", data)
        return self.phoneNumbers.update(phone_number)


class MyWebCrawler(object):
    def __init__(self, url, maxCrawl=10):
        self.visited = set()
        self.starterUrl = url
        self.max = maxCrawl
        self.phoneNumbers = set()
        self.countPerDomain = defaultdict(int)
    
    def getVisited(self):
        return self.visited
    
    def getPhoneNumbers(self):
        return self.phoneNumbers
    
    def getCountPerDomain(self):
        return self.countPerDomain
    
    def addPhoneNumbers(self, numbers):
        self.phoneNumbers.update(numbers)

    def parse(self, url):
        try:
            htmlContent = urlopen(url, context=_create_unverified_context()).read().decode()
            parser = Parser(url)
            parser.feed(htmlContent)
            self.addPhoneNumbers(parser.getPhoneNumbers())
            domain = urlparse(url).netloc
            self.countPerDomain[domain] += len(parser.getPhoneNumbers())

            return parser.getLinks()
        except (HTTPError, InvalidURL, UnicodeDecodeError):
            print(f"FAILED: {url}")
            return set()

    def crawl(self):
        urlsToParse = {self.starterUrl}
        while(len(urlsToParse) > 0 and len(self.visited) < self.max):
            nextUrl = urlsToParse.pop()
            if nextUrl not in self.visited:
                self.visited.add(nextUrl)
                urlsToParse |= self.parse(nextUrl)


if __name__ == "__main__":
    # Change the starting URL below, can also limit the pages to crawl
    crawler = MyWebCrawler("https://therecount.github.io/interview-materials/project-a/1.html", maxCrawl=20)
    crawler.crawl()
    print("\nVisited sites:")
    print(*crawler.getVisited(), sep="\n")
    print("\nPhone numbers collected:")
    print(*crawler.getPhoneNumbers(), sep="\n")
    print("\nCount of numbers per domain:")
    pprint(dict(crawler.getCountPerDomain()))