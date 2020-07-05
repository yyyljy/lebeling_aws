from django.urls import path
from . import views

app_name = "yesorno"

urlpatterns = [
    path('', views.yesnoinfo, name="yesnoinfo"),
    path('right/', views.rightobj, name="rightobj"),
    path('wrong/', views.wrongobj, name="wrongobj"),
]