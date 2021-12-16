from django import template
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import Question, Choice
# Create your views here.
class IndexView(ListView):
    template_name = 'polls\index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        """ Returns the last 5 published questions """
        return Question.objects.filter(pub_date__lte = timezone.now())[:5]

class DetailView(DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(DetailView):
    model = Question
    template_name = 'polls/result.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(request.POST)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        #redisplay the question voting form
        context = {'question': question, 'error_message': "You didn't select a choice"}
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #always return an HttpResponseRedirect after successfully dealing with a POST data
        #This prevent data from being posted twice if a user hits the back button
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))