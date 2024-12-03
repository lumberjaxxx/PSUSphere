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
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
                            Q(description__icontains=query))
        return qs 
                            

class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super(). get_context_data(**kwargs)
        return context
    
    def get_queryset(self, *args, **kwargs):
        pass 

def PieCountbySeverity(request):
    query = '''
        SELECT severity_level, COUNT(*) as count
        FROM fire_incident
        GROUP BY severity_level
    '''  
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    
    if rows:
        # Construct the dictionary with severity level as keys and count as values
        data = {severity: count for severity, count in rows}
    else:
        data = {}
    
    return JsonResponse(data)

def LineCountbyMonth(request):
    current_year = datetime.now().year
    result = {month: 0 for month in range (1, 13)}

    incidents_per_month = Incident.objects.filter.filter(date_time__year=current_year) \
        .values_list('date_time',flat=True)
    
    #counting the number of incidents per month

    for date_time in incidents_per_month:
        month = date_time.month
        result[month] +=1

    #convert month numbers into month name
    month_names = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4:'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }

    result_with_month_names = {
        month_names[int(month)]: count for month,  count in result.items()}
    
    return JsonResponse(result_with_month_names)

def MultilineIncidentTop3Country(request):
    query = '''
        SELECT 
        fl.country,
        strftime('%m, fi.date_time) AS month,
        COUNT(fi.id) AS incident_count
    FROM
        fire_incident fi
    JOIN
        fire_locations fl ON fi.location_id=fl.id
    WHERE
        fl.country IN(
            SELECT
                fl_top.country
            FROM
                fire_incident fi_top
            JOIN 
                fire_locations fl_top ON fi_top.location_id = fl_top.id
            WHERE
                strftime('%Y', fi_top.date_time) = strftime('%y', 'now')
            GROUP BY
                fl_top.country
            ORDER BY
                COUNT(fi_top.id) DESC
            LIMIT 3
            )
        AND strftime ('%Y', fi.date_time) = strftime('%Y', 'now')
    GROUP BY
        fl.country, month
    ORDER BY
        fl.country, month
    '''
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    #initialize a dictionary to store the result
    result = {}

    #initialize a set of months from Jan to dec
    months = set(str(1).zfill(2) for i in range (1, 13))

    #loop through query results
    for row in rows:
        country = row[0]
        month = row[1]
        total_incidents = row[2]

        if country not in result:
            result[country] - {month: 0 for month in months}
        result[country][month] = total_incidents
    while len(result) < 3:
        missing_country = f"Country{len(result) + 1}"
        result[missing_country] = {month: 0 for month in months}

    for country in result:
        result[country] = dict(sorted(result[country].items()))
    return JsonResponse

def multipleBarbySeverity(request):
    query = '''
    SELECT
        fl.severity_level,
        strftime('%m', fi.data_time) AS month,
        COUNT(fi.id) AS incident_count
    FROM
        fire_incident fi
    GROUP BY fi.severity_level, month
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    result = {}
    months = set(str(i).zfill(2) for i in range (1, 13))

    for row in rows:
        level = str(row[0])
        month = row[1]
        total_incidents = row[2]

        if level not in result:
            result[level] = {month: 0 for month in months}
        result[level][month] = total_incidents
    for level in result:
        result[level] = dict(sorted(result[level].items()))

    return JsonResponse

def map_incidents(request):
     incidents = Incident.objects.select_related("location").values(
          "location_name", "location_latitude", "location_longitude", 
          "date_time", "severity_level", "description"
     )

     incidents_list = [
          {
               "name": incident["location_name"],
               "latitude": float(incident["location_latitude"]),
               "longitude": float(incident["location_longitude"]),
               "date_time": incident["date_time"].strftime("%Y-%m-%d %H:%H:%S") if incident["date_time"] else "N/A",
               "severity_level": incident["severity_level"],
               "description": incident["description"],
          }
          for incident in incidents
     ]
     return render(request, "map_incidents.html", {"fireIncidents": incidents_list})

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


class OrganizationUpdateView(UpdateView):
    model = Organization
    fields = "__all__"
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
        college_name = form.instance
        messages.success(self.request, f'{college_name} has been successfully updated.')

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
        prog_name = form.instance
        messages.success(self.request, f'{prog_name} has been successfully updated.')

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
  