from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sub', views.sub, name='sub'),
    path('reset', views.reset, name='reset')
]