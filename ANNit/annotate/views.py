from django.http import HttpResponse, HttpResponseRedirect
from .models import Entry, Choice
from django.template import loader
from django.views.generic import CreateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

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
    all_choices = Choice.objects.all()
    context = {'all_entries': all_entries, 'all_choices':all_choices}
    return render(request, 'annotate/index.html', context)

# def detail(request, entry_id):
#     return HttpResponse("You're looking at entry %s." % entry_id)

def detail(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    all_choices = Choice.objects.all()
    print ('Amount of choices ', len (all_choices))
    return render(request, 'annotate/detail.html', {'entry': entry, 'all_choices': all_choices})

def results(request, entry_id):
    response = "You're looking at the results of entry %s."
    return HttpResponse(response % entry_id)

# def decide(request, entry_id):
#     return HttpResponse("You've submit your decision on entry %s." % entry_id)


def decide(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    all_choices = Choice.objects.all()
    try:
        selected_choice = all_choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'annotate/detail.html', {
            'entry': entry,
            'error_message': "You didn't select a choice.",
        })
    else:
        entry.user_choice = selected_choice.choice_text
        print ('chosen: ', selected_choice.choice_text)
        entry.save()
        # selected_choice.votes += 1
        # selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('annotate:results', args=(entry.id,)))


def results(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    all_choices = Choice.objects.all()
    return render(request, 'annotate/results.html', {'entry': entry, 'all_choices':all_choices})
