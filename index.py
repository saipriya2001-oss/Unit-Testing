import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse
import unittest
from unittest.mock import patch, MagicMock

class WebCrawler:
    def __init__(self):
        self.index = defaultdict(str)
        self.visited = set()

    def crawl(self, url, base_url=None):
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.index[url] = soup.get_text()

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    full_url = urljoin(base_url or url, href)
                    if full_url.startswith(base_url or url):
                        self.crawl(full_url, base_url=base_url or url)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def search(self, keyword):
        results = []
        for url, text in self.index.items():
            if keyword.lower() in text.lower():
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(f"- {result}")
        else:
            print("No results found.")


def main():
    crawler = WebCrawler()
    start_url = "https://example.com"  # You can change this to a valid URL for real crawling
    crawler.crawl(start_url)

    keyword = "test"
    results = crawler.search(keyword)
    crawler.print_results(results)


# ------------------ UNIT TESTS ------------------ #

class WebCrawlerTests(unittest.TestCase):

    @patch('requests.get')
    def test_crawl_success(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        self.assertIn("https://example.com", crawler.index)
        self.assertIn("https://example.com/about", crawler.visited)

    @patch('requests.get')
    def test_crawl_error(self, mock_get):
        mock_get.side_effect = Exception("Test Error")

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        self.assertIn("https://example.com", crawler.visited)

    def test_search(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This has the keyword"
        crawler.index["page2"] = "Nothing useful here"

        results = crawler.search("keyword")

        self.assertIn("page1", results)
        self.assertNotIn("page2", results)

    def test_print_results(self):
        crawler = WebCrawler()
        with patch("builtins.print") as mock_print:
            crawler.print_results(["https://test.com"])
            mock_print.assert_any_call("Search results:")
            mock_print.assert_any_call("- https://test.com")

        with patch("builtins.print") as mock_print_empty:
            crawler.print_results([])
            mock_print_empty.assert_called_with("No results found.")


# ------------------ RUNNING LOGIC ------------------ #

if __name__ == "__main__":
    # Run unit tests
    print("Running Unit Tests...\n")
    unittest.main(exit=False)

    # Run main program
    print("\nRunning Web Crawler...\n")
    main()
