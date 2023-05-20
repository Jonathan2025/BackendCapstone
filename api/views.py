from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

# 2 we will create a simple getRoutes here 
def getRoutes(request): 
    return JsonResponse('Our Api', safe=False) #safe just allows us to get back more data than just a dictionary