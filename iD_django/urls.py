from django.conf.urls import patterns, include, url
from projects.views import *

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

    url(r'^api/0.6/changeset/create', views.create_changeset),
    url(r'^api/0.6/changeset/[^/]+/upload', views.upload_change),

    url(r'^oauth/request_token', views.oauth_token),
    url(r'^api/capabilities', views.capabilities),
    url(r'^api/0.6/map', views.MapViewSet.as_view()),

    # Login / logout.
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),

    # Main page
    (r'^$', create_project),
    (r'^project/.*$', project_page),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url('', include('social.apps.django_app.urls', namespace='social'))
)
