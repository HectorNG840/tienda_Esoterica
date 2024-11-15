#encoding:utf-8

from django.shortcuts import render


# Pantalla principal
def inicio(request):
    return render(request, 'inicio.html')
