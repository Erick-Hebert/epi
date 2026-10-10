from django.shortcuts import render

def home(req):
    return render(req, 'nucleo/index.html')
