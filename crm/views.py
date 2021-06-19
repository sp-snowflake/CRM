from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def dashboard(request):


    return render(request,'crm/dashboard.html')



























