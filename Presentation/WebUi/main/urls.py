from django.conf.urls import url
from . import views

app_name = "main"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^device/(?P<device_id>[0-9]+)/$', views.device_detail, name='device_detail'),
    url(r'^api/waiting-devices', views.waiting_devices_api, name='waiting_devices_api'),
    url(r'^waiting-devices', views.waiting_devices, name='waiting_devices'),
    url(r'^verify-device/(?P<device_id>[0-9]+)', views.verify_device, name='verify_device'),
]
