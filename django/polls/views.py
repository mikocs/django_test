from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
import numpy as np

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Question, Choice
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils import timezone

# Create your views here.


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""
		Return the last five published questions (not including those set in the future).
		"""
		return Question.objects.filter(
			pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		"""
		Excludes any questions that aren't published yet.
		"""
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {
		'latest_question_list': latest_question_list,
	}
	#return HttpResponse("Hello World. You are at the Polls index of this Django app.")
	return render(request, 'polls/index.html', context)

def simple_chart(request):
	plot = figure()
	ndarray = np.random.random_sample((2, 100))
	plot.circle(ndarray[0], ndarray[1])

	script, div = components(plot, CDN)

	return render(request, 'polls/simple_chart.html', {"the_script": script, "the_div": div, "what_dis": "OK, it works"})

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {"question": question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request,  'polls/results.html', {"question": question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request,  'polls/detail.html', {
				'question': question, 
				'error_message': "You didn't select a choice.",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()

		return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))