from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.views import templates
from accounts.models import Point

import operator


def ranking(request):
    # [ORM 사용 가능]
    # 전체 데이터 가져오기
    points = Point.objects.all()
    
    # 계산 - dictionary(이름, 점수)
    dict_ranking = {}
    for user in points:   
        username = user.username
        point = user.occurpoint
        # 이미 dict에 넣은 이름이면 점수 더해서 다시 넣어줌
        if dict_ranking.get(username) != None :
            dict_ranking[username] += point
        # 없으면 이름, 점수 세트 처음으로 dict에 넣어주기 
        else :
            dict_ranking[username] = point

    # 정렬(점수 높은순) => 튜플로 변환
    ranking = sorted(dict_ranking.items(), key=(lambda x:x[1]), reverse=True)
    # 인자값에 있는 lambda x:x[1])는 정렬하고자 하는 키 값을 1번째 인덱스 기준으로 하겠다는 것입니다.
    # 1번째 인자는 Value입니다.

    # 그 데이터 템플릿에게 넘겨주기
    context = {
        'ranking' : dict(ranking)
    }

    return render(request, 'ranking/ranking.html',context)

