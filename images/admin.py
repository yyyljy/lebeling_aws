from django.contrib import admin
from .models import Image, Box, Tag, ImageUserTagBox

# Register your models here.
admin.site.register(Image)
admin.site.register(Box)
admin.site.register(Tag)
admin.site.register(ImageUserTagBox)
