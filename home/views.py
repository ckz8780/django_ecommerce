from django.shortcuts import render
from django.conf import settings

def index(request):
    """A view to return the index page"""

    return render(request, 'home/index.html')