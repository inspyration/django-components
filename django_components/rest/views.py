from django.shortcuts import render
from component.models import Component, Screen
from rest_framework import generics
from rest.serializers import ComponentSerializer, ScreenSerializer

### REST Views ###

class ComponentList(generics.ListAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

class ComponentDetails(generics.RetrieveAPIView):
    queryset = Component.objects.get(pk="pk")
    serializer_class = ComponentSerializer


class ScreenList(generics.ListAPIView):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer


class ScreenDetails(generics.RetrieveAPIView):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer