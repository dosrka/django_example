from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core import serializers
from web_app import models
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    # 每页显示的数据条数
    limit = 70
    city_list_json = serializers.serialize("json", models.CityCopy1.objects.all())
    # 取出的json数据为str格式
    city_list = json.loads(city_list_json)
    # 转换后的list，里面都是字典
    paginator = Paginator(city_list, limit)

    page = request.GET.get('page')
    try:
        city_list = paginator.page(page)
    except PageNotAnInteger:
        city_list = paginator.page(1)
    except EmptyPage:
        city_list = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'city_list': city_list})


def del_content(request):
    nid = request.GET.get("nid")
    models.CityCopy1.objects.filter(id=nid).delete()
    return redirect(index)
