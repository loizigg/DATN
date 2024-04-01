from django.shortcuts import render,redirect

# Create your views here.
def index(request):
    return render(request, 'Webtinhnut/index.html')
def caukien(request):
    return render(request,'Webtinhnut/caukien.html')
def add_caukien(request):
    return render(request,'Webtinhnut/add-caukien.html')



def tinhmomen(request):
    return render(request, 'Webtinhnut/tinhmomen.html')



def tinhvetnut(request):
    return render(request, 'Webtinhnut/tinhvetnut.html')
