from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.paginator import Paginator
from openpyxl import load_workbook,Workbook
from django.http import HttpResponse
from .models import Tinhnut
# Create your views here.
def index(request):
    return render(request, 'Webtinhnut/index.html')
def caukien(request):
    name = request.GET.get("name")
    caukien = Tinhnut.objects.all().order_by('name')
    if name:
        caukien = caukien.filter(name__icontains = name)
    paginator = Paginator(caukien, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'caukien': caukien,
    }
    return render(request,'Webtinhnut/caukien.html',context)
def add_caukien(request):
    caukien= Tinhnut.objects.all()
    context={
        'caukien': caukien,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'Webtinhnut/add-caukien.html',context)
    if request.method =='POST':
        name = request.POST['name']
        b = request.POST['b']
        h = request.POST['h']
        L = request.POST['L']
        cben = request.POST['cben']
        nthep= request.POST['nthep']
        thepd= request.POST['thepd']
        a = request.POST['a']
        thept= request.POST['thept']
        a1 = request.POST['a1']
        try: 
            b = float(b)
            h = float(h)
            L = float(L)
            a = float(a)
            a1 = float(a1)
        except ValueError:
            messages.error(request, 'Must be a valid number')
            return render(request, 'Webtinhnut/add-caukien.html',context)
    Tinhnut.objects.create(name=name,b=b,h=h,L=L,cben=cben,nthep=nthep,thepd=thepd,a=a,thept=thept,a1=a1)
    messages.success(request,'Cấu kiện đã lưu thành công')
    return redirect('caukien')


def edit_caukien(request, id):
    caukien = Tinhnut.objects.get(pk=id)
    context = {
        'caukien': caukien,
        'values': caukien,
    }
    if request.method == 'GET':
        return render(request, 'Webtinhnut/edit-caukien.html',context)
    if request.method =='POST':
        name = request.POST['name']
        b = request.POST['b']
        h = request.POST['h']
        L = request.POST['L']
        cben = request.POST['cben']
        nthep= request.POST['nthep']
        thepd= request.POST['thepd']
        a = request.POST['a']
        thept= request.POST['thept']
        a1 = request.POST['a1']
        try: 
            b = float(b)
            h = float(h)
            L = float(L)
            a = float(a)
            a1 = float(a1)
        except ValueError:
            messages.error(request, 'Must be a valid number')
            return render(request, 'Webtinhnut/edit-caukien.html',context)
    caukien.name=name
    caukien.b=b
    caukien.h=h
    caukien.L=L
    caukien.cben=cben
    caukien.nthep=nthep
    caukien.thepd=thepd
    caukien.a=a
    caukien.thept=thept
    caukien.a1=a1
    messages.success(request,'Cấu kiện đã lưu thành công')
    return redirect('caukien')

def delete_caukien(request,id):
    caukien= Tinhnut.objects.get(pk=id)
    caukien.delete()
    messages.success(request,'Đã xóa cấu kiện')
    return redirect('caukien')

def tinhmomen(request):
    return render(request, 'Webtinhnut/tinhmomen.html')



def tinhvetnut(request):
    return render(request, 'Webtinhnut/tinhvetnut.html')
