from django.shortcuts import render

# Create your views here.
def home(request):
    """首页"""
    
    return render(request, 'index.html')