from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.paginator import Paginator
# from openpyxl import load_workbook,Workbook
from django.http import HttpResponse
from .models import Tinhnut
import psycopg2
from psycopg2.extras import RealDictCursor
# Create your views here.
def index(request):
    return render(request, 'Webtinhnut/index.html')
def caukien(request):
    name = request.GET.get("name")
    caukien = Tinhnut.objects.all().order_by('-id')
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
    if request.GET.get('caukien') != None:
        caukien = request.GET.get('caukien')  # Sử dụng 'caukien' từ JavaScript
        tinhtai = float(request.GET.get('tinhtai'))
        hoattai = float(request.GET.get('hoattai'))
        if caukien:
            try:
                L = Tinhnut.objects.get(name=caukien).L
                Mttg = ((tinhtai * L) ** 2) / 12
                Mhtg = ((hoattai * L) ** 2) / 12
                Mdhg = Mttg+0.3*Mhtg
                Mtpg = Mttg+Mhtg
                Mnhg = (1-0.3)*Mhtg
                Mttd = ((tinhtai * L) ** 2) / 8
                Mhtd = ((hoattai * L) ** 2) / 8
                Mdhd = Mttd+0.3*Mhtd
                Mtpd = Mttd+Mhtd
                Mnhd = (1-0.3)*Mhtd
                Mgiua={
                    'Mttg': round(Mttg,2),
                    'Mhtg': round(Mhtg,2),
                    'Mdhg':round(Mdhg,2),
                    'Mtpg': round(Mtpg,2),
                    'Mnhg': round(Mnhg,2)
                }
                Mdau={
                    'Mttd': round(Mttd,2),
                    'Mhtd': round(Mhtd,2),
                    'Mdhd':round(Mdhd,2),
                    'Mtpd': round(Mtpd,2),
                    'Mnhd': round(Mnhd,2)
                }
                # context = {'Mtt': round(Mtt,2), 'Mht': round(Mht,2)}
                context ={'Mgiua':Mgiua,'Mdau':Mdau}
                return render(request, 'Webtinhnut/tinhmomen.html', context)
            except (Tinhnut.DoesNotExist, Exception) as error:  # Xử lý các trường hợp ngoại lệ cụ thể & chung chung
                context = {'error': str(error)}  # Truyền thông báo lỗi tới template
                return render(request, 'Webtinhnut/tinhmomen.html', context)

    # Xử lý yêu cầu GET (tùy chọn, để hiển thị ban đầu)
    list_caukien = []
    try:
        caukien = Tinhnut.objects.all().values_list('name', flat=True)  # Truy xuất tất cả tên một cách hiệu quả
        list_caukien = list(caukien)  # Chuyển queryset sang list cho ngữ cảnh template
    except Exception as error:
        print(error)
        # Xem xét thêm thông báo thân thiện với người dùng cho template

    context = {'caukien': list_caukien}
    return render(request, 'Webtinhnut/tinhmomen.html', context)

def tinhvetnut(request):
    return render(request, 'Webtinhnut/tinhvetnut.html')


def get_connection():
    connection = psycopg2.connect(
            user="postgres",
            password ="123456",
            host="localhost",
            port="5432",
            database ="Webtinhnut"
    )
    return connection
def close_connection(connection):
    if connection:
        connection.close()