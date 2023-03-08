"""ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url

from qa.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', new_questions, name='new_questions'),
    url(r'^login/$', login, name='login'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^question/(?P<pk>\d+)/$', question_details, name='question_details'),
    url(r'^ask/$', ask, name='ask'),
    url(r'^popular/$', popular_questions, name='popular_questions'),
]
