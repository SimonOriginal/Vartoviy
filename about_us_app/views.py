from django.shortcuts import render
from .models import Project, Developer, FAQ

def about(request):
    project = Project.objects.first()
    developers = Developer.objects.all()
    faqs = FAQ.objects.all()
    return render(request, 'about_us/about.html', {'project': project, 'developers': developers, 'faqs': faqs})
