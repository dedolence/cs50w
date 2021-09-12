from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='pathName_index'),
    path('login', views.login_view, name='pathName_login'),
    path('logout', views.logout_view, name='pathName_logout')
]