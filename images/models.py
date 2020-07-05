from django.db import models
from django.db.models import constraints
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from accounts.models import User

# Create your models here.
# user.pk => company name??
# def articles_image_path(instance, filename):
#     return f'user_{instance.user.pk}/{filename}'

class Image(models.Model):
    image = models.ImageField(blank=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[Thumbnail(800, 600)],
        format='JPEG',
        options={'quality':90}
    )
    # 생성된 후 오랫동안 분석이 완료 되지 않은 이미지 검출용
    created_at = models.DateTimeField(auto_now_add=True)
    # 분석 (완료 / 진행) 등
    status = models.PositiveSmallIntegerField()
    tags = models.ManyToManyField('Tag', through='ImageUserTagBox')
    #filename = models.CharField(max_length=150)

class Box(models.Model):
    #좌측 상단 x,y ? 
    lefttopx = models.PositiveSmallIntegerField()
    lefttopy = models.PositiveSmallIntegerField()
    #우측 하단 x,y ?
    rightbotx = models.PositiveSmallIntegerField()
    rightboty = models.PositiveSmallIntegerField()
    # 1:M 구조
    #source_img = models.ForeignKey(Image, on_delete=models.CASCADE)
    #maker_userid = models.ForeignKey(User.username, on_delete=models.CASCADE)

class Tag(models.Model):
    # 태그 내용(유니크 제약 조건)
    # 중복되는 것은 Image-Tag-Username으로 묶어서 추가
    name = models.CharField(max_length=30, unique=True)
    #source_img = models.ForeignKey(Image, on_delete=models.CASCADE)
    #maker_userid = models.ForeignKey(User.username, on_delete=models.CASCADE)

class ImageUserTagBox(models.Model):
    # image, user는 not null
    # image-tag 일 경우 box=null
    # image-box 일 경우 tag=null
    # point는 선택 (받은 / 받지 못한) 횟수 +- 카운트
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='DELETED_ACCOUNT')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    box = models.ForeignKey(Box, on_delete=models.CASCADE, null=True)
    point = models.IntegerField(default=0)
    class Meta:
        constraints = [
            #한 명의 사람은 한 개의 이미지에 같은 태그를 하나만 달 수 있도록
            #(ex:'A'라는 사람은 'IMAGE1.jpg'에 '사람'이라는 태그를 하나만 달 수 있음)
            models.UniqueConstraint(fields=['image', 'tag', 'user', 'box'], name='unique_imagetaguserbox'),
        ]

# class ImageBoxUser(models.Model):
#     image = models.ForeignKey(Image, on_delete=models.CASCADE)
#     box = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

# A ㄱ 1
#   ㄴ 2
# B ㄱ 3
#   ㅇ 1
# Reservation.objects.all()
# <QuerySet [<Reservation: 1번 의사, 의사가나다의 1번 환자, 환자라마바와 간호사:간호사사자차>]>

# Reservation.objects.filter(doctor__name='의사가나다')
# <QuerySet [<Reservation: 1번 의사, 의사가나다의 1번 환자, 환자라마바와 간호사:간호사사자차>]>