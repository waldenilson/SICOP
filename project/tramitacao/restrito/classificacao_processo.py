from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from project.tramitacao.forms import FormClassificacaoProcesso
from project.tramitacao.models import Tbclassificacaoprocesso, AuthUser
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from project.tramitacao.admin import verificar_permissao_grupo
from project.tramitacao.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS

nome_relatorio      = "relatorio_classificacao_processo"
response_consulta  = "/tramitacao/classificacao_processo/consulta/"
titulo_relatorio    = "Relatorio das Classificacoes de Processos"
planilha_relatorio  = "Classificacoes de Processos"

@permission_required('sicop.classificacao_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmclassificacao']
        lista = Tbclassificacaoprocesso.objects.all().filter( nmclassificacao__icontains=nome, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbclassificacaoprocesso.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_classificacao_processo'] = lista
    return render_to_response('sicop/classificacao_processo/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.classificacao_processo_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    if request.method == "POST":
        if validacao(request):
            f_classificacao = Tbclassificacaoprocesso(
                                                        nmclassificacao = request.POST['nmclassificacao'],
                                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                                      )
            f_classificacao.save()
            return HttpResponseRedirect("/tramitacao/classificacao_processo/consulta/") 
    return render_to_response('sicop/classificacao_processo/cadastro.html', context_instance = RequestContext(request))

@permission_required('sicop.classificacao_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    instance = get_object_or_404(Tbclassificacaoprocesso, id=id)
    if request.method == "POST":

        if not request.user.has_perm('sicop.classificacao_processo_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 

        if validacao(request):
            f_classificacao = Tbclassificacaoprocesso(
                                                        id = instance.id,
                                                        nmclassificacao = request.POST['nmclassificacao'],
                                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                                      )
            f_classificacao.save()
            return HttpResponseRedirect("/tramitacao/classificacao_processo/edicao/"+str(id)+"/")
    return render_to_response('sicop/classificacao_processo/edicao.html', {"classificacao":instance}, context_instance = RequestContext(request))


@permission_required('sicop.classificacao_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NOME','') )
        for obj in lista:
            dados.append( ( obj.nmclassificacao , '' ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.classificacao_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.nmclassificacao)
            x += 1
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA     
       
        relatorio_ods_base(ods, planilha_relatorio)
        # generating response
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
    
        return response
    else:
        return HttpResponseRedirect( response_consulta )

@permission_required('sicop.classificacao_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome'])
        for obj in lista:
            writer.writerow([obj.nmclassificacao])
        return response
    else:
        return HttpResponseRedirect( response_consulta )



def validacao(request_form):
    warning = True
    if request_form.POST['nmclassificacao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do classificacao processo')
        warning = False
    return warning
