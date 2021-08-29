from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'home.html')

def pitstop_analysis(request):
    return render(request,'pitstop_analysis.html')