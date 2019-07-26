from django.urls import path, re_path
from booktest import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'index$', views.index, name='index'),
    #path('show/<str:book_id>', views.show, name='show'),
    re_path(r'show/(?P<id>\d+)', views.show, name='show'),
    path('login', views.login, name='login'),
    path('login_check', views.login_check, name='login_check'),
    path('login_out', views.login_out, name='login_out'),
    re_path(r'^create$', views.create, name='create'),
    re_path(r'^areas$', views.areas, name='areas'),
    path('herocreate/<int:book_id>/', views.herocreate, name='herocreate'),
    path('detail/<int:book_id>/', views.detail, name='detail'),
    path('delete/book<int:book_id>/', views.bookdelete, name="bookdelete"),

]
