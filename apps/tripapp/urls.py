from django.conf.urls import url
from . import views
app_name = "tripapp"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^add$', views.add, name='add'),
    url(r'^addTrip$', views.addTrip, name='addTrip'),
    url(r'^view/(?P<trip_id>\d+)$', views.view, name='view'),
    url(r'^join/(?P<trip_id>\d+)$', views.join, name='join'),
]