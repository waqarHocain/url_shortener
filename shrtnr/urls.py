from django.conf.urls import url

from url_shrtnr import views

urlpatterns = [
    url(r"^$", views.homepage, name="homepage"),
    url(r"^(?P<id>\d+)/$", views.mapper, name="mapper"),
]
