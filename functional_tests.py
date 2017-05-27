import unittest

from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_shorten_a_url(self):
        # Mastan has heard about a new cool url-shortner. He check outs
        # its homepage
        self.browser.get("http://localhost:8000/")

        # He notices Shrtnr in browser title and header
        self.assertIn("Shrtnr", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("Shrtnr", header_text)

        # He is invited to enter url
        input_box = self.browser.find_element_by_class_name("input_url")
        self.assertEqual(input_box.get_attribute("placeholder"),
                            "Enter your url here..")
        # He enters https://www.github.com/waqarHocain in input box and press
        # enter

        # A JSON object is returned in response containing actual url
        # https://www.github.com/waqarHocain and shortened url with
        # <current_page_url>/1

        # He enters the <current_page_url>/1 into browser address bar, he's
        # redirected to https://github.com/waqarHocain



if __name__ == "__main__":
    unittest.main()
