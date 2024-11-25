from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from psusphere.models import Organization, Student, OrgMember, Program, College
from psusphere.forms import OrganizationForm, OrgMemberForm, StudentForm, ProgramForm, CollegeForm
from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

method_decorator(login_required, name='dispatch')

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class OrganizationList(ListView):
    model = Organization
    context_object_name = "organization"
    template_name = "org_list.html"
    paginated_by = 5

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
    template_name = "org_form.html"
    success_url = reverse_lazy('org_list')

    def form_valid(self,form):
        org_name = form.instance
        messages.success(self.request, f'{org_name} has been successfully updated.')

        return super().form_valid(form)


class OrganizationUpdateView(UpdateView):
    model = Organization
    fields = "__all__"
    context_object_name = "organization"
    template_name = "org_edit_form.html"
    success_url = reverse_lazy('org_list')


###############Organization member starts #########################
class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = "org_mem"
    template_name = "org_mem.html"
    paginated = 2

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
    template_name = "orgmem_form.html"
    success_url = reverse_lazy('org_mem')

    def form_valid(self,form):
        orgmem= form.instance
        messages.success(self.request, f'{orgmem} has been successfully updated.')

        return super().form_valid(form)

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    fields = "__all__"
    context_object_name = "org_mem"
    template_name = "orgmem_form.html"
    success_url = reverse_lazy('org_mem')

    
############# Student list starts#######################333333
class StudentList(ListView):
    model = Student
    context_object_name = "student"
    template_name = "student.html"
    paginated = 5
    
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
    template_name = "student_form.html"
    success_url = reverse_lazy('student')


    def form_valid(self,form):
        student_name = form.instance
        messages.success(self.request, f'{Student} has been successfully updated.')

        return super().form_valid(form)



class StudentUpdateView(UpdateView):
    model = Student
    fields = "__all__"
    context_object_name = "student"
    template_name = "stud_edit_form.html"
    success_url = reverse_lazy('student')


##################### College Starts ########################33
class CollegeList(ListView):
    model = College
    context_object_name = "college"
    template_name = "college.html"
    paginated = 3

    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(college_name__icontains=query))
            
        return qs
    

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = "college_form.html"
    success_url = reverse_lazy('college')

    def form_valid(self,form):
        college_name = form.instance
        messages.success(self.request, f'{college_name} has been successfully updated.')

        return super().form_valid(form)



class CollegeUpdateView(UpdateView):
    model = College
    fields = "__all__"
    context_object_name = "college"
    template_name = "college_form.html"
    success_url = reverse_lazy('college')


############################# Program Starts ##############

class ProgramList(ListView):
    model = Program
    context_object_name = "program"
    template_name = "program.html"
    paginated = 2

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
    template_name = "program_form.html"
    success_url = reverse_lazy('program')


    def form_valid(self,form):
        prog_name = form.instance
        messages.success(self.request, f'{Program} has been successfully updated.')

        return super().form_valid(form)

class ProgramUpdateView(UpdateView):
    model = Program
    fields = "__all__"
    context_object_name = "program"
    template_name = "program_form.html"
    success_url = reverse_lazy('program')
  