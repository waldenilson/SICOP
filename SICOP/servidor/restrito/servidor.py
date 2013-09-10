from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages
from sicop.forms import FormPecasTecnicas
from sicop.forms import FormServidor

from sicop.models import Tbpecastecnicas, Tbgleba, Tbcaixa, Tbcontrato, Tbservidor

#SERVIDORES -----------------------------------------------------------------------------------------------------------------------------

@login_required
def consulta(request):
    if request.method == "POST":
        #requerente = request.POST['requerente']
        #cpf = request.POST['cpf']
        #entrega = request.POST['entrega']
        servidor = request.POST['servidor']
        #lista = Tbpecastecnicas.objects.all().filter( nmrequerente__contains=requerente, nrcpfrequerente__contains=cpf, nrentrega__contains=entrega )
        lista = Tbservidor.objects.all().filter( nmservidor__contains=servidor)
    
    else:
        lista = Tbservidor.objects.all()
    lista = lista.order_by( 'id' )
    #return render_to_response('sicop/restrito/peca_tecnica/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))
    return render_to_response('controle/servidor/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    #usar quando tives chaves 
    #contrato = Tbcontrato.objects.all()
    #caixa = Tbcaixa.objects.filter( tbtipocaixa = 2 )
    #gleba = Tbgleba.objects.all()
    if request.method == "POST":
        form = FormServidor(request.POST)
        if validacao(request):
            if form.is_valid():
                print 'passou save'
                form.save()
                return HttpResponseRedirect("/controle/restrito/servidor/consulta/") 
    else:
        form = FormServidor() #gera registro novo
    
    #return render_to_response('sicop/restrito/peca_tecnica/cadastro.html',{"form":form,'caixa':caixa,'contrato':contrato,'gleba':gleba}, context_instance = RequestContext(request))
    return render_to_response('controle/servidor/cadastro.html',{"form":form}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    #usar abaixo se tiver FK tem que recuperar todas antes de exibir
    ##contrato = Tbcontrato.objects.all()
    ##caixa = Tbcaixa.objects.filter( tbtipocaixa = 2 )
    #gleba = Tbgleba.objects.all()
    
    instance = get_object_or_404(Tbservidor, id=id)
        
    if request.method == "POST":
        form = FormServidor(request.POST,request.FILES,instance=instance)
        
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/servidor/restrito/servidor/consulta/")
    else:
        form = FormServidor(instance=instance) 

    return render_to_response('controle/servidor/edicao.html',
                              {"form":form}, 
                              context_instance = RequestContext(request))

def validacao(request_form):
    print 'passou validacao'
    warning = True
    if request_form.POST['nmservidor'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe nome do servidor')
        warning = False
    return warning
