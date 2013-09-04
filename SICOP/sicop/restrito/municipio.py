#PROCESSOS -----------------------------------------------------------------------------------------------------------------------------
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from sicop.forms import FormProcessoBase

@login_required
def consulta(request):
    return render_to_response('sicop/restrito/municipio/consulta.html',{}, 
                              context_instance = RequestContext(request))    
    
@login_required
def cadastro(request):
    form = FormProcessoBase()
    return render_to_response('sicop/restrito/municipio/cadastro.html',{"form":form}, context_instance = RequestContext(request))

@login_required
def edicao(request):
    return render_to_response('sicop/restrito/municipio/edicao.html',{})