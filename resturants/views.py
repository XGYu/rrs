import json
import os

from functools import wraps
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .hme import *
from .jrlm import *
import random

import pandas as pd


# Create your views here.
def index(request):
    return HttpResponse("<h1>这是一个餐馆推荐系统.</h1>")


# 主页：展示前五个餐厅
def show_res_view(request, *arg, **kwargs):
    qs = Resturant.objects.all()[:10]
    resturant = None
    if qs.exists():
        resturant = qs
    return render(request, "resturants/detail.html", {"object": resturant})


# 搜索
def search_view(request, *args, **kwargs):
    q = request.GET.get('q')
    err_msg = ''
    if not q:
        err_msg = '请输入关键词'
        return render(request, "resturants/search.html", locals())

    res_qs = Resturant.objects.filter(name__icontains=q)
    return render(request, "resturants/search.html", locals())


# 展示全部餐厅
def all_res_view(request, *args, **kwargs):
    res_qs = Resturant.objects.all()
    limit = 10
    paginator = Paginator(res_qs, limit)
    page = request.GET.get("page", "1")

    result = paginator.page(page)

    return render(request, "resturants/all_res.html", {"res_page": result})




# 登录模块
def login_view(request, *args, **kwargs):
    if request.session.get('is_login', None):
        return redirect("/")
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = ""
        if username and password:
            try:
                user = User.objects.get(username=username)
                if user.password == password:
                    request.session["is_login"] = True
                    request.session["user_id"] = user.pk
                    request.session["user_name"] = user.username
                    return redirect('/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
            return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


# 注册用户 默认在已经登陆的情况下不可以继续注册
def register_view(request, *args, **kwargs):
    if request.session.get("is_login", None):
        return redirect("/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST or None)
        message = ""
        if register_form.is_valid():
            username = register_form.cleaned_data["username"]
            password1 = register_form.cleaned_data["password1"]
            password2 = register_form.cleaned_data["password2"]
            email = register_form.cleaned_data["email"]
            name = register_form.cleaned_data["name"]
            if password1 != password2:
                message = "两次密码输入不同！"
                return render(request, "login/register.html", locals())
            else:
                same_user_qs = User.objects.filter(username=username)
                if same_user_qs:
                    message = "用户名已存在，请重新选择用户名！"
                    return render(request, "admin/register.html", locals())
                new_user = User()
                new_user.username = username
                new_user.password = password1
                new_user.email = email
                new_user.name = name
                new_user.save()
                return redirect('/login/')
    register_form = RegisterForm()
    return render(request, "login/register.html", locals())


# 登出模块
def logout_view(request, *args, **kwargs):
    if not request.session.get("is_login", None):
        return redirect("/")
    request.session.flush()
    return redirect('/')


# 验证是否登录
def login_confirm(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        is_login = request.session.get("is_login")
        if is_login:
            return func(*args, **kwargs)
        else:
            return redirect("/login/")
    return wrapper


# 个人信息页面
@login_confirm
def my_info_view(request, *args, **kwargs):
    username = request.session["user_name"]
    user = User.objects.get(username=username)
    comment_qs = Comment.objects.filter(user=user)
    info_qs = Info.objects.filter(user=user)
    return render(request, "resturants/my_info.html", locals())


# 查看某个餐厅的详细信息
# 包括用户可以在此订餐、评论和查看对应的评价
@login_confirm
def res_detail_view(request, pk, *args, **kwargs):
    resturant = Resturant.objects.get(pk=pk)
    username = request.session["user_name"]
    user = User.objects.get(username=username)  # 当前的登录用户
    info_qs = Info.objects.filter(Q(user=user), Q(resturant=resturant))  # 找到当前用户在当前餐厅的用餐记录
    comment_qs = Comment.objects.filter(resturant=resturant)
    my_comment_qs = Comment.objects.filter(resturant=resturant)
    clicklunch = False
    if request.method == "POST":
        content = request.POST.get("comment" or None)
        rate_taste = 5
        rate_surround = 5
        rate_service = 5
        message = ""
        if request.POST.get("select1") != "请为该餐厅的口味评分":
            rate_taste = int(request.POST.get("select1"))
        else:
            message = "请填写完整的评价内容！"
        if request.POST.get("select2") != "请为该餐厅的环境评分":
            rate_surround = int(request.POST.get("select2"))
        else:
            message = "请填写完整的评价内容！"
        if request.POST.get("select3") != "请为该餐厅的服务评分":
            rate_service = int(request.POST.get("select3"))
        else:
            message = "请填写完整的评价内容！"
        if content:
            new_comment = Comment()
            new_comment.resturant = resturant
            new_comment.user = user
            new_comment.content = content
            new_comment.rate_taste = rate_taste
            new_comment.rate_surround = rate_surround
            new_comment.rate_service = rate_service
            new_comment.create_time = timezone.now()
            new_comment.save()
            content = None
            return redirect("/detail/%s/" % pk)
        # comment_form = CommentForm(request.POST or None)
        # message = ""
        # if comment_form.is_valid():
        #     content = comment_form.cleaned_data["content"]
        #     rate_taste = comment_form.cleaned_data["rate_taste"]
        #     rate_surround = comment_form.cleaned_data["rate_surround"]
        #     rate_service = comment_form.cleaned_data["rate_service"]
        #     new_comment = Comment()
        #     new_comment.content =content
        #     new_comment.rate_taste = rate_taste
        #     new_comment.rate_surround = rate_surround
        #     new_comment.rate_service = rate_service
        #     new_comment.resturant = resturant
        #     new_comment.user = user
        #     new_comment.create_time = timezone.now()
        #     new_comment.save()
    if request.method == "GET":
        if request.GET.get("lunchevent") and (not clicklunch):
            info = Info()
            info.resturant = resturant
            info.user = user
            info.info_time = timezone.now()
            info.save()
            clicklunch = True

    return render(request, "resturants/res_detail.html", locals())


# 载入餐厅数据
def load_res_data_view(request, *args, **kwargs):
    f_res = open("./data/result_shanghai.txt", "r", encoding="utf-8")
    df_loc = pd.read_csv("./data/rrs_resturant.csv")

    Resturant.objects.all().delete()
    for row in df_loc.iterrows():
        res_line = f_res.readline()
        js_data = json.loads(res_line)
        name = js_data["商铺"]
        longlatitude = row[1]['venueId']
        longtitude = row[1]['longitude']
        latitude = row[1]['latitude']
        address = js_data["地址"]
        type = js_data["类型"]
        position = js_data["商区"]
        rate_taste = js_data["口味"]
        rate_surround = js_data["环境"]
        rate_service = js_data["服务"]
        resturant = Resturant.objects.create(name=name, address=address, longlatitude=longlatitude,
                                             type=type, position=position,
                                             rate_taste=rate_taste, rate_surround=rate_surround,
                                             rate_service=rate_service, longtitude=longtitude, latitude=latitude)
    f_res.close()
    return redirect("/load-user-data-once/")


# 载入餐厅图片
def load_res_img_view(request, *args, **kwargs):
    images = os.listdir("./cdn_test/media/resturants")
    qs = Resturant.objects.all()
    res_str = "resturants/"
    for res in qs:
        image = random.choices(images)[0]
        res.res_image = res_str + image
        res.save()
    return render(request, "resturants/load_data.html", {})


# 载入用户数据
def load_user_data_view(request, *args, **kwargs):
    f_user = open("./data/rrs_userlist.txt", "r", encoding='utf-8')
    User.objects.all().delete()
    while True:
        user_line = f_user.readline().strip().split()
        if not user_line:
            break
        username = user_line[0]
        print(type(username))
        user = User.objects.create(username=username)
    f_user.close()
    return redirect("/load-info-data-once/")


# 载入就餐记录
def load_info_data_view(request, *args, **kwargs):
    df_record = pd.read_csv('./data/rrs_record.csv')
    del df_record['longitude']
    del df_record['latitude']
    df_record['utcTimestamp'] =  pd.to_datetime(df_record['utcTimestamp'], format='%Y-%m-%d %H:%M:%S')
    Info.objects.all().delete()
    for i in range(len(df_record)):
        username = df_record['userId'][i]
        user = User.objects.get(username=username)
        venueId = df_record['venueId'][i]
        resturant = Resturant.objects.get(longlatitude=venueId)
        record_time = df_record['utcTimestamp'][i]
        new_info = Info.objects.create(user=user, resturant=resturant, info_time=record_time)
    return render(request, "resturants/load_data.html", {})


# 利用hme算法为用户推荐餐馆
@login_confirm
def hme_rrs_view(request, *args, **kwargs):
    username = request.session["user_name"]         # 获取了当前用户名
    user = User.objects.filter(username=username)[0]
    info = Info.objects.filter(user=user).order_by('-info_time')[0]
    res = info.resturant
    r_list = RecTopK(0.8, 5, user.username, res.longlatitude)
    res_list = []
    for r_no in r_list:
        res_list.append(Resturant.objects.get(longlatitude=r_no))
    res_qs = Resturant.objects.filter(pk__in=[x.pk for x in res_list])
    print('top5推荐算法：')
    for res in res_qs:
        print(res.name, "\t", res.address)
    return render(request, "resturants/hme_rrs.html", locals())


# 利用jrlm算法为用户推荐餐馆
@login_confirm
def jrlm_rrs_view(request, *args, **kwargs):
    username = request.session["user_name"]         # 获取了当前用户名
    user = User.objects.filter(username=username)[0]
    info = Info.objects.filter(user=user).order_by('-info_time')[0]
    res = info.resturant
    r_list = RecTopK(0.5, 10, user.username, res.longlatitude)
    res_list = []
    for r_no in r_list:
        res_list.append(Resturant.objects.get(longlatitude=r_no))
    res_qs = Resturant.objects.filter(pk__in=[x.pk for x in res_list])
    print('top10推荐算法：')
    for res in res_qs:
        print(res.name, "\t", res.address)
    return render(request, "resturants/jrlm_rrs.html", locals())