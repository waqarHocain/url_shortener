from django.core.urlresolvers import resolve
from django.http import HttpRequest 
from django.template.loader import render_to_string
from django.test import TestCase

from .views import homepage


class HomepageTest(TestCase):

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve("/")
        self.assertEqual(found.func, homepage)

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        response = homepage(request)

        expected_html = render_to_string("url_shrtnr/index.html")

        self.assertEqual(response.content.decode(), expected_html)
