from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from project.tramitacao.forms import FormTipoPendencia
from project.tramitacao.models import Tbtipopendencia, AuthUser, Tbtipoprocesso
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from project.tramitacao.admin import verificar_permissao_grupo
from project.tramitacao.relatorio_base import relatorio_csv_base, relatorio_ods_base,\
    relatorio_ods_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title, relatorio_pdf_base_header
from odslib import ODS

nome_relatorio      = "relatorio_tipo_pendencia"
response_consulta  = "/tramitacao/tipo_pendencia/consulta/"
titulo_relatorio    = "Relatorio dos Tipos das Pendencias"
planilha_relatorio  = "Tipos das Pendencias"


@permission_required('sicop.tipo_pendencia_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        nome = request.POST['dspendencia']
        lista = Tbtipopendencia.objects.all().filter( dspendencia__icontains=nome, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbtipopendencia.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_tipo_pendencia'] = lista
    return render_to_response('sicop/tipo_pendencia/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.tipo_pendencia_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nome')
    if request.method == "POST":
        if validacao(request):
            f_tipopendencia = Tbtipopendencia(
                                        dspendencia = request.POST['dspendencia'],
                                        tbtipoprocesso = Tbtipoprocesso.objects.get( pk = request.POST['tbtipoprocesso'] ),
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_tipopendencia.save()
            return HttpResponseRedirect("/tramitacao/tipo_pendencia/consulta/")
    return render_to_response('sicop/tipo_pendencia/cadastro.html',{'tipoprocesso':tipoprocesso}, context_instance = RequestContext(request))

@permission_required('sicop.tipo_pendencia_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    instance = get_object_or_404(Tbtipopendencia, id=id)
    tipoprocesso = Tbtipoprocesso.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nome')
    if request.method == "POST":

        if not request.user.has_perm('sicop.tipo_pendencia_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/')

           #print request.POST['tbtipoprocesso']
            f_tipopendencia = Tbtipopendencia(
                                        id = instance.id,
                                        dspendencia = request.POST['dspendencia'],
                                        tbtipoprocesso = Tbtipoprocesso.objects.get( pk = request.POST['tbtipoprocesso'] ),
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_tipopendencia.save()
            return HttpResponseRedirect("/tramitacao/tipo_pendencia/edicao/"+str(id)+"/")
    return render_to_response('sicop/tipo_pendencia/edicao.html', {"tipopendencia":instance,'tipoprocesso':tipoprocesso}, context_instance = RequestContext(request))


@permission_required('sicop.tipo_pendencia_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)
        elements=[]

        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('DESCRICAO') )
        for obj in lista:
            dados.append( ( obj.dspendencia ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.tipo_pendencia_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]

    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)

        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Descricao' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')

    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.dspendencia)
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

@permission_required('sicop.tipo_pendencia_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Descricao'])
        for obj in lista:
            writer.writerow([obj.dspendencia])
        return response
    else:
        return HttpResponseRedirect( response_consulta )

def validacao(request_form):
    warning = True
    if request_form.POST['dspendencia'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do tipo pendencia')
        warning = False
    return warning
