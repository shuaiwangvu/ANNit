# from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Entry, Choice
from django.template import loader
from django.views.generic import CreateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import csv
from urllib.parse import quote

path_to_csv_file = ''

def load_entries(path):
	global path_to_csv_file
	path_to_csv_file = path
	filename = path
	Entry.objects.all().delete()
	Choice.objects.all().delete()
	with open(filename, 'r', newline='') as csvfile:
		# csv_reader = csv.DictReader(file)
		csv_reader = csv.reader(csvfile, delimiter='\t')
		for row in csv_reader:
			print(row[0] +'\t\t'+ row[1]) # [1:-1]
			left_triply = quote(row[0],safe='')
			right_triply = quote(row[1],safe='')
			e = Entry(left_URI_text = row[0], right_URI_text = row[1], left_URI_text_triply = left_triply, right_URI_text_triply = right_triply)
			e.save()
	print ('There are in total ', Entry.objects.count(), ' entries')
		# equal =  'equal'
		# left_more_general = 'left>right'
		# right_more_general = 'left<right'
		# neither = 'neither'
		# unknown = 'unknown'
	e = Choice(choice_text = Choice.equal)
	e.save()
	e = Choice(choice_text = Choice.left_more_general)
	e.save()
	e = Choice(choice_text = Choice.right_more_general)
	e.save()
	e = Choice(choice_text = Choice.neither)
	e.save()
	e = Choice(choice_text = Choice.unknown)
	e.save()

def load_annotated_entries(path):
	global path_to_csv_file
	path_to_csv_file = path
	filename = path
	Entry.objects.all().delete()
	Choice.objects.all().delete()

	e = Choice(choice_text = Choice.equal)
	e.save()
	e = Choice(choice_text = Choice.left_more_general)
	e.save()
	e = Choice(choice_text = Choice.right_more_general)
	e.save()
	e = Choice(choice_text = Choice.neither)
	e.save()
	e = Choice(choice_text = Choice.unknown)
	e.save()

	dict_reader = csv.DictReader(open(filename, newline=''), delimiter='\t')
	for row in dict_reader:
		# print (row)
		left = row['LEFT']
		right = row['RIGHT']
		choice = row['UserChoice']
		decision = row['Decision']
		comment = row['Comment']
		left_triply = quote(left,safe='')
		right_triply = quote(right,safe='')
		e = Entry(left_URI_text = left, right_URI_text = right, left_URI_text_triply = left_triply, right_URI_text_triply = right_triply, user_choice = choice, user_decision = decision, comment = comment)
		e.save()

	print ('There are in total ', Entry.objects.count(), ' entries')


def export(request):
	global path_to_csv_file
	print('path to csv file', path_to_csv_file)
	# export_full_name = path_to_csv_file[:path_to_csv_file.rfind('/')+1] + path_to_csv_file[path_to_csv_file.rfind('/')+1:][:2] + 'pair_annotated.tsv' # change it to TSV file.
	export_full_name = path_to_csv_file + '_annotated.tsv' # change it to TSV file.
	with open(export_full_name, "w+") as file:
		writer = csv.writer(file,delimiter='\t')
		writer.writerow([ "LEFT", "RIGHT", "UserChoice", "Decision", "Comment"])
		all_entries = Entry.objects.all()
		for e in all_entries:
			writer.writerow([e.left_URI_text, e.right_URI_text, e.user_choice, e.user_decision, e.comment])
	print ('exported to: ', export_full_name)
	all_entries = Entry.objects.all()
	all_choices = Choice.objects.all()
	context = {'all_entries': all_entries, 'all_choices':all_choices}
	return render(request, 'pair/index.html', context)

def next_entry(request, entry_id):
	# unless all got paird
	all_entries = Entry.objects.all()
	amount_entry = len(all_entries)
	all_choices = Choice.objects.all()
	amount_choice = len (all_choices)

	if entry_id < max([e.id for e in all_entries]):
		entry_id += 1
	else:
		print ('All finished!')
	entry = get_object_or_404(Entry, pk=entry_id)
	return render(request, 'pair/detail.html', {'entry': entry, 'all_choices': all_choices})

