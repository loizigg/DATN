from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='Webtinhnut'),
    path('caukien', views.caukien, name='caukien'),
    path('add-caukien', views.add_caukien, name='add-caukien'),
    path('edit-caukien/<int:id>',views.edit_caukien,name='edit-caukien'),
    path('delete-caukien/<int:id>',views.delete_caukien,name='delete-caukien'),
    path('tinhmomen',views.tinhmomen,name='tinhmomen'),
    path('tinhvetvut',views.tinhvetnut,name='tinhvetnut'),
]
