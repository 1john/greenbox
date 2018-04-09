"""gbb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import views
from showcase import views as showcaseviews
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^contact_us/$', views.contact_us, name="contact_us"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^auth/$', views.auth_view, name="auth"),
    #url(r'^services/$', views.services, name="services"),
    #showcase
    url(r'^team/$', showcaseviews.team, name="team"),
    url(r'^item/$', showcaseviews.item, name="item"),
    url(r'^item/(?P<item_id>[-\w]+)/$', showcaseviews.item, name="item"),
    url(r'^sign_s3_put/$', showcaseviews.sign_s3_put, name="sign_s3_put"),
    url(r'^delete/(?P<item_id>[-\w]+)/$', showcaseviews.delete, name="delete"),
    url(r'^dashboard/$', showcaseviews.dashboard, name="dashboard"),
    
    #sites
    url(r'^sites/(?P<site_name>[-\w]+)/$', views.sites, name="sites"),
    url(r'^showcase/$', views.showcase, name="showcase"),
    url(r'^showcase/(?P<site_name>[-\w]+)/$', views.showcase, name="showcase"),
    url(r'^about/$', views.about, name="about"),
    url(r'^about/(?P<site_name>[-\w]+)/$', views.about, name="about"),
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^contact/(?P<site_name>[-\w]+)/$', views.contact, name="contact"),

    #admin
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #serving static files for development
