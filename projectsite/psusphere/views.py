from django.shortcuts import render
from django.views.generic.list import ListView 
from django.views.generic.edit import CreateView 
from psusphere.models import Organization
from psusphere.forms import OrganizationForm
from django.urls import reverse_lazy

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class OrganizationList(ListView):
    model = Organization
    context_object_name = "organization"
    template_name = "org_list.html"
    paginated_by = 5

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "org_form.html"
    success_url = reverse_lazy('org_list')