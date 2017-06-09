import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.url = self.live_server_url
        self.test_page_url = "https://github.com/waqarHocain"

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
        regex = self.url + "/" + r"[\w\d]+"
        self.assertRegexpMatches(page_content, regex)


        # He enters the shortened url into browser address bar, he's
        # redirected to https://github.com/waqarHocain
        shortened_url = re.search(regex, page_content).group()
        self.browser.get(shortened_url)

        self.assertEqual(self.browser.current_url, self.test_page_url)

        # He is satisfied, he now goes to sleep.
        self.browser.quit()

        # A new user, named Jack, hears about the our site from Mastan.
        # He's looking for a way to shorten urls by making calls from his
        # application and get back shortened url in response as JSON.
        # He figures out that if you make a request to `\new` followed by url,
        # you'll get the shortened url. 
        jacks_url = "http://wikipedia.org"

        self.browser = webdriver.Firefox()
        self.browser.get(self.url + "/new/" + jacks_url)

        ## wait for page to load
        sleep(1)

        # He notices along with shortened url, original url is also returned in
        # response.
        page_content = self.browser.find_element_by_tag_name("body").text
        shortened_url = re.search(regex, page_content).group()

        self.assertIn(jacks_url, page_content)
        self.assertIn(shortened_url, page_content)

        # He now wonders if this shortened url will resolve to the original
        # url. He inputs the shortened url into browser address bar.
        self.browser.get(shortened_url)

        # He notices he's redirected the original url.
        self.assertEqual(self.browser.current_url, jacks_url)

