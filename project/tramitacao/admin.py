# -*- coding: UTF-8 -*-

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib import admin
from project.tramitacao.models import Tbtipocaixa, Tbtipoprocesso, Tbstatuspendencia,\
    Tbpecastecnicas, Tbprocessobase,Tbclassificacaoprocesso, Tbsubarea, Tbcaixa,\
    Tbgleba, Tbcontrato, Tbsituacaoprocesso, Tbtipopendencia, AuthUser,\
    AuthUserGroups, AuthGroupPermissions, Tbmovimentacao, Tbprocessosanexos
from project.geoinformacao.models import TbparcelaGeo
from django.http.response import HttpResponse
import csv
import sys
import sqlite3
from datetime import datetime
from project.tramitacao.models import Tbpendencia,Tbprocessorural, Tbprocessoclausula, Tbprocessourbano
from project.livro.models import Tbtituloprocesso
from django.core import serializers
import urllib2
import json
from odslib import ODS

@permission_required('sicop.processamento', login_url='/excecoes/permissao_negada/', raise_exception=True)
def processamento(request):
    cadastro_automatico_p23(request)
    return render_to_response('core/excecao/pagina_nao_encontrada.html',
                              context_instance = RequestContext(request))   


def cadastro_automatico_p23(request):
    print 'cadastro automatico p23'
    obss = Tbprocessoclausula.objects.filter( dsobs__startswith = '56418' )
    total = []
    other = []
    processos = []
    cad = []

    for obs in obss:
        txt = obs.dsobs.replace('.','').replace('/','').replace('-','').replace(' ','').replace('\\','').replace('\n','').replace('\r','')
        lista = txt.split(',')
        #for l in lista:
        if len(txt) == 17:
            total.append(txt)
            obj = Tbprocessobase.objects.filter( nrprocesso = txt )
            if not obj:
                processos.append(txt)
                    #criar objeto tbprocessobase
                obj_base = Tbprocessobase(
                        nrprocesso = txt,
                        tbgleba = obs.tbprocessobase.tbgleba,
                        tbmunicipio = obs.tbprocessobase.tbmunicipio,
                        tbcaixa = obs.tbprocessobase.tbcaixa,
                        tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessorural' ),
                        dtcadastrosistema = datetime.now(),
                        auth_user = AuthUser.objects.get( pk = request.user.id ),
                        tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 2 ),
                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao,
                        nmendereco = obs.tbprocessobase.nmendereco,
                        nmcontato = obs.tbprocessobase.nmcontato,
                        tbmunicipiodomicilio = obs.tbprocessobase.tbmunicipiodomicilio
                        )
                obj_base.save()

                    #criar objeto tbprocessobase
                obj_rural = Tbprocessorural(
                        nmrequerente = obs.nminteressado,
                        nrcpfrequerente = obs.nrcpfinteressado,
                        nmconjuge = '',
                        nrcpfconjuge = '',
                        tbprocessobase = obj_base,
                        blconjuge = False
                )
                if obs.nminteressado == 'O MESMO':
                    obj_rural.nmrequerente = obs.nmrequerente
                obj_rural.save()

                f_anexos = Tbprocessosanexos(
                        tbprocessobase = obs.tbprocessobase,
                        tbprocessobase_id_anexo = obj_base,
                        auth_user = AuthUser.objects.get( pk = request.user.id ),
                        dtanexado = datetime.now()
                )
                f_anexos.save()

            else:
                cad.append(txt)
        else:
            other.append(txt)

    for o in other:
        print str(o.encode('utf-8'))
    print 'total de registros: '+str(len(obss))
    print 'registros fora da formatacao: '+str(len(other))
    print 'total processos: '+str(len(total))
    print 'aptos a cadastrar: '+str(len(processos))
    print 'ja cadastrados: '+str(len(cad))


def mes_do_ano_texto(inteiro):
    mes_texto = ""
    
    if inteiro == 1: mes_texto = "Janeiro"
    elif inteiro == 2: mes_texto = "Fevereiro"
    elif inteiro == 3: mes_texto = "Marco"
    elif inteiro == 4: mes_texto = "Abril"
    elif inteiro == 5: mes_texto = "Maio"
    elif inteiro == 6: mes_texto = "Junho"
    elif inteiro == 7: mes_texto = "Julho"
    elif inteiro == 8: mes_texto = "Agosto"
    elif inteiro == 9: mes_texto = "Setembro"
    elif inteiro == 10: mes_texto = "Outubro"
    elif inteiro == 11: mes_texto = "Novembro"
    elif inteiro == 12: mes_texto = "Dezembro"
    
    return mes_texto


