from django.conf.urls import url
from . import views
app_name = "eventapp"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^add$', views.add, name='add'),
    url(r'^addevent$', views.addevent, name='addevent'),
    url(r'^addactivity/(?P<event_id>\d+)$', views.addactivity, name='addactivity'),
    url(r'^addgoal/(?P<event_id>\d+)$', views.addgoal, name='addgoal'),
    url(r'^view/(?P<event_id>\d+)$', views.view, name='view'),
    url(r'^join/(?P<event_id>\d+)$', views.join, name='join'),
]