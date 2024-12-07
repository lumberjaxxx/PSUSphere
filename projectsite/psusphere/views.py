from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from psusphere.models import Organization, Student, OrgMember, Program, College
from psusphere.forms import OrganizationForm, OrgMemberForm, StudentForm, ProgramForm, CollegeForm
from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db import connection
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth

from django.db.models import Count
from datetime import datetime


method_decorator(login_required, name='dispatch')

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class ChartView(ListView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(). get_context_data(**kwargs)
        return context
    
    def get_queryset(self, *args, **kwargs):
        pass 

def PieCountbyStudent(request):
    query = '''
    SELECT 
        p.prog_name AS program_name, 
        COUNT(s.id) AS student_count
    FROM 
        psusphere_student AS s
    JOIN 
        psusphere_program AS p ON s.program_id = p.id 
    GROUP BY 
        p.prog_name;
    '''  
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    
    if rows:
        # Construct the dictionary with severity level as keys and count as values
        data = {program_name: student_count for program_name, student_count in rows}
    else:
        data = {}
    
    return JsonResponse(data)

def barcountStudent(request):
    query = '''
    SELECT 
        p.prog_name AS program_name, 
        COUNT(s.id) AS student_count
    FROM 
        psusphere_student AS s
    JOIN 
        psusphere_program AS p ON s.program_id = p.id 
    GROUP BY 
        p.prog_name;
    '''  
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    
    if rows:
        # Construct the dictionary with severity level as keys and count as values
        data = {program_name: student_count for program_name, student_count in rows}
    else:
        data = {}
    
    return JsonResponse(data)


def LineCountbyMonth(request):
    current_year = datetime.now().year
    result = {month: 0 for month in range (1, 13)}

    members_per_month = OrgMember.objects.filter(date_joined__year=current_year) \
        .values_list('date_joined',flat=True)
    
    #counting the number of incidents per month

    for date_joined in members_per_month:
        if date_joined:
            month = date_joined.month
            result[month] +=1

    #convert month numbers into month name
    month_names = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4:'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }

    result_with_month_names = {
        month_names[int(month)]: count for month,  count in result.items()}
    
    return JsonResponse(result_with_month_names)

def timeline_of_org(request): #multiline
    data = (
        OrgMember.objects.values('date_joined')
        .annotate(member_count=Count('id'))
        .order_by('date_joined')
    )
        
    labels = [entry['date_joined'].strftime('%Y-%m-%d') for entry in data]
    counts = [entry['member_count'] for entry in data]

    response_data = {
        "labels": labels,  
        "datasets": [
            {
                "label": "New Members",
                "data": counts,  
                "backgroundColor": "rgba(54, 162, 235, 0.5)",  
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 1,
            }
        ],
    }

    return JsonResponse(response_data)

def popular_organization(request): #circle graph
    data = (
        OrgMember.objects
        .values('organization__college__college_name', 'organization__name')
        .annotate(member_count=Count('id'))
        .order_by('organization__college__college_name', '-member_count')
    )


    college_data = {}
    for entry in data:
        college_name = entry['organization__college__college_name']
        organization_name = entry['organization__name']
        member_count = entry['member_count']

        if college_name not in college_data:
            college_data[college_name] = {
                "organization": organization_name,
                "members": member_count
            }


    labels = list(college_data.keys())  
    counts = [info['members'] for info in college_data.values()]  
    organizations = [info['organization'] for info in college_data.values()]  

    response_data = {
        "labels": labels,
        "datasets": [
            {
                "label": "Most Popular Organization",
                "data": counts,  
                "backgroundColor": "rgba(75, 192, 192, 0.5)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1,
            }
        ],
        "organization_names": organizations, 
    }

    return JsonResponse(response_data)

class OrganizationList(ListView):
    model = Organization
    context_object_name = "organization"
    template_name = "organization/org_list.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)|
                Q(college__college_name__icontains=query))
            
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "organization/org_form.html"
    success_url = reverse_lazy('org_list')

    def form_valid(self,form):
        name = form.instance.name
        messages.success(self.request, f'{name} has been successfully added.')

        return super().form_valid(form)