def verificar_permissao_grupo(usuario, grupos):
    if usuario:
        permissao = False
        obj_usuarios = AuthUserGroups.objects.filter( user = usuario.id )
        for obj in obj_usuarios:
            for obj_g in grupos:
                if obj.user.id == usuario.id and obj.group.name == str(obj_g):
                    permissao = True
        return permissao
    return False

def verificar_permissoes(grupo, permissoes):
    if grupo:
        permissao = False
        obj_grupos = AuthGroupPermissions.objects.filter( group = grupo.id )
        for obj in obj_grupos:
            for obj_g in permissoes:
                if obj.group.id == grupo.id and obj.permission.id == obj_g.id:
                    permissao = True
        return permissao
    return False

def diferenca_mes(d2, d1):
    delta = 1
    print str(d1.month) + '/' + str(d1.year) 
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            print str(d1.month) + '/' + str(d1.year)
            delta += 1
        else:
            break
    return delta

def batimento_cpf_processo(csv_1, csv_2):
    
    with open(csv_1, 'rb') as csvfile:
        parcelas = []
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            parcelas.append(row)

    with open(csv_2, 'rb') as csvfile:
        processos = []
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            processos.append(row)

        
        todos = []
        tem = []
        atrabalhar = []
        for p in parcelas:
            if p in processos:
                tem.append(p)
                todos.append('OK')
            else:
                atrabalhar.append(p)
                todos.append('-')
        print len(tem)
        print len(atrabalhar)
        print len(todos)

        unico = []
        for atr in atrabalhar:
            if atr not in unico:
                unico.append(atr)

    #564180010222015-34

        print len(unico)

    #    with open('/opt/cig_matinha.csv', 'w') as csvfile:
    #        fieldnames = ['trabalhada']
    #        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    #        writer.writeheader()
    #        for cx in todos:
    #            writer.writerow({'trabalhada': str(cx) })


    #        lines = []
    #        x = 0
    #        for l in aux:
    #            if l:
    #                print str(l)
    #                rs = Tbprocessorural.objects.filter( nrcpfrequerente = l[0] )
    #                rs1 = Tbprocessorural.objects.filter( nrcpfconjuge = l[0] )
    #                cs = Tbprocessoclausula.objects.filter( nrcpfrequerente = l[0] )
    #                cs1 = Tbprocessoclausula.objects.filter( nrcpfinteressado = l[0] )
    #                if rs or rs1:
    #                    x += 1
    #            lines.append(l)

    #        print str(x)
    #        print len(lines)

