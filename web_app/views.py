from __future__ import unicode_literals
from django.shortcuts import render
from django.core import serializers
from web_app import models
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# def index(request):
#     city_list = list()
#     city_list_json = serializers.serialize("json", models.City.objects.all())
#     # 取出的json数据为str格式
#     city_list_dic = json.loads(city_list_json)
#     # 转换后的list，里面都是字典
#     for i in city_list_dic:
#         city_list.append(i)
#     print(city_list)
#     return render(request, 'index.html', {'city_list': city_list})


def index(request):
    # 每页显示的数据条数
    limit = 50
    city_list = list()
    city_list_json = serializers.serialize("json", models.CityCopy1.objects.all())
    # 取出的json数据为str格式
    city_list_dic = json.loads(city_list_json)
    # 转换后的list，里面都是字典
    for i in city_list_dic:
        city_list.append(i)
    print(city_list)
    paginator = Paginator(city_list, limit)

    page = request.GET.get('page')
    try:
        city_list = paginator.page(page)
    except PageNotAnInteger:
        city_list = paginator.page(1)
    except EmptyPage:
        city_list = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'city_list': city_list})
