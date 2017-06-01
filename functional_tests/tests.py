import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.url = "http://localhost:8000/"
        self.test_page_url = "https://www.github.com/waqarHocain"

    def tearDown(self):
        self.browser.quit()

    def test_can_shorten_a_url(self):
        # Mastan has heard about a new cool url-shortner. He check outs
        # its homepage
        self.browser.get(self.url)

        # He notices Shrtnr in browser title and header
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("Shrtnr", self.browser.title)
        self.assertIn("Shrtnr", header_text)

        # He is invited to enter url
        input_box = self.browser.find_element_by_class_name("input_url")
        self.assertEqual(input_box.get_attribute("placeholder"),
                         "Enter your url here..")

        # He enters https://www.github.com/waqarHocain in input box and press
        # enter
        input_box.send_keys(self.test_page_url)
        input_box.send_keys(Keys.ENTER)

        # A JSON object is returned in response containing actual url
        # https://www.github.com/waqarHocain and shortened url with
        # <current_page_url>/1

        ## wait 1 second for page to load
        sleep(1)

        page_content = self.browser.find_element_by_tag_name("body").text

        self.assertIn(self.test_page_url, page_content)
        self.assertRegexpMatches(page_content, self.url + "\d+")


        # He enters the <current_page_url>/1 into browser address bar, he's
        # redirected to https://github.com/waqarHocain
        self.browser.get(self.url + "1")

        self.assertEqual(self.browser.current_url, self.test_page_url)

