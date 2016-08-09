from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Question,Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    print latest_question_list
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list}
    return HttpResponse(template.render(context, request))
def details(request, question_id):
    question = Question.objects.get(pk=question_id)
    choice_set = question.choice_set.all()
    template = loader.get_template('polls/details.html')
    context = {'question': question}
    return HttpResponse(template.render(context, request))
