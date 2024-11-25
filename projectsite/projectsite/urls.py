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
from psusphere.views import HomePageView, OrganizationList, OrganizationCreateView, OrgMemberList, StudentList, ProgramList, CollegeList, OrgMemberCreateView, StudentCreateView, ProgramCreateView, CollegeCreateView
from psusphere.views import OrganizationUpdateView, OrgMemberUpdateView, CollegeUpdateView, ProgramUpdateView, StudentUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name="home"), #home

    path('orglist/', OrganizationList.as_view(), name='org_list'),
    path('orglist/add/', OrganizationCreateView.as_view(), name='org_add'),  ##### adding in forms
    path('orglist/edit/<pk>/', OrganizationUpdateView.as_view(), name='org_edit'),

    re_path(r'^login/$',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    path('org_mem/', OrgMemberList.as_view(), name="org_mem"),
    path('orgmem/add/', OrgMemberCreateView.as_view(), name='orgmem_add'),
    path('orgmem/edit/', OrganizationUpdateView.as_view(), name='orgmem_edit'),

    path('student/', StudentList.as_view(), name="student"),
    path('student/add/', StudentCreateView.as_view(), name='student_add'),
    path('student/edit/', OrganizationUpdateView.as_view(), name='student_edit'),

    path('program/', ProgramList.as_view(), name='program'),
    path('program/add/', ProgramCreateView.as_view(), name='program_add'),
    path('program/edit/', OrganizationUpdateView.as_view(), name='program_edit'),

    path('college', CollegeList.as_view(), name='college'),
    path('college/add/', CollegeCreateView.as_view(), name='college_add'),
    path('college/edit/', OrganizationUpdateView.as_view(), name='college_edit'),
]
