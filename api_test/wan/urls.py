from django.contrib import admin
from django.urls import path,include
from . import views
app_name = 'api'
urlpatterns = [
    #path('',views.choice,name='choice'),
    path('api/v2/',views.Datalist.as_view(),name='datalist'),
    #path('api/v2/<int:pk>/',views.Data.as_view()),
    path('api/v3/',views.DeviceData.as_view(),name='device_data'),
    #path('api/v3/<int:pk>/',views.DeviceDetail.as_view()),
    path('api/v2/temp/',views.TempDevice.as_view(),name='device_temp'),


]
# device_mac = Dn.objects.filter(device_name__contains='Dekist')[0].device_mac
# sensor_mac = Dn.objects.filter(device_name__contains='Dekist')[0].sensor_mac
# url2 = 'https://oa.tapaculo365.com/tp365/v1/channel/get_recentdata'
# params2 = {
#     'device_mac': device_mac,
#     'sensor_mac': sensor_mac,
#     'api_key': 4528458,
#     'api_secret': '3fa6d40e4461cd250a683b86eed42bad'
# }
# r2 = requests.get(url2, params=params2)
# data = r2.json()
# df = pd.DataFrame(data['rows'])