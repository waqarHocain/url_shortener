from django.conf.urls import url

from url_shrtnr import views

urlpatterns = [
    url(r"^$", views.homepage, name="homepage"),
    url(r"^(?P<id>[\w\d]+)/$", views.mapper, name="mapper"),
    url(r"^new/(?P<url>.+)/", views.create_url, name="create_url"),
]
