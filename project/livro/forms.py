'''
Created on 02/07/2014

@author: eduardo
'''
from django.forms import models
from project.livro.models import Tbstatustitulo, Tbtitulo

class FormStatusTitulo(models.ModelForm):
    class Meta:
        model = Tbstatustitulo

class FormTitulo(models.ModelForm):        
    class Meta:
        model = Tbtitulo





