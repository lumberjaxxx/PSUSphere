"""
URL configuration for projectsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, re_path
from psusphere import views
from django.contrib.auth import views as auth_views
from psusphere.views import HomePageView, OrganizationList, OrganizationCreateView, OrgMemberList, StudentList, ProgramList, CollegeList


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name="home"),
    path('orglist/', OrganizationList.as_view(), name='org_list'),
    path('orglist/add/', OrganizationCreateView.as_view(), name='org_add'),
    re_path(r'^login/$',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    path('org_mem/', OrgMemberList.as_view(), name="org_mem"),
    path('student/', StudentList.as_view(), name="student"),
    path('program/', ProgramList.as_view(), name='program'),
    path('college', CollegeList.as_view(), name='college')

]
