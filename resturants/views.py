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
import random


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
    f_res = open("./data/resturants.txt", "r", encoding="utf-8")
    f_loc = open("./data/location.txt", "r", encoding="utf-8")
    Resturant.objects.all().delete()
    while True:
        res_line = f_res.readline()
        loc_line = f_loc.readline().strip().split()
        if (not res_line) or (not loc_line):
            break
        js_data = json.loads(res_line)
        name = js_data["商铺"]
        longlatitude = loc_line[0]
        address = js_data["地址"]
        type = js_data["类型"]
        position = js_data["商区"]
        rate_taste = js_data["口味"]
        rate_surround = js_data["环境"]
        rate_service = js_data["服务"]
        resturant = Resturant.objects.create(name=name, address=address, longlatitude=longlatitude,
                                             type=type, position=position,
                                             rate_taste=rate_taste, rate_surround=rate_surround,
                                             rate_service=rate_service)
    f_res.close()
    f_loc.close()
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
    f_user = open("./data/user.txt", "r", encoding='utf-8')
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
    f_info = open("./data/nyc_data.txt", "r", encoding="utf-8")
    Info.objects.all().delete()
    info_line = f_info.readline()
    info = info_line.strip().split(" ")
    cur_user = info[0]
    user = User.objects.get(username=cur_user)
    while True:
        if not info_line:
            break
        if info[0][0] == "u":
            cur_user = info[0]
            user = User.objects.get(username=cur_user)
        for pos in info:
            if pos[0] == 'l':
                try:
                    res = Resturant.objects.get(longlatitude=pos)
                    new_info = Info.objects.create(user=user, resturant=res)
                except Resturant.DoesNotExist:
                    print(pos)
        info_line = f_info.readline()
        info = info_line.strip().split(" ")

    return render(request, "resturants/load_data.html", {})




