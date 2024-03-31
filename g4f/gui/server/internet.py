from __future__ import annotations  # Allows using class names in annotations

import asyncio
from aiohttp import ClientSession, ClientTimeout
from ...errors import MissingRequirementsError  # Custom error for missing requirements

try:
    from duckduckgo_search import DDGS  # Web search module
    from bs4 import BeautifulSoup  # HTML parsing module
    has_requirements = True  # Flag for having required modules
except ImportError:
    has_requirements = False

class SearchResults:
    def __init__(self, results: list):
        """
        Initialize SearchResults class with a list of SearchResultEntry objects.
        """
        self.results = results

    def __iter__(self):
        """
        Allow iteration over SearchResults object.
        """
        yield from self.results

    def __str__(self):
        """
        Generate a string representation of SearchResults object.
        """
        search = ""
        for idx, result in enumerate(self.results):
            if search:
                search += "\n\n\n"
            search += f"Title: {result.title}\n\n"
            if result.text:
                search += result.text
            else:
                search += result.snippet
            search += f"\n\nSource: [[{idx}]]({result.url})"
        return search

class SearchResultEntry:
    def __init__(self, title: str, url: str, snippet: str, text: str = None):
        """
        Initialize SearchResultEntry class with title, url, snippet, and optional text.
        """
        self.title = title
        self.url = url
        self.snippet = snippet
        self.text = text

    def set_text(self, text: str):
        """
        Set the text attribute of SearchResultEntry class.
        """
        self.text = text

def scrape_text(html: str, max_words: int = None) -> str:
    """
    Scrape text from the given HTML string with a maximum word count.
    """
    soup = BeautifulSoup(html, "html.parser")
    # Remove script and style elements
    for exclude in soup(["script", "style"]):
        exclude.extract()
    # Select main content elements
    for selector in [
            "main",
            ".main-content-wrapper",
            ".main-content",
            ".emt-container-inner",
            ".content-wrapper",
            "#content",
            "#mainContent",
        ]:
        select = soup.select_one(selector)
        if select:
            soup = select
            break
    # Remove specific elements for zdnet.com
    for remove in [".c-globalDisclosure"]:
        select = soup.select_one(remove)
        if select:
            select.extract()
    clean_text = ""
    for paragraph in soup.select("p"):
        text = paragraph.get_text()
        for line in text.splitlines():
            words = []
            for word in line.replace("\t", " ").split(" "):
                if word:
                    words.append(word)
            count = len(words)
            if not count:
                continue
            if max_words:
                max_words -= count
                if max_words <= 0:
                    break
            if clean_text:
                clean_text += "\n"
            clean_text += " ".join(words)

    return clean_text

async def fetch_and_scrape(session: ClientSession, url: str, max_words: int = None) -> str:
    """
    Fetch the webpage content and scrape text with a maximum word count.
    """
    try:
        async with session.get(url) as response:
            if response.status == 200:
              `enter code here`                html = await response.text()
                return scrape_text(html, max_words)
    except Exception:
        return

async def search(query: str, n_results: int = 5, max_words: int = 2500, add_text: bool = True) -> SearchResults:
    """
    Search the web and return search results with optional text.
    """
    if not has_requirements:
        raise MissingRequirementsError('Install "duckduckgo-search" and "beautifulsoup4" package')
    with DDGS() as ddgs:
        results = []
        for result in ddgs.text(
                query,
                region="wt-wt",
                safesearch="moderate",
                timelimit="y",
            ):
            results.append(SearchResultEntry(
                result["title"],
                result["href"],
                result["body"]
            ))
            if len(results) >= n_results:
                break

        if add_text:
            requests = []
            async with ClientSession(timeout=ClientTimeout(5)) as session:
                for entry in results:
                    requests.append(fetch_and_scrape(session, entry.url, int(max_words / (n_results - 1))))
                texts = await asyncio.gather(*requests)

        formatted_results = []
        left_words = max_words
        for i, entry in enumerate(results):
            if add_text:
                entry.text = texts[i]
            if left_words:
                left_words -= entry.title.count(" ") + 5
                if entry.text:
                    left_words -= entry.text.count(" ")
                else:
                    left_words -= entry.snippet.count(" ")
                if 0 > left_words:
                    break
            formatted_results.append(entry)

        return SearchResults(formatted_results)

def get_search_message(prompt) -> str:
    """
    Generate a search message based on the user's prompt and search results.
    """
    try:
        search_results = asyncio.run(search(prompt))
        message = f"""
