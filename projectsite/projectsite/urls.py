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
from psusphere.views import OrganizationList, OrganizationCreateView, OrgMemberList, StudentList, ProgramList, CollegeList, OrgMemberCreateView, StudentCreateView, ProgramCreateView, CollegeCreateView
from psusphere.views import OrganizationUpdateView, OrgMemberUpdateView, CollegeUpdateView, ProgramUpdateView, StudentUpdateView
from psusphere.views import OrganizationUpdateView, OrgMemberUpdateView, CollegeUpdateView, ProgramUpdateView, StudentUpdateView
from psusphere.views import OrganizationDeleteView, OrgMemberDeleteView,StudentDeleteView,ProgramDeleteView,CollegeDeleteView

from psusphere.views import HomePageView, ChartView, PieCountbyStudent, LineCountbyMonth,timeline_of_org, popular_organization, barcountStudent,CircleCountbyStudent

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name="home"), #home
    path('dashboard_chart', ChartView.as_view(), name='dashboard-chart'),
    path('home/piechart/', PieCountbyStudent, name='pie-chart'),
    path('home/lineChart/', LineCountbyMonth, name='line-chart'),
    path('home/barChart/', barcountStudent, name='barchart'),
    path('home/doughnut/', CircleCountbyStudent, name='doughnut'),



    path('orglist/', OrganizationList.as_view(), name='org_list'),
    path('orglist/add/', OrganizationCreateView.as_view(), name='org_add'),  ##### adding in forms
    path('orglist/<pk>/edit', OrganizationUpdateView.as_view(), name='org_edit'),
    path('orglist/<pk>/delete', OrganizationDeleteView.as_view(), name='org_del'),

    re_path(r'^login/$',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    path('org_mem/', OrgMemberList.as_view(), name="org_mem"),
    path('orgmem/add/', OrgMemberCreateView.as_view(), name='orgmem_add'),
    path('orgmem/<pk>/edit', OrgMemberUpdateView.as_view(), name='orgmem_edit'),
    path('orgmem/<pk>/delete', OrgMemberDeleteView.as_view(), name='orgmem_del'),

    path('student/', StudentList.as_view(), name="student"),
    path('student/add/', StudentCreateView.as_view(), name='student_add'),
    path('student/<pk>/edit', OrganizationUpdateView.as_view(), name='student_edit'),
    path('student/<pk>/delete', StudentDeleteView.as_view(), name='student_del'),

    path('program/', ProgramList.as_view(), name='program'),
    path('program/add/', ProgramCreateView.as_view(), name='program_add'),
    path('program/<pk>/edit', ProgramUpdateView.as_view(), name='program_edit'),
    path('program/<pk>/edit', ProgramDeleteView.as_view(), name='program_del'),

    path('college/', CollegeList.as_view(), name='college'),
    path('college/add/', CollegeCreateView.as_view(), name='college_add'),
    path('college/<pk>/edit/', CollegeUpdateView.as_view(), name='college_edit'),
    path('college/<pk>/delete/', CollegeDeleteView.as_view(), name='college_del'),

]
