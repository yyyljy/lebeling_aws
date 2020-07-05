from django.shortcuts import render, redirect, get_object_or_404
from .forms import ImgForm, BoxForm
from images.models import Image, Box, Tag, ImageUserTagBox
import random
from django.db.models import Count, Sum

# Create your views here.
def boxing(request):
    return render(request, 'boxing/index.html')

def tag(request):
    image_pk = random.choice(ImageUserTagBox.objects.filter(box_id__isnull=True)).image_id 
    image = get_object_or_404(Image, pk=image_pk)
    taglist = image.tags.annotate(tag_count=Sum('name')).order_by('-tag_count')[:5]
    context = {
        'image' : image,
        'taglist' : taglist
    }

    return render(request, 'boxing/tag.html', context)

def non_tag(request):
    image = Image.objects.order_by('?').first()
    context = {
        'image' : image
    }
    return render(request, 'boxing/nontag.html', context)

def save_position(request, image_pk):
    saveImage = get_object_or_404(Image, pk=image_pk)
    # positionList = request.POST
    # form = BoxForm(request.POST)
    # if request.method == "POST":
    #     box = form.save(commit=False)
    # print(request.POST)
    positions = request.POST.get('position').split(',')
    for position in positions:
        strs = position.split('/')
        lx, ly, rx, ry = map(lambda x: int(round(float(x))), strs)
        saveBox = Box.objects.create(lefttopx=lx, lefttopy=ly, rightbotx=rx, rightboty=ry)
        ImageUserTagBox.objects.create(image=saveImage, user=request.user, box=saveBox)
    
    return redirect('boxing:nontag')

def save_tag_position(request, image_pk):
    saveImage = get_object_or_404(Image, pk=image_pk)
    tagPositions = request.POST.get('tagposition').split(',')
    for tagPosition in tagPositions:
        strs = tagPosition.split('/')
        saveTag = Tag.objects.get(name=strs[0])
        saveBox = Box.objects.create(lefttopx=int(round(float(strs[1]))), lefttopy=int(round(float(strs[2]))), rightbotx=int(round(float(strs[3]))), rightboty=int(round(float(strs[4]))))
        ImageUserTagBox.objects.create(image=saveImage, user=request.user, tag=saveTag, box=saveBox)
    return redirect('boxing:tag')

def save_img(request):
    if request.method == "POST":
        form = ImgForm(files=request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.status = 0
            image.save()
            return redirect('boxing:menu')
    else: 
        form = ImgForm()
    context = {
        'form' : form
    }
    return render(request, 'boxing/imgupload.html', context)
