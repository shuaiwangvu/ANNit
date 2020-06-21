from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. Please tell me where the nodes are. \nReady to annotate the nodes.")
