from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from osm_api import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iD_django.views.home', name='home'),
    # url(r'^iD_django/', include('iD_django.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^api/0.6/node/(?P<id>.+)', views.NodeViewSet.as_view()),
    url(r'^api/0.6/node/$', views.NodeViewSetList.as_view()),

    url(r'^api/0.6/way/(?P<id>.+)', views.WayViewSet.as_view()),
    url(r'^api/0.6/way/$', views.WayViewSetList.as_view()),

    url(r'^api/0.6/relation/(?P<id>.+)', views.RelationViewSet.as_view()),
    url(r'^api/0.6/relation/$', views.RelationViewSetList.as_view()),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
