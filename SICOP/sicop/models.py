# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)
    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    tbdivisao = models.ForeignKey('Tbdivisao')
    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = 'auth_user_user_permissions'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    class Meta:
        db_table = 'django_site'

class Tbcaixa(models.Model):
    nmlocalarquivo = models.CharField(max_length=80, blank=True)
    qtdprocessos = models.IntegerField(null=True, blank=True)
    tbtipocaixa = models.ForeignKey('Tbtipocaixa')
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbcaixa'

class Tbclassificacaoprocesso(models.Model):
    nmclassificacao = models.CharField(max_length=80, blank=True)
    id = models.AutoField(primary_key=True)
    tbdivisao = models.ForeignKey('Tbdivisao', null=True, blank=True)
    class Meta:
        db_table = 'tbclassificacaoprocesso'

class Tbcontrato(models.Model):
    nrcontrato = models.CharField(max_length=10, blank=True)
    nmempresa = models.CharField(max_length=100, blank=True)
    id = models.AutoField(primary_key=True)
    tbdivisao = models.ForeignKey('Tbdivisao', null=True, blank=True)
    class Meta:
        db_table = 'tbcontrato'

class Tbdivisao(models.Model):
    id = models.AutoField(primary_key=True)
    nmdivisao = models.CharField(max_length=80, blank=True)
    dsdivisao = models.TextField(blank=True)
    tbuf = models.ForeignKey('Tbuf', null=True, blank=True)
    class Meta:
        db_table = 'tbdivisao'

class Tbgleba(models.Model):
    cdgleba = models.IntegerField(null=True, blank=True)
    nmgleba = models.CharField(max_length=80, blank=True)
    tbsubarea = models.ForeignKey('Tbsubarea')
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbgleba'

