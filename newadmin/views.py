from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login    # 验证
from django import conf     # 动态导入，以后迁移到其它app都能使用
from newadmin import app_setup
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# from crm import models
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from newadmin import form_handle


app_setup.newadmin_auto_discover()

from newadmin.sites import site
# print("sites",site.enabled_admins)

def acc_login(request):
    error_msg = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)    # 验证，如果成功返回对象，错误返回none
        if user:
            print("passed authenticate",user)
            login(request,user)     # 真正的登录，session设置信息
            return redirect(request.GET.get('next','/newadmin/'))
        else:
            error_msg = "Wrong username or password! "
        print('-----',user,username,password)


    return render(request,'newadmin/login.html',locals())

def acc_logout(request):
    pass

def app_index(request):

    return render(request,'newadmin/app_index.html',{'site':site})


def get_filter_result(request,querysets):
    filter_conditions={}
    for key,val in request.GET.items():
        if key in ('_page','_o','_q'):continue
        if val:
            filter_conditions[key] =  val
    return querysets.filter(**filter_conditions),filter_conditions


def get_orderby_result(request,querysets,admin_class):   # 排序
    """排序"""
    current_ordered_column = {}
    orderby_index = request.GET.get('_o')
    if orderby_index:
        orderby_key = admin_class.list_display[abs(int(orderby_index))]
        current_ordered_column[orderby_key] = orderby_index # 为了让前端知道当前排序知道的列

        if orderby_index.startswith('-'):
            orderby_key = '-' + orderby_key
        return querysets.order_by(orderby_key),current_ordered_column
    else:
        return querysets,current_ordered_column

def get_searched_result(request,querysets,admin_class):
    '''搜索'''
    search_key = request.GET.get('_q')
    if search_key:
        q = Q()
        q.connector = 'OR'

        for search_field in admin_class.search_fields:
            q.children.append(("%s__contains" % search_field,search_key))

        return querysets.filter(q)
    return querysets


@login_required
def table_obj_list(request,app_name,model_name):
    """取出指定model里的数据返回给前端"""
    # print("app_name,model_name:",site.enabled_admins[app_name][modle_name])
    admin_class = site.enabled_admins[app_name][model_name]
    querysets = admin_class.model.objects.all().order_by('-id')

    querysets,filter_condtions = get_filter_result(request,querysets)
    admin_class.filter_condtions = filter_condtions

    # 搜索
    querysets = get_searched_result(request,querysets,admin_class)
    admin_class.search_key = request.GET.get('_q','')

    # 排序
    querysets,sorted_column = get_orderby_result(request,querysets,admin_class)

    # 分页
    paginator = Paginator(querysets,2)

    page = request.GET.get('_page')
    # print('---',request.GET)
    try:
        querysets = paginator.page(page)
    except PageNotAnInteger:
        querysets = paginator.page(1)
    except EmptyPage:
        querysets = paginator.page(paginator.num_pages)


    return render(request,'newadmin/table_obj_list.html',locals())

@login_required
def table_obj_change(request,app_name,model_name,obj_id):
    """newadmin 数据修改页"""

    admin_class = site.enabled_admins[app_name][model_name]
    model_form = form_handle.create_dynamic_model_form(admin_class)
    obj = admin_class.model.objects.get(id = obj_id)

    if request.method == "GET":
        form_obj = model_form(instance=obj)
    elif request.method == "POST":
        form_obj = model_form(instance=obj,data = request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/newadmin/%s/%s/" %(app_name,model_name))

    return render(request,'newadmin/table_obj_change.html',locals())


@login_required
def table_obj_add(request,app_name,model_name):
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = form_handle.create_dynamic_model_form(admin_class,form_add=True)
    if request.method == "GET":
        form_obj = model_form()
    elif request.method == "POST":
        form_obj = model_form(data = request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/newadmin/%s/%s/" % (app_name, model_name))

    return render(request,'newadmin/table_obj_add.html',locals())




