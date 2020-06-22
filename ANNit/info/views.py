from django.http import HttpResponse, HttpResponseRedirect

from django.template import loader
from django.views.generic import CreateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

# def index(request):
#     return HttpResponse("This is the info page. Click start to import files")


def index(request):
    return render(request, 'info/index.html', {})
