from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login    # 验证


# Create your views here.

def acc_login(request):
    error_msg = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)    # 验证，如果成功返回对象，错误返回none
        if user:
            print("passed authenticate",user)
            login(request,user)     # 真正的登录，session设置信息
            return redirect(request.GET.get('next','/'))
        else:
            error_msg = "Wrong username or password! "
        print('-----',user,username,password)


    return render(request,'login.html',locals())

def acc_logout(request):
    pass























