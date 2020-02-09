from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import *

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
        html = ("<H1>%s</H!>", user_hashtag)
        return HttpResponse(html)
        #return render(request, 'tat/search.html', user_hashtag)

