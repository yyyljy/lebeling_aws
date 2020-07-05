from django.shortcuts import render,redirect
from images.models import ImageUserTagBox
from accounts.models import Point

# Create your views here.
def yesnoinfo(request):
    objs = ImageUserTagBox.objects.exclude(image=None).exclude(box=None).exclude(tag=None).order_by('?')
    obj = objs[0]
    context = {
        'image' : obj
    }
    return render(request, 'yesorno/info.html', context)

def rightobj(request):
    obj_pk = request.POST['image_pk']
    obj = ImageUserTagBox.objects.filter(pk=obj_pk)
    image = obj[0].image
    tag = obj[0].tag
    box = obj[0].box
    tag_user = ImageUserTagBox.objects.filter(image=image, tag=tag)
    box_user = ImageUserTagBox.objects.filter(image=image, box=box)
    for user in tag_user:
        point = Point.objects.create(username=user.user, occurpoint=1)
    for user in box_user:
        point = Point.objects.create(username=user.user, occurpoint=1)
    return redirect('yesorno:yesnoinfo')

def wrongobj(request):
    obj_pk = request.POST['image_pk']
    obj = ImageUserTagBox.objects.filter(pk=obj_pk)
    image = obj[0].image
    tag = obj[0].tag
    box = obj[0].box
    tag_user = ImageUserTagBox.objects.filter(image=image, tag=tag)
    box_user = ImageUserTagBox.objects.filter(image=image, box=box)
    for user in tag_user:
        point = Point.objects.create(username=user.user, occurpoint=-1)
    for user in box_user:
        point = Point.objects.create(username=user.user, occurpoint=-1)
    return redirect('yesorno:yesnoinfo')