#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User, Group
from ubigeo.models import Ubigeo
import datetime
from django.utils import timezone
from datetime import datetime
from django_facebook.models import FacebookProfile
from django.db.models.signals import post_save
##from django_facebook.models import get_user_model

class Pais(models.Model):
	no_pais = models.CharField(max_length=100, verbose_name='Pais')

	class Meta:
		ordering = ['no_pais',]
		
	def __unicode__(self):
		return self.no_pais

def get_default_pais():
    return Pais.objects.get(pk=1)

class Empresa(models.Model):
	im_logo = models.ImageField(upload_to='empresa', verbose_name="Logo", blank=True)
	nu_ruc = models.CharField(max_length=11, verbose_name='RUC', unique=True)
	no_razon_social = models.CharField(max_length=255, verbose_name='Razón Social', unique=True)
	no_comercial = models.CharField(max_length=255, verbose_name='Nombre Comercial', blank=True)
	de_direccion = models.TextField(verbose_name='Dirección')
	pais = models.ForeignKey(Pais, verbose_name='Nacionalidad', default=get_default_pais)
	ubigeo = models.ForeignKey(Ubigeo)
	nu_fijo = models.CharField(max_length=50, verbose_name='Telefono Fijo')
	nu_movil = models.CharField(max_length=50, verbose_name='Telefono Movil', blank=True)
	no_web = models.URLField(verbose_name='Sitio web', blank=True)
	no_contacto = models.CharField(max_length=255, verbose_name='Contacto')
	nu_telefono_contacto = models.CharField(max_length=50, verbose_name='Telefono Contacto')
	no_email_contacto = models.CharField(max_length=255, verbose_name='Email Contacto', null=True, blank=True)
	fl_notificaciones = models.BooleanField(default=True, blank=True, verbose_name="Recibir notificaciones de Postulantes")
	user = models.OneToOneField(User, unique=True)

	def __unicode__(self):
		return self.no_comercial

	def save(self):
		for field in self._meta.fields:
			if field.name == 'im_logo':
				field.upload_to = 'empresa/%d' % self.user.id
		super(Empresa, self).save()

class Area(models.Model):
	no_area = models.CharField(max_length=50, verbose_name='Área')

	class Meta:
		ordering = ['no_area',]
		
	def __unicode__(self):
		return self.no_area

class TipoEmpleo(models.Model):
	no_tipo_empleo = models.CharField(max_length=50, unique=True, verbose_name='Tipo de empleo')

	def __unicode__(self):
		return self.no_tipo_empleo

class Universidad(models.Model):
	no_universidad = models.CharField(max_length=255, unique=True, verbose_name='Universidad')

	class Meta:
		ordering = ['no_universidad',]

	def __unicode__(self):
		return self.no_universidad

class Carrera(models.Model):
	no_carrera = models.CharField(max_length=255, unique=True, verbose_name='Carrera')

	class Meta:
		ordering = ['no_carrera',]

	def __unicode__(self):
		return self.no_carrera

class EmpleoEstado(models.Model):
	no_estado = models.CharField(max_length=50, unique=True, verbose_name='Estado')

	def __unicode__(self):
		return self.no_estado

def get_empleoestado_pais():
    return EmpleoEstado.objects.get(pk=1)

def get_default_tipoempleo():
    return TipoEmpleo.objects.get(pk=1)

