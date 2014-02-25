from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django_to_id import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iD_django.views.home', name='home'),
    # url(r'^iD_django/', include('iD_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^api/0.6/node/(?P<id>.+)', views.NodeViewSet.as_view()),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
