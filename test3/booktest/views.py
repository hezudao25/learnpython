from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from .models import BookInfo, HeroInfo, AreaInfo, UserInfo
import hashlib
from django.conf import settings
from django.core.paginator import Paginator


# 装饰器 判断是否登录
def auth(func):
    def get_auth(request, *args, **kwargs):
        if request.session.get('username', None):
            pass
        else:
            return redirect('login')

        return func(request, *args, **kwargs)
    return get_auth


# Create your views here.
def index(request):
    user_ip = request.META['REMOTE_ADDR']
    print(user_ip)
    if request.session.exists('username'):
        name = request.session.get('username')
    else:
        if 'username' in request.COOKIES:
            name = request.get_signed_cookie('username', salt='wangda')

        else:
            name = ''

    bookinfo_list = BookInfo.objects.order_by('bpub_date')
    paginator = Paginator(bookinfo_list, 5)
    current = request.GET.get('page')
    page = paginator.get_page(current)


    context = {'page': page, 'name': name}

    return  render(request, 'booktest/index.html', context)


def show(request, id):

    return HttpResponse(id)



def login(request):
    if request.session.get('username', None):
        return redirect('index')
    else:
        return render(request, 'booktest/login.html')


def login_check(request):
    """登录校验"""
    # request.POST 保存 POST模式表单信息
    username = request.POST['username']
    pwd = request.POST['password']
    if username == "":
        return JsonResponse({'res': 0, 'message': '请输入用户名'})

    if pwd == "":
        return JsonResponse({'res': 0, 'message': '请输入密码'})
    try:
        us = UserInfo.objects.get(username=username)
        if hashlib.sha1((pwd+us.username).encode('utf-8')).hexdigest() == us.password:
            res = 1
            response = JsonResponse({'res': res})  # 设置COOKIES
            response.set_cookie('username', username, max_age=7 * 24 * 3600)
            response.set_signed_cookie('username', username, salt='wangda')
            # 设置session
            request.session['username'] = username
            request.session.set_expiry(24 * 3600)
            return response

        else:
            res = 0
            return JsonResponse({'res': res, 'message': '密码错误'})
    except :
        return JsonResponse({'res': 0, 'message': '此用户名不存在'})






def login_out(request):
    response = redirect('index')
    response.delete_cookie('username')
    request.session.clear()
    return response



def detail(request, book_id):
    #bookinfo = BookInfo.objects.get(id=book_id)
    bookinfo = get_object_or_404(BookInfo, pk=book_id)
    hero_list = bookinfo.heroinfo_set.all()
    context = {'bookinfo': bookinfo, 'hero_list': hero_list}
    return render(request, 'booktest/detail.html', context)

@auth
def create(request):
    try:
        if request.POST["action"] == "add":
            if request.POST["btitle"]=="":
                raise ValueError("请输入书名")
            if request.POST["bpub_date"]=="":
                raise ValueError("请输入时间")

            files = request.FILES['pic']

            save_path = '%s/book/%s' % (settings.MEDIA_ROOT, files.name)
            with open(save_path, 'wb') as f:
                for content in files.chunks():
                    f.write(content)


            book = BookInfo()
            book.btitle = request.POST["btitle"]
            book.bpub_date = request.POST['bpub_date']
            book.pic = 'book/%s' % files.name
            book.save()

        return redirect('/index')
    except (KeyError):
        return render(request, 'booktest/create.html')

@auth
def herocreate(request, book_id):
    try:
        if request.POST["action"] == "add":
            if request.POST["hname"]=="":
                raise ValueError("请输入英雄名称")
            if request.POST["hcomment"]=="":
                raise ValueError("请输入备注")

            book = BookInfo.objects.get(id=book_id)
            hero = HeroInfo()
            hero.hname = request.POST["hname"]
            hero.hcomment = request.POST['hcomment']
            hero.hbook = book
            hero.save()

        return redirect('/detail/%s/' % book_id)
    except (KeyError):
        return render(request, 'booktest/herocreate.html')

@auth
def bookdelete(request, book_id):
    book = get_object_or_404(BookInfo, pk=book_id)
    book.delete()
    return redirect('/index')


def areas(request):
    try:
        area = AreaInfo.objects.get(atitle='杭州市')
        parent = area.aparent
        children = area.areainfo_set.all()
    except:
        area = None
        parent = None
        children =None
    context = {'area': area, 'parent': parent, 'children': children}
    return render(request, 'booktest/areas.html', context)