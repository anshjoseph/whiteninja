"""WhiteNinjaesp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from accounts import views as acc_views
from management import views as man_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',acc_views.register,name="register"),
    path('',acc_views.login_pg,name="login"),
    path("profile/",acc_views.profile_page,name="profile"),
    path("change_profile/",acc_views.change_profile,name="change_profile"),
    path("ch_us_id_pg/",acc_views.ch_pg,name="ch_pg"),
    path("ch_us_id_ff/",acc_views.ch_ff,name="ch_ff"),
    path("logout/",acc_views.user_logout,name="logout"),
    path("take_part/",man_views.part,name="particepant"),
    path("mem_data/",man_views.data_part,name="data"),
    path("parts/",man_views.ac_part,name="part"),
    path("del/",acc_views.leave_team,name="le_tm"),
    path("get_data/",man_views.get_data,name="data"),
    path("diojhsk/",man_views.get_doc,name="doc")
]
