import json
from django.http import JsonResponse
from django.shortcuts import render

from .models import Url


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

        # url is not saved
        url = Url.objects.create(full_url=request.POST["input_url"])
        url.shortened_url = "http://localhost:8000/" + str(url.id)
        url.save()

        context = {
            "full_url": url.full_url,
            "shortened_url": url.shortened_url
        }
        return JsonResponse(context)
    return render(request, "url_shrtnr/index.html")
