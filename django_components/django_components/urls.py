"""django_components URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import DetailView

from component.models import Screen


if settings.DEBUG:
    import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('components/', include("component.urls")),
    path("app/<int:pk>/", DetailView.as_view(model=Screen, template_name="screen.html"), name="screen_bootstrap")
]

if settings.DEBUG:
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns  # pylint: disable=invalid-name
