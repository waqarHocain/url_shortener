import unittest

from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_can_shorten_a_url(self):
        # Mastan has heard about a new cool url-shortner. He check outs
        # its homepage
        self.browser.get("http://localhost:8000/")

        # He notices Shrtnr in browser title and header
        self.assertIn("Shrtnr", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("Shrtnr", header_text)


if __name__ == "__main__":
    unittest.main()
