from django.shortcuts import render
from django.views.generic.list import ListView
from psusphere.models import Organization

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"