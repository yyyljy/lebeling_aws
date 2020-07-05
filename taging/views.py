from django.shortcuts import render, redirect
import os
import random
from django import template
from django.conf import settings
from images.models import Image, Tag, ImageUserTagBox
from accounts.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum

# Create your views here.
@login_required
def images(request):
    image = Image.objects.order_by('?').first()
    context = {
        #'image' : image.image.url,
        'image' : image.image_thumbnail.url,
        'image_pk' : image.pk
    }
    return render(request, 'taging/images.html',context)

@login_required
@require_POST
def addtag(request, image_pk):
    user = User.objects.get(username=request.user)
    image = Image.objects.get(pk=image_pk)

    datalen = len(list(request.POST))
    datalist = request.POST.getlist('tag')
    for data in datalist:
        try:
            #tag = Tag.objects.filter(name=data)
            tag = Tag.objects.get(name=data)
        except:
            tag = Tag.objects.create(name=data)
        imagetag = ImageUserTagBox.objects.create(user=user,image=image,tag=tag)

    return redirect('taging:images')

def test(request):
    # delimage = Image.objects.filter(image='')
    # delimage.delete()
    # print(delimage)
    image = Image.objects.order_by('?').first()
    tags = image.tags.annotate(tag_count=Sum('name')).order_by('-tag_count')
    context = {
        'image' : image.image.url,
        'tags' : tags
    }
    return render(request, 'taging/test.html', context)