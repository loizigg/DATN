from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.paginator import Paginator
# from openpyxl import load_workbook,Workbook
from django.http import HttpResponse
from .models import Tinhnut
import psycopg2
from psycopg2.extras import RealDictCursor
import math
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
        caukien = request.GET.get('caukien')
        tinhtai = float(request.GET.get('tinhtai'))
        hoattai = float(request.GET.get('hoattai'))
        if caukien:
            try:
                L = Tinhnut.objects.get(name=caukien).L
                Mttg = ((tinhtai * L) ** 2) / 12
                Mhtg = ((hoattai * L) ** 2) / 12
                Mdhg = Mttg+0.3*Mhtg
                Mtpg = Mttg+Mhtg
                Mnhg = Mttg+0.3*Mhtg
                Mttd = ((tinhtai * L) ** 2) / 8
                Mhtd = ((hoattai * L) ** 2) / 8
                Mdhd = Mttd+0.3*Mhtd
                Mtpd = Mttd+Mhtd
                Mnhd = Mttd+0.3*Mhtd
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
                context ={'Mgiua':Mgiua,'Mdau':Mdau}
                return render(request, 'Webtinhnut/tinhmomen.html', context)
            except (Tinhnut.DoesNotExist, Exception) as error:  
                context = {'error': str(error)}  
                return render(request, 'Webtinhnut/tinhmomen.html', context)
    list_caukien = []
    try:
        caukien = Tinhnut.objects.all().values_list('name', flat=True) 
        list_caukien = list(caukien)  
    except Exception as error:
        print(error)
    
    context = {'caukien': list_caukien}
    return render(request, 'Webtinhnut/tinhmomen.html', context)

