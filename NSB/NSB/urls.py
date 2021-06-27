"""NSB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

#id이런 값을 html에서 받을때 받아야함 그래야 view에 있는 함수들을 실행할 수 있다

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name="home"),
    path('login/',views.login,name="login"),

    path('user/<int:id>',views.user_read,name="user_read"),
    path('user/new',views.user_create,name="user_create"),

    path('service/<int:id>', views.service_read, name="service_read"),
    path('service/new', views.service_create, name="service_create"),

    path('service/<str:service_upload_id>/evalu/<int:id>', views.s_evalu_read, name="s_evalu_read"),
    path('service/<int:id>/evalu/new', views.s_evalu_create, name="s_evalu_create"), # id가 service의 값으로 들어오는 것 같음
]
