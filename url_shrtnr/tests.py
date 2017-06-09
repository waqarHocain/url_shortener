from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.test import TestCase

from .views import homepage, mapper, create_url
from .base62 import ShortenUrl
from .models import Url


class HomepageTest(TestCase):

    def setUp(self):
        self.test_url = "https://www.github.com/waqarHocain"
        self.fake_meta = {
            'SERVER_NAME':'127.0.0.1',
            'HTTP_HOST':'127.0.0.1',
            'SERVER_PORT': 8000
        }

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve("/")
        self.assertEqual(found.func, homepage)

    def test_homepage_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "url_shrtnr/index.html")

    def test_homepage_can_save_a_POST_request(self):
        request = HttpRequest()
        request.META = self.fake_meta
        request.method = "POST"
        request.POST["input_url"] = self.test_url 

        response = homepage(request)

        self.assertEqual(Url.objects.count(), 1)

        new_url = Url.objects.first()
        self.assertEqual(self.test_url, new_url.full_url)

        self.assertIn(self.test_url, response.content.decode())

    def test_shortened_url_is_saved_with_base62_encoded_id(self):
        request = HttpRequest()
        request.META = self.fake_meta
        request.method = "POST"
        request.POST["input_url"] = "https://www.twitter.com/waqarHocain"
        response1 = homepage(request)

        shrtnr = ShortenUrl()

        domain_name = request.build_absolute_uri() + "/"

        first_saved_url = Url.objects.first()
        base62_str1 = shrtnr.encode(first_saved_url.id)
        expected_shortened_url_1 = domain_name + base62_str1
        self.assertIn(expected_shortened_url_1, response1.content)


        request2 = HttpRequest()
        request2.META = self.fake_meta
        request2.POST["input_url"] = self.test_url
        response2 = homepage(request)

        second_saved_url = Url.objects.first()
        base62_str2 = shrtnr.encode(second_saved_url.id)
        expected_shortened_url_2 = domain_name + base62_str2

        self.assertIn(expected_shortened_url_2, response2.content)


    def test_for_an_already_saved_url_no_new_instance_is_saved(self):
        request = HttpRequest()
        request.META = self.fake_meta
        request.method = "POST"
        request.POST["input_url"] = self.test_url

        res1 = homepage(request)

        # generate shortened url
        url = Url.objects.first()
        shrtnr = ShortenUrl()
        domain_name = request.build_absolute_uri() + "/"
        shortened_url = domain_name + shrtnr.encode(url.id)

        self.assertEqual(Url.objects.count(), 1)
        self.assertIn(self.test_url, res1.content)
        self.assertIn(shortened_url, res1.content)

        request.POST["input_url"] = self.test_url
        res2 = homepage(request)

        self.assertEqual(Url.objects.count(), 1)
        self.assertIn(self.test_url, res2.content)
        self.assertIn(shortened_url, res2.content)


class MapperTest(TestCase):
    
    def setUp(self):
        self.test_url = "https://www.github.com/waqarHocain"

    def test_url_with_id_is_resolved_to_mapper(self):
        found = resolve("/1/")
        self.assertEqual(found.func, mapper)

    def test_redirects_to_correct_url_for_a_given_id(self):
        shrtnr = ShortenUrl()
        url = Url()
        url.id = 13
        url.full_url = self.test_url
        url.save()
        url.shortened_url = "http://localhost:8000/" + shrtnr.encode(url.id)
        url.save()

        id = shrtnr.encode(url.id)
        request = HttpRequest()
        response = mapper(request, id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], url.full_url)

    def test_404_page_is_returned_for_a_not_saved_url(self):
        id = 1
        request = HttpRequest()

        self.assertRaises(mapper, args=(request, id))

        #self.assertEqual(response.status_code, 404)


class CreateUrlTest(TestCase):

    def setUp(self):
        self.test_url = "https://www.github.com/waqarHocain"
        self.fake_meta = {
            'SERVER_NAME':'127.0.0.1',
            'HTTP_HOST':'127.0.0.1',
            'SERVER_PORT': 8000
        }

    def test_requests_to_new_resolves_to_create_url(self):
        found = resolve("/new/http://somerandomdude.me")
        self.assertEqual(found.func, create_url)

    def test_it_can_create_a_new_url_when_passed_a_url_as_parameter(self):
        request = HttpRequest()
        request.META = self.fake_meta
        request.GET = "/new/"
        url = self.test_url
        response = create_url(request, url)

        self.assertEqual(Url.objects.count(), 1)

    def test_returns_shortened_url_in_response_along_with_original_url(self):
        request = HttpRequest()
        request.META = self.fake_meta
        request.GET = "/new/"
        url = self.test_url
        response = create_url(request, url)

        saved_url = Url.objects.first()

        shrtnr = ShortenUrl()
        domain_name = request.build_absolute_uri() + "/"
        shortened_url = domain_name + shrtnr.encode(saved_url.id)

        self.assertIn(url, response.content)
        self.assertIn(shortened_url, response.content)


class ShortenUrlTest(TestCase):

    def test_it_can_convert_an_int_to_base62_str(self):
        int_1 = 987
        int_2 = 1
        int_3 = 76589
        expected_str_1 = "Fv"
        expected_str_2 = "1"
        expected_str_3 = "JvJ"

        shortener = ShortenUrl()

        self.assertEqual(shortener.encode(int_1), expected_str_1)
        self.assertEqual(shortener.encode(int_2), expected_str_2)
        self.assertEqual(shortener.encode(int_3), expected_str_3)

    def test_it_can_convert_from_base62_str_to_base10_int(self):
        str_1 = "Jjf"
        str_2 = "Blo"
        str_3 = "Awesme"
        expected_int_1 = 75867
        expected_int_2 = 45248 
        expected_int_3 = 10028099520 

        shortener = ShortenUrl()

        self.assertEqual(shortener.decode(str_1), expected_int_1)
        self.assertEqual(shortener.decode(str_2), expected_int_2)
        self.assertEqual(shortener.decode(str_3), expected_int_3)


class UrlModelTest(TestCase):

    def setUp(self):
        self.test_url = "https://www.github.com/waqarHocain"

    def test_saving_and_retrieving_urls(self):
        first_url = Url()
        first_url.full_url = self.test_url
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
        self.assertEqual(first_saved_url.full_url, self.test_url)
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