class Empleo(models.Model):
	no_empleo = models.CharField(max_length=255, verbose_name='Titulo del empleo')
	de_empleo = models.TextField(verbose_name='Descripción')
	no_contacto = models.CharField(max_length=100, verbose_name='Contacto')
	no_contacto_telefono = models.CharField(max_length=50, verbose_name='Telefono')
	no_contacto_email = models.CharField(max_length=255, verbose_name='Email')
	de_requisitos = models.TextField(verbose_name='Requisitos', help_text='Separe los requisitos por comas (,)', blank=True)
	de_funciones = models.TextField(verbose_name='Funciones', help_text='Separe las funciones por comas (,)', blank=True)
	va_sueldo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Sueldo', default=0.00, help_text='Dejar en 0.00 para sueldo no especificado')
	fe_creacion = models.DateTimeField(auto_now=True)
	fe_modificacion = models.DateTimeField(auto_now=True)
	area = models.ForeignKey(Area)
	tipoempleo = models.ForeignKey(TipoEmpleo, default=get_default_tipoempleo)
	#contacto = models.ForeignKey(Contacto)
	ubigeo = models.ForeignKey(Ubigeo)
	estado = models.ForeignKey(EmpleoEstado, default=get_empleoestado_pais)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.no_empleo

	def dias_publicado(self):
		td = datetime.now() - datetime(self.fe_creacion.year, self.fe_creacion.month, self.fe_creacion.day)
		dias = td.days
		if(dias < 1):
			return 'publicado hoy'
		elif (dias < 2):
			return 'publicado hace un dia'
		elif (dias < 30):
			return 'publicado hace %s dias' % (dias)
		elif (dias < 31):
			return 'publicado hace %s mes' % (dias)
		else:
			if(dias%30 == 0):
				return 'publicado hace %s meses' % (dias / 30)
			else:
				return 'publicado hace mas de %s meses' % (dias / 30)

class EstadoCivil(models.Model):
	no_estado_civil = models.CharField(max_length=255, verbose_name='Estado Civil')

	def __unicode__(self):
		return self.no_estado_civil

class Sexo(models.Model):
	fl_Sexo = models.CharField(max_length=255, verbose_name='Sexo')

	def __unicode__(self):
		return self.fl_Sexo

class TipoLicencia(models.Model):
	no_tipo_licencia = models.CharField(max_length=255, verbose_name='Tipo de Licencia')

	def __unicode__(self):
		return self.no_tipo_licencia

class Postulante(models.Model):
	im_foto = models.ImageField(upload_to='postulante', verbose_name="Foto", blank=True)
	no_postulante = models.CharField(max_length=255, verbose_name="Nombre")
	ap_postulante = models.CharField(max_length=255, verbose_name="Apellido Paterno")
	am_postulante = models.CharField(max_length=255, verbose_name="Apellido Materno")
	fe_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
	sexo = models.ForeignKey(Sexo)
	de_direccion = models.TextField(verbose_name='Dirección', blank=True)
	pais = models.ForeignKey(Pais, verbose_name='Nacionalidad', default=get_default_pais)
	ubigeo = models.ForeignKey(Ubigeo)
	nu_fijo = models.CharField(max_length=50, verbose_name='Telefono Fijo')
	nu_movil = models.CharField(max_length=50, verbose_name='Telefono Movil', blank=True)
	estadocivil = models.ForeignKey(EstadoCivil, verbose_name='Estado Civil')
	fl_licencia = models.BooleanField(default=False, blank=True, verbose_name="Licencia de Conducir")
	tipolicencia = models.ForeignKey(TipoLicencia, blank=True, null=True)
	fl_auto_propio = models.BooleanField(default=False, blank=True, verbose_name="Vehiculo Propio")
	de_sobremi = models.TextField(verbose_name='Sobre mi', blank=True)
	fl_notificaciones = models.BooleanField(default=True, blank=True, verbose_name="Recibir notificaciones de empleos")
	user = models.OneToOneField(User, unique=True)

	def __unicode__(self):
		return self.no_postulante

	def save(self):
		for field in self._meta.fields:
			if field.name == 'im_foto':
				field.upload_to = 'postulante/%d' % self.user.id
		super(Postulante, self).save()
		
	def get_nombre_completo(self):
		return self.no_postulante + ' ' + self.ap_postulante + ' ' + self.am_postulante

	def get_anios(self):
		td = datetime.now() - datetime(self.fe_nacimiento.year, self.fe_nacimiento.month, self.fe_nacimiento.day)
		dias = td.days
		return dias / 365

class PostulanteEmpresaEmpleo(models.Model):
	empleo = models.ForeignKey(Empleo)
	user = models.ForeignKey(User)
	fe_creacion = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.empleo.no_empleo

