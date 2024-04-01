from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='Webtinhnut'),
    path('caukien', views.caukien, name='caukien'),
    path('add-caukien', views.add_caukien, name='add-caukien'),
    path('tinhmomne',views.tinhmomen,name='tinhmomen'),
    path('tinhvetvut',views.tinhvetnut,name='tinhvetnut'),
]
