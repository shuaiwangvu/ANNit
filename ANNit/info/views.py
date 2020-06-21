from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("This is the info page. Click start to import files")
