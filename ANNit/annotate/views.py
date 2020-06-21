from django.http import HttpResponse
from .models import Entry, Choice

def index(request):
    all_entries = Entry.objects.all()
    count_total_entries = len(all_entries)

    to_anno_entries = [a for a in all_entries if a.needs_anno()]
    output = ', '.join([q.URI_text for q in to_anno_entries])
    return HttpResponse(output + ' totoal=' + str(count_total_entries) + '; to decide=' + str(count_total_entries))


def detail(request, entry_id):
    return HttpResponse("You're looking at entry %s." % entry_id)

def results(request, entry_id):
    response = "You're looking at the results of entry %s."
    return HttpResponse(response % entry_id)

def decide(request, entry_id):
    return HttpResponse("You've submit your decision on entry %s." % entry_id)
