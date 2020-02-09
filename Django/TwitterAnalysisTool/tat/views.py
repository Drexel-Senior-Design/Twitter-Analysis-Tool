from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import *

from tat.models import GaussianNB, LSTMTextClassifier

# Create your views here.
def index(request):
    template = loader.get_template('tat/index.html')
    user_hashtag = ''
    context = {
        'usser_hashtag' : user_hashtag,

    }
    #return HttpResponse(template.render(context, request))
    return render(request, 'tat/index.html', context)

def about(request):
    template = loader.get_template('tat/about.html')
    context = {

    }
    return render(request, 'tat/about.html', context)

def search(request):
    if request.method == 'POST':
        user_hashtag = request.POST.get('user_hashtag', None)
        user_model = request.POST.get('user_model', None)
        #print(user_model)
        if user_model == 'nb':
            html = GaussianNB('Hashtags', user_hashtag)
        else:
            html = LSTMTextClassifier('Hashtags', user_hashtag)
        print(user_hashtag)
        return HttpResponse(html)
        #return render(request, 'tat/search.html', user_hashtag)

