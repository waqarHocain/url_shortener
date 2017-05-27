from django.shortcuts import render


def homepage(request):
    return render(request, "url_shrtnr/index.html")