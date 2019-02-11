from rest.views import ComponentList, ComponentDetails, ScreenList, ScreenDeatils
from component.models import Component
from django.urls import path, re_path

urlpatterns = [
    path('components/', ComponentList.as_view(), name='components'),
    re_path(r'^components/(?P<pk>\d+/$', ComponentDetails.as_view(), name='component-detail'),
    path('screens/', ScreenList.as_view(), name=''screens),
    re_path(r'^screens/(?P<pk>\d+/$', ScreenDetails.as_view(), name='screen-detail'),
]