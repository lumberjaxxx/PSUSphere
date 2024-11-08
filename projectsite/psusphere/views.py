from django.shortcuts import render
from django.views.generic.list import ListView 
from django.views.generic.edit import CreateView 
from psusphere.models import Organization
from psusphere.forms import OrganizationForm
from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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
            qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))
            
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "org_form.html"
    success_url = reverse_lazy('org_list')