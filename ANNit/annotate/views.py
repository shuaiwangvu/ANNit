from django.http import HttpResponse
from .models import Entry, Choice
from django.template import loader
from django.views.generic import CreateView
from django.shortcuts import render

# def index(request):
#     all_entries = Entry.objects.all()
#     count_total_entries = len(all_entries)
#
#     to_anno_entries = [a for a in all_entries if a.needs_anno()]
#     output = ', '.join([q.URI_text for q in to_anno_entries])
# #     return HttpResponse(output + ' totoal=' + str(count_total_entries) + '; to decide=' + str(count_total_entries))
# #
# #
# # def index(request):
# #     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('annotate/index.html')
#     context = {
#         'latest_question_list': all_entries,
#     }
#     return HttpResponse(template.render(context, request))

def index(request):
    all_entries = Entry.objects.all()
    context = {'all_entries': all_entries}
    return render(request, 'annotate/index.html', context)

# def detail(request, entry_id):
#     return HttpResponse("You're looking at entry %s." % entry_id)

def detail(request, entry_id):
    try:
        entry = Entry.objects.get(pk=entry_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'annotate/detail.html', {'entry': entry})

def results(request, entry_id):
    response = "You're looking at the results of entry %s."
    return HttpResponse(response % entry_id)

def decide(request, entry_id):
    return HttpResponse("You've submit your decision on entry %s." % entry_id)
