from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormSituacaoProcesso
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from sicop.models import Tbsituacaoprocesso
from sicop.relatorio_base import relatorio_base_consulta

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmsituacao']
        lista = Tbsituacaoprocesso.objects.all().filter( nmsituacao__contains=nome )
    else:
        lista = Tbsituacaoprocesso.objects.all()
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_situacao_processo'] = lista
    return render_to_response('sicop/restrito/situacao_processo/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    if request.method == "POST":
        next = request.GET.get('next', '/')
        form = FormSituacaoProcesso(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                if next == "/":
                    return HttpResponseRedirect("/sicop/restrito/situacao_processo/consulta/")
                else:    
                    return HttpResponseRedirect( next ) 
    else:
        form = FormSituacaoProcesso()
    return render_to_response('sicop/restrito/situacao_processo/cadastro.html',{"form":form}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    instance = get_object_or_404(Tbsituacaoprocesso, id=id)
    if request.method == "POST":
        form = FormSituacaoProcesso(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/situacao_processo/consulta/")
    else:
        form = FormSituacaoProcesso(instance=instance) 
    return render_to_response('sicop/restrito/situacao_processo/edicao.html', {"form":form}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_situacao_processo']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DAS SITUACOES DOS PROCESSOS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/situacao_processo/consulta/")

def validacao(request_form):
    warning = True
    if request_form.POST['nmsituacao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome da situacao processo')
        warning = False
    return warning
