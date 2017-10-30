from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core import serializers
from web_app import models
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    # 每页显示的数据条数
    limit = 5
    city_list_json = serializers.serialize("json", models.City.objects.all())
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

    url_id=request.META['HTTP_REFERER']
    nid = request.GET.get("nid")

    print(url_id)
    print("="*50)
    models.City.objects.filter(id=nid).delete()
    # return redirect('index?page=%s' % url_id)
    return HttpResponseRedirect(url_id)


def add_form(request):
    if request.method == "GET":
        return render(request, 'add_form.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        countrycode = request.POST.get('countrycode')
        district = request.POST.get('district')
        population = request.POST.get('population')
        models.City.objects.create(name=name,
                                   countrycode=countrycode,
                                   district=district,
                                   population=population
                                   )
        return redirect(index)


def edit_form(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        obj = models.City.objects.filter(id=nid).first()
        obj_json = serializers.serialize("json", models.City.objects.filter(id=nid))
        # 取出的json数据为str格式
        city = json.loads(obj_json)

        print("="*50)
        print(city)
        return render(request, 'edit_form.html', {'obj': obj, 'city': city})
    elif request.method == "POST":
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        countrycode = request.POST.get('countrycode')
        district = request.POST.get('district')
        population = request.POST.get('population')
        models.City.objects.filter(id=nid).update(name=name,
                                                  countrycode=countrycode,
                                                  district=district,
                                                  population=population
                                                  )
    return redirect(index)
