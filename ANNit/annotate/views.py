from django.http import HttpResponse, HttpResponseRedirect
from .models import Entry, Choice
from django.template import loader
from django.views.generic import CreateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import csv

path_to_csv_file = ''

def load_entries(path):
    global path_to_csv_file
    path_to_csv_file = path
    Entry.objects.all().delete()
    my_id = 0
    with open(path) as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # print(row['Entity']) # [1:-1]
            e = Entry(id = my_id)
            e.URI_text = row['Entity']
            e.save()
            my_id += 1
    Choice.objects.all().delete()

def load_entries_examination(path):
    Choice.objects.all().delete()
    global path_to_csv_file
    path_to_csv_file = path
    Entry.objects.all().delete()
    collect_annotations = set()
    my_id = 0
    with open(path) as file:
        csv_reader = csv.DictReader(file, delimiter="\t")
        for row in csv_reader:
            e = Entry(id = my_id)
            e.URI_text = row['Entity']
            e.user_choice = row['Annotation']
            e.comment = row['Comment']
            print('Entity: ', row['Entity']) # [1:-1]
            print('Annotation: ', row['Annotation']) # [1:-1]
            print('Comment: ', row['Comment']) # [1:-1]
            # e = Entry(URI_text = row['Entity'], exist_choice = row['Annotation'], exist_comment = row['Comment'])
            e.save()
            my_id += 1
            # collect_annotations.add(row['Annotation'])
            new_anno = row['Annotation']
            if new_anno not in [s.choice_text for s in Choice.objects.all()] :
                c = Choice(choice_text = new_anno)
                c.save()
    print ('total choices/annotations', len(list(Choice.objects.all())))
    print ('total entires loaded', len(list(Entry.objects.all())))


def export(request):
    global path_to_csv_file
    print('path to csv file',path_to_csv_file)
    export_full_name = path_to_csv_file +'.export'
    if 'csv' in path_to_csv_file:
        export_full_name = path_to_csv_file[:path_to_csv_file.rfind('/')+1] + path_to_csv_file[path_to_csv_file.rfind('/')+1:][:-4] + '_Annotated.tsv' # change it to TSV file.
    elif 'tsv' in path_to_csv_file:
        export_full_name = path_to_csv_file[:path_to_csv_file.rfind('/')+1] + path_to_csv_file[path_to_csv_file.rfind('/')+1:][:-4] + '_Verified.tsv' # change it to TSV file.
    with open(export_full_name, "w+") as file:
        writer = csv.writer(file,delimiter='\t')
        writer.writerow([ "Entity", "Annotation", "Comment"])
        all_entries = Entry.objects.all()
        for e in all_entries:
            writer.writerow([e.URI_text, e.user_choice, e.comment])
    print ('exported to: ', export_full_name)
    all_entries = Entry.objects.all()
    all_choices = Choice.objects.all()
    context = {'all_entries': all_entries, 'all_choices':all_choices}
    return render(request, 'annotate/index.html', context)

def next_entry(request, entry_id):
    # unless all got annotated
    all_entries = Entry.objects.all()
    amount_entry = len(all_entries)
    all_choices = Choice.objects.all()
    amount_choice = len (all_choices)

    if entry_id < max([e.id for e in all_entries]):
        entry_id += 1
    else:
        print ('All finished!')
    entry = get_object_or_404(Entry, pk=entry_id)
    return render(request, 'annotate/detail.html', {'entry': entry, 'all_choices': all_choices})

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

def load (request):
    global path_to_csv_file
    all_entries = Entry.objects.all()
    amount_entry = len(all_entries)
    all_choices = Choice.objects.all()
    amount_choice = len (all_choices)

    path_to_csv_file = request.POST['u_name'] # u_name is the name of the input tag
    if 'tsv' in path_to_csv_file:
        if path_to_csv_file != None and path_to_csv_file != '':
            print ('examining tsv: load the file at = ', path_to_csv_file)
            existing_annos = load_entries_examination(path_to_csv_file)

    elif 'csv' in path_to_csv_file:
        if path_to_csv_file != None and path_to_csv_file != '':
            print ('load the file at = ', path_to_csv_file)
            load_entries(path_to_csv_file)

    new_anno = request.POST['a_name'] # u_name is the name of the input tag
    if new_anno != None and new_anno != '':
        print ('new annotate = ', new_anno)
        if new_anno not in [s.choice_text for s in Choice.objects.all()] :
            e = Choice(choice_text = new_anno)
            e.save()


    # if request.POST['clear_names']:
    #     print ('REMOVE ALL NAMES')
    #     Choice.objects.all().delete()

    context = {'all_entries': all_entries, 'amount_entry':amount_entry, 'all_choices':all_choices, 'path':path_to_csv_file,'amount_choice':amount_choice}
    return render(request, 'annotate/index.html', context)

# def detail(request, entry_id):
#     return HttpResponse("You're looking at entry %s." % entry_id)

def detail(request, entry_id):
    print ('There are in total ', len (Entry.objects.all()), ' entries.')
    # entry = get_object_or_404(Entry, pk=entry_id)
    entry = Entry.objects.get(pk=entry_id)
    all_choices = Choice.objects.all()
    # print ('Amount of choices ', len (all_choices))
    return render(request, 'annotate/detail.html', {'entry': entry, 'all_choices': all_choices})

# def results(request, entry_id):
#     response = "You're looking at the results of entry %s."
#     return HttpResponse(response % entry_id)
    # todo : redirect?

# def decide(request, entry_id):
#     return HttpResponse("You've submit your decision on entry %s." % entry_id)


def decide(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    all_choices = Choice.objects.all()

    # is_private = request.POST.get('is_private', False)
    comment = request.POST.get('comment', False) # u_name is the name of the input tag
    if comment != None and comment != '' and comment != False:
        print('Comment:', comment)
        entry.comment = comment
        entry.save()
    else:
        entry.comment = 'TBA'
        entry.save()


    try:
        selected_choice = all_choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.

        new_anno = request.POST['a_name'] # u_name is the name of the input tag
        if new_anno != None and new_anno != '':
            print('Add new annotation:', new_anno)
            if new_anno not in [s.choice_text for s in Choice.objects.all()] :
                c = Choice(choice_text = new_anno)
                c.save()
            entry.user_choice = new_anno
            print ('chosen: ', new_anno)
            entry.save()
            # selected_choice.votes += 1
            # selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('annotate:results', args=(entry.id,)))
        else:
            print ('ERROR')
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
#
# def next_entry (request, entry_id):
#     return HttpResponseRedirect(reverse('annotate:detail', args=(entry.id +1,)))