def tinhvetnut(request):
    if request.GET.get('caukien') != None:
           caukien = request.GET.get('caukien')  # Sử dụng 'caukien' từ JavaScript
           mdh = float(request.GET.get('mdh'))
           mtp = float(request.GET.get('mtp'))
           mnh = float(request.GET.get('mnh'))
           if caukien:
                try:
                    b = Tinhnut.objects.get(name=caukien).b
                    h = Tinhnut.objects.get(name=caukien).h
                    L = Tinhnut.objects.get(name=caukien).L
                    cben= Tinhnut.objects.get(name=caukien).cben
                    nthep = Tinhnut.objects.get(name=caukien).nthep
                    thepd = Tinhnut.objects.get(name=caukien).thepd
                    a = Tinhnut.objects.get(name=caukien).a
                    thept = Tinhnut.objects.get(name=caukien).thept
                    a1 = Tinhnut.objects.get(name=caukien).a1
                    listcben=["B15","B20","B22.5","B25","B30","B35","B40","B45","B50","B50"]
                    Rb= [8.5,11.5,13,14.5,17,19.5,22,25,27.5,33]
                    Rbt = [0.75,0.9,1,1.05,1.15,1.3,1.4,1.5,1.6,1.8]
                    Rbser = [11,15,16.75,18.5,22,25.5,19,32,36,43]
                    Rbtser = [1.1,1.35,1.45,1.55,1.75,1.95,2.1,2.25,2.45,2.6]
                    Eb = [24000,27500,29000,30000,32500,34500,36000,37000,38000,39500]
                    listnthep = ["AI","AII","AIII","AIV","CB240T","CB300V","CB400V","CB500V"]
                    Rs= [225,280,365,510,210,260,350,435]
                    Rsc=[225,280,365,450,210,260,350,400]
                    Rsw=[175,225,290,405,170,210,280,300]
                    Es =[200000,200000,200000,190000,200000,200000,200000,200000]
                    for i, value in enumerate(listcben):
                        if cben == value:
                            aRb = Rb[i]
                            aRbt = Rbt[i]
                            aRbser = Rbser[i]
                            aRbtser = Rbtser[i]
                            aEb = Eb[i]
                            break
                    for i, value in enumerate(listnthep):
                        if nthep == value:
                            aRs = Rs[i]
                            aRsc = Rsc[i]
                            aRsw = Rsw[i]
                            aEs = Es[i]
                            break
                    h0 = h - a
                    h1 = h - a1
                    clthepd = thepd.split("+")
                    Asd = 0
                    for clthep1 in clthepd:
                        sl1,d1 = clthep1.split("Ф")
                        sl1 = int(sl1)
                        d1 = int(d1)
                        dientich1 = (sl1 * math.pi *d1**2)/4
                        Asd += dientich1/100
                    clthept = thept.split("+")
                    Ast = 0
                    for clthep2 in clthept:
                        sl2,d2 = clthep2.split("Ф")
                        sl2 = int(sl2)
                        d2 = int(d2)
                        dientich2= (sl2 * math.pi *d2**2)/4
                        Ast += dientich2/100
                    anpha = (aEs/aEb)
                    yt = (b*h*h/2+anpha*Asd*100*a+anpha*Ast*100*h1)/(b*h+anpha*Ast*100+Asd*100*anpha)
                    Ired = (((b*h**3)/12)+b*h*((h/2)-yt)**2+anpha*(Asd*100*(h0-yt)**2)+anpha*(Ast*100*(yt-a1)**2))/(1000**4)
                    Ared = (b*h+anpha*Asd*100+anpha*Ast*100)/(1000**2)
                    phi = 0.3
                    y = 1.3
                    Stred = (b*h*h/2+anpha*Asd*100*a+anpha*Ast*100*h1)/1000**3
                    Muys = Asd/(b*h0/100)
                    Muys1 = Ast/(b*h1/100)
                    anphas1 = (0.0015*aEs)/aRbser
                    anphas2 = (0.0015*aEs)/aRbser
                    yc = h0*(((Muys*anphas2+Muys1*anphas1)**2+2*(Muys*anphas2+Muys1*anphas1*a1/h0))**0.5-(Muys*anphas2+Muys1*anphas1))
                    dmax = max(d1,d2)
                    hbt = min(max((h-yc),(2*a)),0.5*h)
                    Abt = b*hbt
                    Ls = (0.5*Abt*dmax)/(Asd*100)
                    Ls = min(Ls,min(40*dmax,400))
                    Ls = max(Ls,min(10*dmax,100))
                    Ls = Ls/1000
                    Mcrc = (y*Ared*Ired*aRbtser*1000)/Stred
                    if Mcrc>= mtp:
                        kqkiemtranut = "Không thỏa mãn điều kiện hình thành vết nứt"
                    else:
                        kqkiemtranut = "Thỏa mãn điều kiện hình thành vết nứt"
                    phi11 = 1.4
                    phi12 = 0.5
                    phi13 = 1
                    si = 1
                    Iredcrc = (b*yc**3/3+Asd*100*anphas1*(h0-yc)**2+Ast*100*anphas2*(yc-a1)**2)/1000**4
                    sigma1 = mdh*(h0-yc)/1000*anphas1/Iredcrc
                    acrc1 = phi11*phi12*phi13*si*sigma1*Ls/(aEs*1000)*1000
                    phi21 =1
                    phi22 =0.5
                    phi23= 1
                    sigma2 = mtp*(h0-yc)/1000*anphas1/Iredcrc
                    acrc2 = phi21*phi22*phi23*si*sigma2*Ls/(aEs*1000)*1000
                    phi31 = 1
                    phi32 = 0.5
                    phi33 = 1
                    sigma3 = mnh*(h0-yc)/1000*anphas1/Iredcrc
                    acrc3 = phi31*phi32*phi33*si*sigma3*Ls/(aEs*1000)*1000
                    acrcdh = acrc1
                    acrcnh = acrc1+acrc2-acrc3
                    if acrcdh<0.3:
                        kqkiemtradh = "Đảm bảo điều kiện bề rộng vết nứt dài hạn (Bảng 17 TCVN 5574:2018)"
                    else:
                        kqkiemtradh = "Không đảm bảo điều kiện vết nứt dài hạn (Bảng 17 TCVN 5574:2018)"
                    
                    if acrcnh<0.4:
                        kqkiemtranh="Đảm bảo điều kiện bề rộng vết nứt dài hạn (Bảng 17 TCVN 5574:2018)"
                    else:
                        kqkiemtranh="Không đảm bảo điều kiện bề rộng vết nứt dài hạn (Bảng 17 TCVN 5574:2018)"
                    context= {
                        'Mcrc':Mcrc,
                        'acrcdh':acrcdh,
                        'acrcnh':acrcnh,
                        'kqkiemtranut':kqkiemtranut,
                        'kqkiemtranh': kqkiemtranh,
                        'kqkiemtradh':kqkiemtradh,
                    }
                    return render(request, 'Webtinhnut/tinhvetnut.html', context)
                except (Tinhnut.DoesNotExist, Exception) as error:  
                    context = {'error': str(error)}
                    return render(request, 'Webtinhnut/tinhvetnut.html', context)

    list_caukien = []
    try:
        caukien = Tinhnut.objects.all().values_list('name', flat=True)  
        list_caukien = list(caukien)  
    except Exception as error:
        print(error)
    context = {'caukien': list_caukien}
    return render(request, 'Webtinhnut/tinhvetnut.html',context)


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