class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    context_object_name = "organization"
    template_name = "organization/org_edit_form.html"
    success_url = reverse_lazy('org_list')

    def form_valid(self,form):
        org_name = form.instance
        messages.success(self.request, f'{org_name} has been successfully updated.')

        return super().form_valid(form)

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = "organization/org_del.html"
    success_url = reverse_lazy('org_list')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully deleted.')
        return super().form_valid(form)


###############Organization member starts #########################
class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = "org_mem"
    template_name = "orgmember/org_mem.html"
    paginate_by = 2

    def get_queryset(self, *args, **kwargs):
        qs = super(OrgMemberList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                # Q(student____icontains=query) |
                Q(organization__name__icontains=query)|
                Q(date_joined__icontains=query)
                )
            
        return qs
    
class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = "orgmember/orgmem_form.html"
    success_url = reverse_lazy('org_mem')

    def form_valid(self,form):
        student = form.instance.student
        messages.success(self.request, f'{student} has been successfully added.')

        return super().form_valid(form)

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    fields = "__all__"
    context_object_name = "org_mem"
    template_name = "orgmember/orgmem_form.html"
    success_url = reverse_lazy('org_mem')

    def form_valid(self,form):
        orgmem= form.instance
        messages.success(self.request, f'{orgmem} has been successfully updated.')

        return super().form_valid(form)

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = "orgmember/orgmem_del.html"
    success_url = reverse_lazy('org_mem')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully deleted.')
        return super().form_valid(form)

    
############# Student list starts#######################333333
class StudentList(ListView):
    model = Student
    context_object_name = "student"
    template_name = "student/student.html"
    paginate_by = 5
    
    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(student_id__icontains=query) |
                Q(lastname__icontains=query) |
                Q(firstname__icontains=query) | 
                Q(middlename__icontains=query)|
                Q(program__prog_name__icontains=query) |
                Q(college__college_name__icontains=query)
                )
            
        return qs
    
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "student/student_form.html"
    success_url = reverse_lazy('student')


    def form_valid(self,form):
        student = form.instance.student_id
        messages.success(self.request, f'{student} has been successfully added.')

        return super().form_valid(form)



class StudentUpdateView(UpdateView):
    model = Student
    fields = "__all__"
    context_object_name = "student"
    template_name = "student/stud_edit_form.html"
    success_url = reverse_lazy('student')

    def form_valid(self,form):
        student_name = form.instance
        messages.success(self.request, f'{student_name} has been successfully updated.')

        return super().form_valid(form)
    
class StudentDeleteView(DeleteView):
    model = Student
    template_name = "student/student_del.html"
    success_url = reverse_lazy('student')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully deleted.')
        return super().form_valid(form)


##################### College Starts ########################33
class CollegeList(ListView):
    model = College
    context_object_name = "college"
    template_name = "college/college.html"
    paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(college_name__icontains=query))
            
        return qs
    

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = "college/college_form.html"
    success_url = reverse_lazy('college')

    def form_valid(self,form):
        college = form.instance.college_name
        messages.success(self.request, f'{college} has been successfully added.')

        return super().form_valid(form)



class CollegeUpdateView(UpdateView):
    model = College
    fields = "__all__"
    context_object_name = "college"
    template_name = "college/college_form.html"
    success_url = reverse_lazy('college')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = "college/college_del.html"
    success_url = reverse_lazy('college')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully deleted.')
        return super().form_valid(form)


############################# Program Starts ##############

class ProgramList(ListView):
    model = Program
    context_object_name = "program"
    template_name = "program/program.html"
    paginate_by = 2

    def get_queryset(self, *args, **kwargs):
        qs = super(ProgramList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(prog_name__icontains=query) | 
                Q(college__college_name__icontains=query))
            
        return qs
    
class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = "program/program_form.html"
    success_url = reverse_lazy('program')


    def form_valid(self,form):
        program = form.instance.prog_name
        messages.success(self.request, f'{program} has been successfully added.')

        return super().form_valid(form)

class ProgramUpdateView(UpdateView):
    model = Program
    fields = "__all__"
    context_object_name = "program"
    template_name = "program/program_form.html"
    success_url = reverse_lazy('program')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = "program/program_del.html"
    success_url = reverse_lazy('program')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully deleted.')
        return super().form_valid(form)
  