from django.urls import path
from . import views

app_name = "boxing"

urlpatterns = [
    path('', views.boxing, name="menu"),
    path('tag/', views.tag, name="tag"),
    path('non_tag/', views.non_tag, name="nontag"),
    path('save_img/', views.save_img, name="save_img"),
    path('save_position/<int:image_pk>/', views.save_position, name="save_position"),
    path('save_tag_position/<int:image_pk>/', views.save_tag_position, name="save_tag_position"),
]