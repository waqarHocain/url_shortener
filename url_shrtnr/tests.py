from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

from .views import homepage
from .models import Url


class HomepageTest(TestCase):

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve("/")
        self.assertEqual(found.func, homepage)

    def test_homepage_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "url_shrtnr/index.html")

    def test_homepage_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST["input_url"] = "https://www.github.com/waqarHocain"

        response = homepage(request)

        self.assertEqual(Url.objects.count(), 1)

        new_url = Url.objects.first()
        self.assertEqual("https://www.github.com/waqarHocain",
                         new_url.full_url)

        self.assertIn("https://www.github.com/waqarHocain",
                      response.content.decode())

    def test_for_an_already_saved_url_no_new_instance_is_saved(self):
        request = HttpRequest()
        request.method = "POST"
        
        request.POST["input_url"] = "https://www.github.com/waqarHocain"
        res1 = homepage(request)

        shortened_url = "http://localhost:8000/1"

        self.assertEqual(Url.objects.count(), 1)
        self.assertIn("https://www.github.com/waqarHocain", res1.content)
        self.assertIn(shortened_url, res1.content)

        request.POST["input_url"] = "https://www.github.com/waqarHocain"
        res2 = homepage(request)

        self.assertEqual(Url.objects.count(), 1)
        self.assertIn("https://www.github.com/waqarHocain", res2.content)
        self.assertIn(shortened_url, res2.content)


class UrlModelTest(TestCase):

    def test_saving_and_retrieving_urls(self):
        first_url = Url()
        first_url.full_url = "https://www.github.com/waqarHocain"
        first_url.save()
        first_url.shortened_url = "http://localhost:8000/" + str(first_url.id)
        first_url.save()

        second_url = Url()
        second_url.full_url = "https://www.twitter.com/waqarHocain"
        second_url.save()
        second_url.shortened_url = "http://localhost:8000/" + \
                                   str(second_url.id)
        second_url.save()

        saved_urls = Url.objects.all()
        self.assertEqual(saved_urls.count(), 2)

        first_saved_url = saved_urls[0]
        second_saved_url = saved_urls[1]
        self.assertEqual(first_saved_url.full_url,
                         "https://www.github.com/waqarHocain")
        self.assertEqual(first_saved_url.shortened_url,
                         "http://localhost:8000/1")
        self.assertEqual(second_saved_url.full_url,
                         "https://www.twitter.com/waqarHocain")
        self.assertEqual(second_saved_url.shortened_url,
                         "http://localhost:8000/2")

    def test_dont_save_a_url_if_it_is_already_saved(self):
        first_url = Url()
        first_url.full_url = "https://www.github.com/waqarHocain"
        first_url.save()
        first_url.shortened_url = "http://localhost:8000/" + str(first_url.id)
        first_url.save()

        second_url = Url()
        second_url.full_url = "https://www.github.com/waqarHocain"
        
        self.assertRaises(second_url.save)

        saved_urls = Url.objects.all()

        self.assertEqual(saved_urls.count(), 1)
        self.assertEqual(saved_urls[0].full_url, first_url.full_url)

