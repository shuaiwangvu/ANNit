from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. Please tell me where the nodes are. \nReady to annotate the nodes.")

def detail(request, entry_id):
    return HttpResponse("You're looking at entry %s." % entry_id)

def results(request, entry_id):
    response = "You're looking at the results of entry %s."
    return HttpResponse(response % entry_id)

def decide(request, entry_id):
    return HttpResponse("You've submit your decision on entry %s." % entry_id)