def index(request):
	all_entries = Entry.objects.all()
	all_choices = Choice.objects.all()
	context = {'all_entries': all_entries, 'all_choices':all_choices}
	return render(request, 'pair/index.html', context)

def load (request):
	global path_to_csv_file
	all_entries = Entry.objects.all()
	amount_entry = len(all_entries)
	all_choices = Choice.objects.all()
	amount_choice = len (all_choices)

	path_to_csv_file = request.POST['u_name'] # u_name is the name of the input tag
	if path_to_csv_file != None and path_to_csv_file != '':
		print ('load the file at = ', path_to_csv_file)
		load_entries(path_to_csv_file)

	new_anno = request.POST['a_name'] # u_name is the name of the input tag
	if new_anno != None and new_anno != '':
		print ('new pair = ', new_anno)
		if new_anno not in [s.choice_text for s in Choice.objects.all()] :
			e = Choice(choice_text = new_anno)
			e.save()

	context = {'all_entries': all_entries, 'amount_entry':amount_entry, 'all_choices':all_choices, 'path':path_to_csv_file,'amount_choice':amount_choice}
	return render(request, 'pair/index.html', context)

# -=====new method for the checking of annotations

def checkannotation (request):
	global path_to_csv_file
	all_entries = Entry.objects.all()
	amount_entry = len(all_entries)
	all_choices = Choice.objects.all()
	amount_choice = len (all_choices)

	path_to_csv_file = request.POST['c_name'] # u_name is the name of the input tag
	if path_to_csv_file != None and path_to_csv_file != '':
		print ('load the file at = ', path_to_csv_file)
		load_annotated_entries(path_to_csv_file)

	context = {'all_entries': all_entries, 'amount_entry':amount_entry, 'all_choices':all_choices, 'path':path_to_csv_file,'amount_choice':amount_choice}
	return render(request, 'pair/index.html', context)

def detail(request, entry_id):
	entry = get_object_or_404(Entry, pk=entry_id)
	all_choices = Choice.objects.all()
	# print ('Amount of choices ', len (all_choices))
	return render(request, 'pair/detail.html', {'entry': entry, 'all_choices': all_choices})

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
			return HttpResponseRedirect(reverse('pair:results', args=(entry.id,)))
		else:
			print ('ERROR')
			return render(request, 'pair/detail.html', {
				'entry': entry,
				'error_message': "You didn't select a choice.",
			})
	else:
		entry.user_choice = selected_choice.choice_text
		if entry.user_choice == Choice.left_more_general or entry.user_choice == Choice.neither:
			entry.user_decision = 'remove'
		elif entry.user_choice == Choice.right_more_general or entry.user_choice == Choice.equal:
			entry.user_decision = 'remain'
		elif entry.user_choice == Choice.unknown :
			entry.user_decision = 'unknown'

		# find if there is an entry similar and make decision automatically
		for e in Entry.objects.all():
			if e.left_URI_text ==  entry.right_URI_text  and e.right_URI_text == entry.left_URI_text:
				if entry.user_choice == Choice.left_more_general:
					e.user_choice = Choice.right_more_general
					e.user_decision =  'remain'
				elif entry.user_choice == Choice.right_more_general:
					e.user_choice = Choice.left_more_general
					e.user_decision =  'remove'
				elif entry.user_choice == Choice.equal:
					e.user_choice = Choice.equal
					e.user_decision = 'remain'
				elif entry.user_choice == Choice.neither:
					e.user_choice = Choice.neither
					e.user_decision = 'remove'
				else:
					e.user_decision = 'unknown'
					e.user_choice = Choice.unknown
				e.save()

		print ('chosen: ', selected_choice.choice_text)
		entry.save()
		# selected_choice.votes += 1
		# selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('pair:results', args=(entry.id,)))


def results(request, entry_id):
	entry = get_object_or_404(Entry, pk=entry_id)
	all_choices = Choice.objects.all()
	return render(request, 'pair/results.html', {'entry': entry, 'all_choices':all_choices})
#
# def next_entry (request, entry_id):
#     return HttpResponseRedirect(reverse('pair:detail', args=(entry.id +1,)))
