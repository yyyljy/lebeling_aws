from django.urls import path
from . import views

app_name = "taging"

urlpatterns = [
    path('images/', views.images, name="images"),
    path('addtag/<int:image_pk>/', views.addtag, name="addtag"),
    path('test/', views.test, name="test"),
    
]