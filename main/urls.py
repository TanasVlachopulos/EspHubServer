from django.conf.urls import url
from . import views

app_name = "main"
urlpatterns = [
    # Pages
    url(r'^$', views.index, name='index'),  # main page with devices list
    url(r'^device/(?P<device_id>[0-9]+)', views.device_detail, name='device_detail'),  # device detail
    url(r'^waiting-devices', views.waiting_devices, name='waiting_devices'),  # devices waiting for verification
    url(r'^display/(?P<device_id>[0-9]+)/(?P<ability_name>\w+)/', views.display, name='display'),
    # Forms
    url(r'^verify-device/(?P<device_id>[0-9]+)', views.verify_device, name='verify_device'),  # device verification form
    url(r'^remove-device/(?P<device_id>[0-9]+)', views.remove_device, name='remove_device'),  # remove device form
    url(r'^output-action/(?P<device_id>[0-9]+)/(?P<ability>\w+)', views.output_action, name='output_action'),  # toogle output form
    url(r'^save-screen/(?P<device_id>[0-9]+)', views.save_screen, name='save_screen'),  # save screen form
    # APIs
    url(r'^api/waiting-devices', views.waiting_devices_api, name='waiting_devices_api'),  # REST api for waiting devices
    url(r'^api/telemetry/(?P<device_id>[0-9]+)', views.telemetry_api, name='telemetry_api'),  # REST api for device telemetry
    url(r'^api/device-values/(?P<device_id>[0-9]+)', views.device_actual_values_api, name='device_actual_values_api'),  # REST api for actual device values
    url(r'^api/records/(?P<device_id>[0-9]+)/(?P<ability>\w+)/$', views.records_api, name='records_api'),  # api provide data for JS plot library
    url(r'api/display/(?P<device_id>[0-9]+)/(?P<ability>\w+)/$', views.display_preview_api, name='display_preview_api'),  # api render graph preview for display setting page
]