class Tbmovimentacao(models.Model):
    tbprocessobase = models.ForeignKey('Tbprocessobase')
    dtmovimentacao = models.DateTimeField(null=True, blank=True)
    tbcaixa_id_origem = models.ForeignKey(Tbcaixa, db_column='tbcaixa_id_origem', related_name='tbcaixa_id_origem')
    tbcaixa = models.ForeignKey(Tbcaixa)
    auth_user = models.ForeignKey(AuthUser)
    nrdias = models.IntegerField(null=True, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbmovimentacao'

class Tbmunicipio(models.Model):
    nome_mun_maiusculo = models.CharField(max_length=50, db_column='Nome_Mun_Maiusculo', blank=True) # Field name made lowercase.
    nome_mun = models.CharField(max_length=50, db_column='Nome_Mun', blank=True) # Field name made lowercase.
    codigo_mun = models.IntegerField(null=True, db_column='Codigo_Mun', blank=True) # Field name made lowercase.
    regiao = models.CharField(max_length=50, db_column='Regiao', blank=True) # Field name made lowercase.
    nome_estado = models.CharField(max_length=50, db_column='Nome_Estado', blank=True) # Field name made lowercase.
    uf = models.CharField(max_length=2, db_column='UF', blank=True) # Field name made lowercase.
    sr = models.CharField(max_length=50, db_column='SR', blank=True) # Field name made lowercase.
    codigo_uf = models.ForeignKey('Tbuf', null=True, db_column='Codigo_UF', blank=True) # Field name made lowercase.
    populacao = models.CharField(max_length=50, db_column='Populacao', blank=True) # Field name made lowercase.
    id = models.IntegerField(primary_key=True)
    nrmodulofiscal = models.IntegerField(null=True, blank=True)
    nrfracaominima = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'tbmunicipio'

class Tbpecastecnicas(models.Model):
    cdpeca = models.CharField(max_length=50, blank=True)
    tbcontrato = models.ForeignKey(Tbcontrato)
    nrentrega = models.CharField(max_length=10, blank=True)
    nrcpfrequerente = models.CharField(max_length=14, blank=True)
    nmrequerente = models.CharField(max_length=80, blank=True)
    stenviadobrasilia = models.BooleanField()
    stpecatecnica = models.BooleanField()
    stanexadoprocesso = models.BooleanField()
    dsobservacao = models.TextField(blank=True)
    tbcaixa = models.ForeignKey(Tbcaixa)
    nrarea = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    nrperimetro = models.DecimalField(null=True, max_digits=18, decimal_places=4, blank=True)
    tbgleba = models.ForeignKey(Tbgleba)
    id = models.AutoField(primary_key=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    class Meta:
        db_table = 'tbpecastecnicas'

class Tbpendencia(models.Model):
    nrcodigo = models.CharField(max_length=50, blank=True)
    tbprocessobase = models.ForeignKey('Tbprocessobase')
    tbtipopendencia = models.ForeignKey('Tbtipopendencia')
    dsdescricao = models.TextField(blank=True)
    dtpendencia = models.DateTimeField(null=True, blank=True)
    auth_user = models.ForeignKey(AuthUser)
    tbstatuspendencia = models.ForeignKey('Tbstatuspendencia')
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbpendencia'

class Tbprocessobase(models.Model):
    nrprocesso = models.CharField(max_length=17, blank=True)
    tbgleba = models.ForeignKey(Tbgleba)
    tbcaixa = models.ForeignKey(Tbcaixa)
    tbmunicipio = models.ForeignKey(Tbmunicipio)
    auth_user = models.ForeignKey(AuthUser)
    tbtipoprocesso = models.ForeignKey('Tbtipoprocesso')
    id = models.AutoField(primary_key=True)
    tbsituacaoprocesso = models.ForeignKey('Tbsituacaoprocesso', null=True, blank=True)
    dtcadastrosistema = models.DateTimeField(null=True, blank=True)
    tbclassificacaoprocesso = models.ForeignKey(Tbclassificacaoprocesso, null=True, blank=True)
    tbdivisao = models.ForeignKey('Tbdivisao')
    class Meta:
        db_table = 'tbprocessobase'

class Tbprocessoclausula(models.Model):
    tbprocessobase = models.ForeignKey(Tbprocessobase)
    nmrequerente = models.CharField(max_length=100, blank=True)
    nminteressado = models.CharField(max_length=100, blank=True)
    nrcpfrequerente = models.CharField(max_length=11, blank=True)
    nrcpfinteressado = models.CharField(max_length=11, blank=True)
    nrarea = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    cdstatus = models.IntegerField(null=True, blank=True)
    dsobs = models.TextField(blank=True)
    stprocuracao = models.BooleanField( blank=True)
    id = models.AutoField(primary_key=True)
    dttitulacao = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'tbprocessoclausula'

class Tbprocessorural(models.Model):
    tbprocessobase = models.ForeignKey(Tbprocessobase)
    nmrequerente = models.CharField(max_length=100, blank=True)
    nrcpfrequerente = models.CharField(max_length=11, blank=True)
    blconjuge = models.BooleanField( blank=True)
    cdstatus = models.IntegerField(null=True, blank=True)
    id = models.AutoField(primary_key=True)
    nrcpfconjuge = models.CharField(max_length=11, blank=True)
    nmconjuge = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = 'tbprocessorural'

class Tbprocessosanexos(models.Model):
    tbprocessobase = models.ForeignKey(Tbprocessobase)
    tbprocessobase_id_anexo = models.ForeignKey(Tbprocessobase, db_column='tbprocessobase_id_anexo', related_name='tbprocessobase_id_anexo')
    dtanexado = models.DateTimeField(null=True, blank=True)
    auth_user = models.ForeignKey(AuthUser)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbprocessosanexos'

class Tbprocessourbano(models.Model):
    tbprocessobase = models.ForeignKey(Tbprocessobase)
    nmpovoado = models.CharField(max_length=80, blank=True)
    nrcnpj = models.CharField(max_length=14, blank=True)
    dtaberturaprocesso = models.DateTimeField(null=True, blank=True)
    dttitulacao = models.DateTimeField(null=True, blank=True)
    nrarea = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    nrperimetro = models.DecimalField(null=True, max_digits=18, decimal_places=4, blank=True)
    nrdomicilios = models.IntegerField(null=True, blank=True)
    nrhabitantes = models.IntegerField(null=True, blank=True)
    nrpregao = models.CharField(max_length=30, blank=True)
    tbcontrato = models.ForeignKey(Tbcontrato)
    id = models.AutoField(primary_key=True)
    tbsituacaogeo = models.ForeignKey('Tbsituacaogeo', null=True, blank=True)
    class Meta:
        db_table = 'tbprocessourbano'

class Tbservidor(models.Model):
    id = models.AutoField(primary_key=True)
    iduser = models.ForeignKey(AuthUser, db_column='idUser_id') # Field name made lowercase.
    nmservidor = models.CharField(max_length=100)
    nmunidade = models.CharField(max_length=100)
    nmlotacao = models.CharField(max_length=30)
    cdsiape = models.CharField(max_length=7) # Field name made lowercase.
    nrcpf = models.CharField(max_length=11) # Field name made lowercase.
    dsportariacargo = models.CharField(max_length=80)
    dsportaria = models.CharField(max_length=80)
    nmcargo = models.CharField(max_length=40)
    nrtelefone1 = models.CharField(max_length=10)
    nrtelefone2 = models.CharField(max_length=10)
    email = models.CharField(max_length=75)
    dsatividades = models.CharField(max_length=80)
    class Meta:
        db_table = 'tbservidor'

class Tbsituacaogeo(models.Model):
    id = models.AutoField(primary_key=True)
    nmsituacaogeo = models.CharField(max_length=80, blank=True)
    dssituacaogeo = models.TextField(blank=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    class Meta:
        db_table = 'tbsituacaogeo'

class Tbsituacaoprocesso(models.Model):
    nmsituacao = models.CharField(max_length=80, blank=True)
    id = models.AutoField(primary_key=True)
    dssituacao = models.TextField(blank=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    class Meta:
        db_table = 'tbsituacaoprocesso'

class Tbstatuspendencia(models.Model):
    stpendencia = models.IntegerField(null=True, blank=True)
    dspendencia = models.CharField(max_length=100, blank=True)
    id = models.AutoField(primary_key=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    class Meta:
        db_table = 'tbstatuspendencia'

class Tbsubarea(models.Model):
    cdsubarea = models.CharField(max_length=10, blank=True)
    nmsubarea = models.CharField(max_length=80, blank=True)
    id = models.AutoField(primary_key=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    class Meta:
        db_table = 'tbsubarea'

class Tbtipocaixa(models.Model):
    nmtipocaixa = models.CharField(max_length=80, blank=True)
    desctipocaixa = models.TextField(blank=True)
    id = models.AutoField(primary_key=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    class Meta:
        db_table = 'tbtipocaixa'

class Tbtipopendencia(models.Model):
    cdtipopend = models.IntegerField(null=True, blank=True)
    dspendencia = models.CharField(max_length=50, blank=True)
    cdgrupo = models.CharField(max_length=20, blank=True)
    id = models.AutoField(primary_key=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    class Meta:
        db_table = 'tbtipopendencia'

class Tbtipoprocesso(models.Model):
    nome = models.CharField(max_length=80, blank=True)
    tabela = models.CharField(max_length=50, blank=True)
    id = models.AutoField(primary_key=True)
    coridentificacao = models.CharField(max_length=20, blank=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    class Meta:
        db_table = 'tbtipoprocesso'

class Tbuf(models.Model):
    id = models.IntegerField(primary_key=True)
    sigla = models.CharField(max_length=2, blank=True)
    nmuf = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = 'tbuf'
