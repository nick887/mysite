from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .forms import TopicForm
# Create your views here.


def index(request):
    return render(request,'learning_logs/index.html')




