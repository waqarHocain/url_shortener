from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.http.response import Http404
from django.shortcuts import render, redirect

from .models import Url
from .base62 import ShortenUrl
from .utils import check_trailing_slash


def homepage(request):
    if request.method == "POST":
        try:
            url = Url.objects.get(full_url = request.POST["input_url"])
        except Url.DoesNotExist:
            url = None

        if url:
            # url is already saved
            context = {
                "full_url": url.full_url,
                "shortened_url": url.shortened_url
            }
            return JsonResponse(context)

        # url is not saved, check if it is a valid url
        try:
            URLValidator()(request.POST["input_url"])
        except ValidationError:
            return JsonResponse({
                "error": "Invalid url"
            })

        # url is not saved and it is a valid url, save it
        shrtnr = ShortenUrl()

        domain_name = check_trailing_slash(request.build_absolute_uri())

        url = Url.objects.create(full_url=request.POST["input_url"])
        url.shortened_url = domain_name + shrtnr.encode(url.id)
        url.save()

        context = {
            "full_url": url.full_url,
            "shortened_url": url.shortened_url
        }
        return JsonResponse(context)
    return render(request, "url_shrtnr/index.html")


def create_url(request, url):
    # check if it is a valid url
    try:
        URLValidator()(url)
    except ValidationError:
        return JsonResponse({
            "error": "Invalid url"
        })

    # it is a valid url, save it
    _url = Url.objects.create(full_url = url)

    shrtnr = ShortenUrl()
    domain_name = check_trailing_slash(request.build_absolute_uri("/"))
    _url.shortened_url = domain_name + shrtnr.encode(_url.id) 
    _url.save()

    context = {
        "full_url": _url.full_url,
        "shortened_url": _url.shortened_url
    }

    return JsonResponse(context)


def mapper(request, id):
    shrtnr = ShortenUrl()
    id = shrtnr.decode(id)
    try:
        url = Url.objects.get(id = int(id))
    except Url.DoesNotExist:
        raise Http404 
    
    full_url = url.full_url

    return redirect(full_url)