class PostulanteEstudio(models.Model):
	institucion = models.ForeignKey(Universidad, verbose_name="Universidad/Instituto")
	carrera = models.ForeignKey(Carrera, verbose_name="Carrera")
	fe_periodo_ini = models.CharField(max_length=7, verbose_name="Inicio")
	fe_periodo_fin = models.CharField(max_length=7, verbose_name="Fin", blank=True)
	fl_actualidad = models.BooleanField(default=False, blank=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.institucion.no_universidad

class PostulanteEmpleo(models.Model):
	no_empresa = models.CharField(max_length=255, verbose_name="Empresa")
	no_cargo = models.CharField(max_length=255, verbose_name="Cargo")
	de_funciones = models.TextField(verbose_name='Funciones', blank=True)
	de_logros = models.TextField(verbose_name='Logros', blank=True)
	no_referencia = models.CharField(max_length=255, verbose_name="Persona Referencia")
	no_referencia_cargo = models.CharField(max_length=255, verbose_name="Cargo")
	nu_referencia_telefono = models.CharField(max_length=255, verbose_name="Teléfono")
	fe_periodo_ini = models.CharField(max_length=7, verbose_name="Inicio Labores")
	fe_periodo_fin = models.CharField(max_length=7, verbose_name="Fin Labores", blank=True)
	fl_actualidad = models.BooleanField(default=False, blank=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.no_empresa

class MensajeDirecto(models.Model):
	fe_creacion = models.DateTimeField(auto_now=True)
	de_asunto = models.CharField(max_length=255, verbose_name='Asunto')
	de_mensaje = models.TextField(verbose_name='Mensaje')
	de_adjunto = models.FileField(upload_to='mensaje', verbose_name="Adjunto", blank=True)
	fl_revisado = models.BooleanField(default=False, blank=True)
	fe_revisado = models.DateTimeField(blank=True, null=True)
	remitente = models.ForeignKey(User, related_name='remitente')
	destinatario = models.ForeignKey(User, related_name='destinatario')
	postulanteempresaempleo = models.ForeignKey(PostulanteEmpresaEmpleo)

	class Meta:
		ordering = ['-fe_creacion',]

	def __unicode__(self):
		return self.de_asunto

class Idioma(models.Model):
	no_idioma = models.CharField(max_length=255, verbose_name='Idioma')

	class Meta:
		ordering = ['no_idioma',]
		
	def __unicode__(self):
		return self.no_idioma

class Nivel(models.Model):
	no_nivel = models.CharField(max_length=255, verbose_name='Nivel')

	def __unicode__(self):
		return self.no_nivel

class PostulanteIdiomaNivel(models.Model):
	user = models.ForeignKey(User)
	idioma = models.ForeignKey(Idioma)
	nivel = models.ForeignKey(Nivel)

	def __unicode__(self):
		return '%s - %s' % (self.idioma, self.nivel)

class RecuperarPassword(models.Model):
	usuario = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	token = models.CharField(max_length=255, unique=True)
	fe_expira = models.DateTimeField(auto_now=True)
	fl_usado = models.BooleanField(default=False, blank=True)

class Programa(models.Model):
	no_programa = models.CharField(max_length=255, verbose_name='Programa')

	class Meta:
		ordering = ['no_programa',]
		
	def __unicode__(self):
		return self.no_programa

class PostulanteProgramaNivel(models.Model):
	user = models.ForeignKey(User)
	programa = models.ForeignKey(Programa)
	nivel = models.ForeignKey(Nivel)

	def __unicode__(self):
		return '%s - %s' % (self.programa, self.nivel)

#class MyFbCustomProfile(FacebookProfileModel):
#    user = models.OneToOneField('auth.User')

    #def save(self):
	#	self.user.groups.add(Group.objects.get(pk=1)) #Postulante
	#	super(MyFbCustomProfile, self).save()

#def create_facebook_profile(sender, instance, created,	 **kwargs):
#	if created:
#		instance.groups.add(Group.objects.get(pk=1)) #Postulante
		#MyFbCustomProfile.objects.create(user=instance)

def add_group(sender, instance, created, **kwargs):
	if created:
		g = instance.groups.all().count()
		#fb = FacebookProfile.objects.filter(user=instance)
		if g == 0:
			instance.groups.add(Group.objects.get(pk=1))
			instance.save()

post_save.connect(add_group, sender=User)