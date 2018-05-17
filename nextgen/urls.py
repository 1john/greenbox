from django.conf.urls import url
from views import greenhouseview

urlpatterns = [
	url(r'^greenhouses/(?P<site_name>[-\w]+)/$', greenhouseview, name="greenhouses"),
	url(r'^greenhouses/', greenhouseview, name="greenhouses"),
]