def import_tr(csv_):
    trs = []
    aux = []
    with open(csv_, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            aux.append(row)

    lines = []
    for l in aux:
        #lines.append(l[0])
        sp = l[0].split('|')
        
        #print "ano "+sp[0] + ", mes "+str(1)+", valor "+sp[1]
        if sp[12] == '-':
            obj = TbtrMensal( ano = sp[0], mes = 12, valor = None )
        else:    
            obj = TbtrMensal( ano = sp[0], mes = 12, valor = sp[12].replace(',','.') )
        obj.save()

                #obj = TbtrMensal(
                #        ano = sp[0],
                #        mes = x,
                #        valor = s
                #    )
                #obj.save()
        


    print len(lines)
    print lines

def batimento_txt_n_processo_result_localidade(csv_, filename):
    procs = []
    with open(csv_, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            procs.append(row)

    procs_line = []
    for proc in procs:
        if proc:
            #if not cpf[0] in cpfs_line:
            procs_line.append(proc[0])
        else:
            procs_line.append('0')

    processos = []
    for p in procs_line:
        obj = Tbprocessorural.objects.filter( nrcpfrequerente__icontains = p.replace('/','').replace('.','').replace('-','') )
        if obj:
            #print obj[0].nrprocesso+'|'+obj[0].tbprocessobase.tbcaixa.nmlocalarquivo
            processos.append( obj[0].tbprocessobase.tbcaixa.nmlocalarquivo.encode("utf-8") )
        else:
            processos.append( "-" )

    print len(procs_line)


    with open('/opt/'+filename, 'w') as csvfile:
        fieldnames = ['caixa']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for cx in processos:
            writer.writerow({'caixa': str(cx) })


def batimento_processo(csv_):
    procs = []
    with open(csv_, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            procs.append(row)

    procs_line = []
    for proc in procs:
        if proc:
            #if not cpf[0] in cpfs_line:
            procs_line.append(proc[0])
        else:
            procs_line.append('0')

    processos = []
    for p in procs_line:
        obj = Tbprocessobase.objects.filter( nrprocesso = p.replace('/','').replace('.','').replace('-','') )
        if obj:
            print obj[0].nrprocesso+'|'+obj[0].tbcaixa.nmlocalarquivo
            processos.append( obj[0].tbcaixa.nmlocalarquivo.encode("utf-8") )
        else:
            processos.append( "-" )

    print len(procs_line)


    with open('/opt/matinha.csv', 'w') as csvfile:
        fieldnames = ['caixa']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for cx in processos:
            writer.writerow({'caixa': str(cx) })

def parcela_kml():
    try:
        response = urllib2.urlopen('https://sigef.incra.gov.br/geo/parcela/kml/5db8b1d3-bd31-44eb-90e0-e0847b09115d',timeout=5)
        txt = response.read()
        print txt
    except:
        pass    

def buscar_parcelas_sigef(nrcpf):
    # buscar parcelas do sigef pelo webservice do sigef
    #    idkmls = []
    parcelas = []
    total_area_sigef = 0.0
    try:
        response = urllib2.urlopen('https://sigef.incra.gov.br/api/destinacao/parcelas/?cpf='+nrcpf,timeout=5)
        txt = response.read()
        #jsonparcelas = serializers.serialize('json', html)
        parcelas = txt
 #       x = 0
 #       for parcela in retorno['parcelas']:
 #           x +=1
 #           for mun in parcela['municipios']: 
 #               parc = dict()
 #               parc['parcela'] = 'Parcela '+str(x)
 #               parc['imovel'] = parcela['nome']
 #               parc['area'] = mun['area_parcela']
 #               parc['nome'] = mun['nome'].encode("utf-8")+' / '+mun['uf'].encode("utf-8")
 #               parcelas.append(parc)
 #               total_area_sigef += mun['area_parcela']
            #idkmls.append(parcela['id'])
    except:
        parcelas = None
        print 'error'
    return parcelas    

def sinc_parcelas():
    parcelas = Tbparcela.objects.all()
    total = 0
    ids = []
    for p in parcelas:
        if p.dsjson is not None:
            j = json.loads(p.dsjson)
            total += len(j['parcelas'])
            #print j['parcelas']
            for p in j['parcelas']:
                if p['id'] not in ids:

                    #import para a tabela tbparcela_geo
#                    p_geo = TbparcelaGeo(
#                        id_sigef = p['id'],
#                        nome = p['nome'],
#                        area_total = p['area'],
#                        status = p['status'],
#                        kml = '' 
#                        )
#                    p_geo.save()

                    #import para a tabela tbcpf_parcela_geo                    
#                    for cpf in p['cpfs']:
#                        cpf_geo = TbCPFParcelaGeo(
#                            cpf = cpf,
#                            tbparcela_geo = TbparcelaGeo.objects.filter(id_sigef=p['id'])[0]
#                            )
#                        cpf_geo.save()    
                    
                    #import para a tabela tbcnpj_parcela_geo
#                    for cnpj in p['cnpjs']:
#                        cnpj_geo = TbCNPJParcelaGeo(
#                            cnpj = cnpj,
#                            tbparcela_geo = TbparcelaGeo.objects.filter(id_sigef=p['id'])[0]
#                            )
#                        cnpj_geo.save()    

                    #import para a tabela tbcnpj_parcela_geo
#                    for mun in p['municipios']:
#                        mun_geo = TbMunicipioParcelaGeo(
#                            area = mun['area_parcela'],
#                            area_perc = mun['area_parcela_perc'],
#                            ibge = mun['cod_ibge'],
#                            uf = mun['uf'],
#                            nome = mun['nome'],
#                            tbparcela_geo = TbparcelaGeo.objects.filter(id_sigef=p['id'])[0]
#                            )
#                        mun_geo.save()    
                    
                    ids.append( p['id'] )
    print 'total de parcelas: '+str(len(ids))

def sinc_sigef_parcelas_banco():
    #rural = Tbprocessoclausula.objects.filter( tbprocessobase__tbclassificacaoprocesso__id = 2 )
    rural = Tbparcela.objects.filter( dsjson = None )
    total = 0
    print str(len(rural))
    for r in rural:
        #print r.nrcpfrequerente
        parcela = Tbparcela(
            id = r.id,
            cpf = r.cpf,
            dsjson = buscar_parcelas_sigef( r.cpf )
            )
        parcela.save()
#        if buscar_parcelas_sigef( r.nrcpfrequerente ):
        total += 1
        print 'processamento: '+ str( total )+'/'+ str(len(rural))

def sinc_sigef_parcelas():
    rural = Tbprocessorural.objects.all()
    total = 0
    for r in rural:
        if r.nrcpfconjuge != None and r.nrcpfconjuge != '' and r.nrcpfconjuge != r.nrcpfrequerente:
            parcela = Tbparcela(
                cpf = r.nrcpfconjuge,
                dsjson = buscar_parcelas_sigef( r.nrcpfconjuge )
                )
            parcela.save()
    #        if buscar_parcelas_sigef( r.nrcpfrequerente ):
            total += 1
    print 'processamento: '+ str( total )+'/'+ str(len(rural))

def buscar_processos_sem_pecas_sicop_sigef(request,csv_sigef):
    cpfs = []
    with open(csv_sigef, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            cpfs.append(row)

    cpfs_line = []
    for cpf in cpfs:
        if cpf:
            #if not cpf[0] in cpfs_line:
            cpfs_line.append(cpf[0])
        else:
            cpfs_line.append('0')
#    print len(cpfs_line)
    cont = 0
    procs = []

    rurais = Tbprocessorural.objects.filter( tbprocessobase__tbclassificacaoprocesso__id = 1, tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    p_rural_sem_peca = []
            
    for r in rurais:
        if not Tbpecastecnicas.objects.filter( nrcpfrequerente = r.nrcpfrequerente.replace('.','').replace('-','') ):
            p_rural_sem_peca.append( r )

    print 'Processos sem peca no sicop: '+str(len(p_rural_sem_peca))


    for r in p_rural_sem_peca:
        caixa = ''
        nome = ''
        cpf = ''
        if not r.nrcpfrequerente in cpfs_line and r.nrcpfrequerente != '99999999999' and r.nrcpfrequerente != '00000000000':
            caixa = r.tbprocessobase.tbcaixa.nmlocalarquivo
            nome = r.nmrequerente
            cpf = r.nrcpfrequerente
            print r.nmrequerente + '|' + r.nrcpfrequerente + '|' + r.tbprocessobase.tbcaixa.nmlocalarquivo + '|' + r.tbprocessobase.tbmunicipio.nome_mun + '|' + r.tbprocessobase.tbgleba.nmgleba
            procs.append( str(r.nmrequerente.encode("utf-8") + '|' + r.nrcpfrequerente.encode("utf-8") + '|' + r.tbprocessobase.tbcaixa.nmlocalarquivo.encode("utf-8") +'|'+ r.tbprocessobase.tbmunicipio.nome_mun.encode("utf-8") +'|'+ r.tbprocessobase.tbgleba.nmgleba.encode("utf-8")) )
 
    print 'Processos sem peca no sicop nem no sigef: '+str(len(procs))

    print 'Processos sem peca no sicop mais que ja tem no sigef: '+str(len(p_rural_sem_peca)-len(procs))

    print len(cpfs_line)


    with open('/opt/export-sem-peca-sicop-sigef.csv', 'w') as csvfile:
        fieldnames = ['caixa']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for cx in procs:
            writer.writerow({'caixa': str(cx) })

def buscar_processos_cpfs_abril_sigef(csv_sigef):
    cpfs = []
    with open(csv_sigef, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            cpfs.append(row)

    procs = []
    cpfs_line = []
    for cpf in cpfs:
        if cpf:
            #if not cpf[0] in cpfs_line:
            cpfs_line.append(cpf[0])
        else:
            cpfs_line.append('0')
#    print len(cpfs_line)
    cont = 0
    for c in cpfs_line:
        res = Tbprocessorural.objects.filter( nrcpfrequerente = c, tbprocessobase__tbclassificacaoprocesso__id = 1 )
        caixa = ''
        nome = ''
        if res:
            cont += 1
            obj = res[0]
            caixa = obj.tbprocessobase.tbcaixa.nmlocalarquivo
            nome = obj.nmrequerente
#            print obj.tbprocessobase.nrprocesso + '|' + obj.nmrequerente + '|' + obj.nrcpfrequerente + '|' + obj.tbprocessobase.tbgleba.nmgleba + '|' + obj.tbprocessobase.tbcaixa.nmlocalarquivo
#            procs.append(obj)
        else:
            nome = 'none'
            caixa = '-'
        procs.append( caixa )
        print nome+'|'+caixa

    print len(cpfs_line)
    print len(procs)
    print str(cont)

    with open('/opt/export-sigef-titulacao.csv', 'w') as csvfile:
        fieldnames = ['caixa']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for cx in procs:
            writer.writerow({'caixa': str(cx.encode("utf-8"))})


def buscar_processos_cpfs_sigef(csv_sigef):
    cpfs = []
    with open(csv_sigef, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            cpfs.append(row)


    procs = []
    cpfs_line = []
    for cpf in cpfs:
        if cpf:
            if not cpf[0] in cpfs_line:
                cpfs_line.append(cpf[0])
    print len(cpfs_line)

    for c in cpfs_line:
        res = Tbprocessorural.objects.filter( nrcpfrequerente = c, tbprocessobase__tbclassificacaoprocesso__id = 1 )
        if res:
            obj = res[0]
            print obj.tbprocessobase.nrprocesso + '|' + obj.nmrequerente + '|' + obj.nrcpfrequerente + '|' + obj.tbprocessobase.tbgleba.nmgleba + '|' + obj.tbprocessobase.tbcaixa.nmlocalarquivo
            procs.append(obj)

    print len(cpfs_line)
    print len(procs)


def list_json():
    pecas = ""
    peca = Tbpecastecnicas.objects.filter(nrcpfrequerente = 47551810625)
    for p in peca:
        if p.nrarea:
            pecas += str(p.nrarea)
        else:
            pecas += str('')
            
        pecas += '|'+str(p.tbmunicipio.nome_mun.encode("utf-8"))    
        pecas += '|'+str(p.tbgleba.nmgleba.encode("utf-8"))
        pecas += '|'+str(p.tbcontrato.nrcontrato.encode("utf-8"))
        if p.dsobservacao:
            pecas += '|'+str(p.dsobservacao.encode("utf-8"))
        else:
            pecas += '|'+str('')    
        pecas += 'FIMREG'

    print pecas

def refazer_movimentacao(request):
    # verificar cada processo: se a caixa atual eh o ultimo obj de destino em movimentacao
    procs = Tbprocessobase.objects.filter( tbclassificacaoprocesso__id = 1 )
    qtd = 0
    for p in procs:
        cx = p.tbcaixa.id
        movs = Tbmovimentacao.objects.filter( tbprocessobase__id = p.id ).order_by( "-dtmovimentacao" )
        if movs:
            m = movs[0]
            if m.tbcaixa.id != cx:
                qtd += 1
                print 'Aqui esta diferente: '+p.nrprocesso+' - '+str(p.tbtipoprocesso.id)+' - '+str(p.tbcaixa.id)
#                obj = Tbmovimentacao(
#                    tbprocessobase = p,
#                    tbcaixa_id = p.tbcaixa.id,
#                    tbcaixa_id_origem = m.tbcaixa,
#                    auth_user = AuthUser.objects.get( pk = request.user.id ),
#                    dtmovimentacao = datetime(2015,5,29)
#                    )
#                obj.save()
    print str(qtd)


# tbtipocaixa,
# tbcaixa,
# tbmunicipio, 
# tbtipopendencia,
# tbstatuspendencia, 
# tbsubarea, 
# tbconjuge,
# tbcontrato,
# tbgleba,
# tbsituacaoprocessourbano,
# tbclassificacaoprocesso,
# tbtipoprocesso

# TABELAS BASICAS (VARIAVEIS STATUS E/OU TIPOS)
#admin.site.register(Tbtipoprocesso)
#admin.site.register(Tbtipopendencia)
#admin.site.register(Tbsituacaoprocesso)
#admin.site.register(Tbclassificacaoprocesso)
#admin.site.register(Tbstatuspendencia)
#admin.site.register(Tbpecastecnicas)

# TABELAS CONTROLE CRUD (MIGRACAO)
# admin.site.register(Tbmunicipio)
#admin.site.register(Tbsubarea)
#admin.site.register(Tbcontrato)
#admin.site.register(Tbgleba)
#admin.site.register(Tbcaixa)
#admin.site.register(Tbtipocaixa)
admin.site.register(AuthUser)

