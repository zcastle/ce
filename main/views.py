#encoding:utf-8
# Create your views here.
from __future__ import unicode_literals
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from main.models import Area, Empleo, Empresa, Postulante, PostulanteEstudio, PostulanteEmpleo, PostulanteEmpresaEmpleo, MensajeDirecto, TipoEmpleo, PostulanteIdiomaNivel, Universidad, RecuperarPassword, PostulanteProgramaNivel, Carrera, Idioma, Programa
from main.forms import PostulanteCreationCompleteForm, PostulanteChangeForm, PostulanteEstudioForm, PostulanteEmpleoForm, EmpresaCreationCompleteForm, EmpresaEmpleoForm, MensajeDirectoForm, PostulanteIdiomaNivelForm, PostulanteChangePasswordForm, RecuperarPasswordForm, PostulanteRecuperarPasswordForm, PostulanteProgramaNivelForm, EmpresaChangeForm, EmpresaNotificacionesForm, PostulanteNotificacionesForm, ValidarPasswordForm, BusquedaAvanzadaForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
#from emailusernames.utils import create_user
from emailusernames.forms import EmailAuthenticationForm, EmailUserCreationForm
#, EmailUserChangeForm
from django.utils import simplejson as json
#from django.forms.models import model_to_dict
from django.utils import formats
from datetime import datetime
import smtplib
from emailusernames.utils import _email_to_username
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ubigeo.models import Ubigeo

def getEp(request, empleo_id):
	empresaempleos = PostulanteEmpresaEmpleo.objects.filter(empleo_id=empleo_id).order_by('fe_creacion') #.reverse()
	ee = []
	for empresaempleo in empresaempleos:
		if empresaempleo.empleo.user == request.user:
			item = {'id': empresaempleo.pk, 'fe_creacion': empresaempleo.fe_creacion, 'id_postulante': empresaempleo.user.pk, 'postulante': empresaempleo.user.postulante}
			ee.append(item)
	return ee

def home(request):
	#empleos = Empleo.objects.all().order_by('fe_creacion').reverse()[:10]
	if request.user.groups.filter(pk=1).count() > 0:
		distrito = request.user.postulante.ubigeo
		departamento = Ubigeo.objects.get(pk=distrito.parent_id)
		empleos_list = Empleo.objects.filter(ubigeo=distrito).order_by('-fe_creacion')
	else:
		empleos_list = Empleo.objects.all().order_by('-fe_creacion')

	paginator = Paginator(empleos_list, 10)
	page = request.GET.get('page')
	try:
		empleos = paginator.page(page)
	except PageNotAnInteger:
		empleos = paginator.page(1)
	except EmptyPage:
		empleos = paginator.page(paginator.num_pages)

	return render_to_response('home.html', locals(), context_instance=RequestContext(request))

def buscar(request):
	text_buscar = request.GET.get('text_buscar', '')
	text_buscar_list = text_buscar.split(' ')
	#fields = ['no_empleo', 'de_empleo', 'area__no_area', 'empresa__no_comercial']
	if text_buscar:
		qset = Q()
		for term in text_buscar_list:
			qset.add((Q(no_empleo__icontains=term) | Q(de_empleo__icontains=term) | Q(area__no_area__icontains=term) | Q(user__empresa__no_comercial__icontains=term) | Q(user__empresa__no_razon_social__icontains=term) | Q(ubigeo__name__icontains=term)), qset.connector)
		empleos = Empleo.objects.filter(qset).distinct()
	else:
		return HttpResponseRedirect('/')
	return render_to_response('buscar.html', locals(), context_instance=RequestContext(request))

def listar_areas(request):
	return render_to_response('list-areas.html', locals(), context_instance=RequestContext(request))

def listar_empresas(request):
	return render_to_response('list-empresas.html', locals(), context_instance=RequestContext(request))

def listar_por_areas(request, id_area):
	result = get_object_or_404(Area, pk=id_area)
	empleos = Empleo.objects.filter(area=result)
	return render_to_response('list.html', locals(), context_instance=RequestContext(request))

def listar_por_empresas(request, id_empresa):
	result = get_object_or_404(User, pk=id_empresa)
	empleos = Empleo.objects.filter(user=result)
	result = result.empresa
	return render_to_response('list.html', locals(), context_instance=RequestContext(request))

def listar_por_tipo_empleo(request, id_tipo_empleo):
	result = get_object_or_404(TipoEmpleo, pk=id_tipo_empleo)
	empleos = Empleo.objects.filter(tipoempleo=result)
	return render_to_response('list.html', locals(), context_instance=RequestContext(request))

def empresa_crear(request):
	if request.method == 'POST':
		formulario = EmailUserCreationForm(request.POST)
		if formulario.is_valid():
			user = formulario.save()
			user.groups.add(Group.objects.get(pk=2)) #Empresa
			user.is_active = False
			user.save()
			acceso = authenticate(email=request.POST['email'], password=request.POST['password1'])
			login(request, acceso)
			return HttpResponseRedirect('/empresa/completar')
	else:
		formulario = EmailUserCreationForm()
	return render_to_response('empresa-crear.html', locals(), context_instance=RequestContext(request))

#@user_passes_test(lambda u: u.groups.filter(pk=1).count() == 0, login_url='/')
@login_required(login_url='/empresa/ingresar')
def empresa_completar(request):
	if request.method == 'POST':
		formulario = EmpresaCreationCompleteForm(request.POST, request.FILES)
		if formulario.is_valid():
			obj = formulario.save(commit=False)
			obj.user = request.user
			obj.save()
			headers = ["from: Coopsol Empleos <no-responder@coopsolempleos.com>",
			"subject: Bienvenido a Coopsol Empleos",
			"to: " + obj.user.email,
			"mime-version: 1.0",
			"content-type: text/html"]
			headers = "\r\n".join(headers)

			body = """<img src='http://www.coopsolempleos.com/static/images/logo.png'><p>
			Hola %s, gracias por registraste en Coopsol Empleos,<p>
			Sus datos estan siendo verificados y pronto podra acceder al portal
			<p>
			Si no te has registrado, favor hacer caso omiso a este mail
			<p>
			Gracias""" % (obj.user.empresa.no_razon_social)

			enviar_email([obj.user.email], headers, body)

			headers = ["from: Coopsol Empleos <no-responder@coopsolempleos.com>",
			"subject: Nueva Empresa Registrda en Coopsol Empleos",
			"to: webmaster@coopsolempleos.com",
			"mime-version: 1.0",
			"content-type: text/html"]
			headers = "\r\n".join(headers)

			body = """<img src='http://www.coopsolempleos.com/static/images/logo.png'><p>
			Nueva empresa registrada:<p>
			<strong>Razon Social: </strong> %s<br/>
			<strong>RUC: </strong> %s<br/>
			<strong>Email: </strong> %s<br/>
			<strong>Contacto: </strong> %s<br/>
			<strong>Telefono: </strong> %s<br/>
			<strong>Email: </strong> %s<br/>
			""" % (obj.user.empresa.no_razon_social, obj.user.empresa.nu_ruc, obj.user.email, obj.user.empresa.no_contacto, obj.user.empresa.nu_telefono_contacto, obj.user.empresa.no_email_contacto)

			enviar_email(['webmaster@coopsolempleos.com'], headers, body)
			return HttpResponseRedirect('/empresa')
	else:
		formulario = EmpresaCreationCompleteForm()
	return render_to_response('empresa-completar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/empresa/ingresar')
def empresa_editar(request):
	if request.method == 'POST':
		formulario = EmpresaChangeForm(request.POST, request.FILES, instance=request.user.empresa)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/empresa')
	else:
		formulario = EmpresaChangeForm(instance=request.user.empresa)
	return render_to_response('empresa-editar.html', locals(), context_instance=RequestContext(request))

def empresa_ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/empresa')
	if request.method == 'POST':
		formulario = EmailAuthenticationForm(request.POST)
		if formulario.is_valid:
			user = authenticate(email=request.POST['email'], password=request.POST['password'])
			if user:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(request.session.get('next'))
				else:
					return HttpResponseRedirect('/usuario-inactivo')
		else:
			return render_to_response('empresa-ingresar.html', locals(), context_instance=RequestContext(request))
	else:
		formulario = EmailAuthenticationForm()
	if 'next' in request.REQUEST:
		request.session['next'] = request.REQUEST['next']
	else:
		request.session['next'] = '/'
	return render_to_response('empresa-ingresar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/empresa/ingresar')
def empresa_mostrar(request):
	empresa = Empresa.objects.filter(user=request.user)
	empleos = Empleo.objects.filter(user=request.user).order_by('-fe_creacion').order_by('-pk')[:5]
	empleospostulantes = []
	for item in empleos:
		empleospostulantes.append({'id': item.pk, 'ca_postulantes': PostulanteEmpresaEmpleo.objects.filter(empleo=item).count()})

	if not empresa:
		return HttpResponseRedirect('/empresa/completar')
	else:
		return render_to_response('empresa-mostrar.html', locals(), context_instance=RequestContext(request))

def empresa_mostrar_id(request, id_empresa):
	empresa = get_object_or_404(Empresa, pk=id_empresa)
	empleos = Empleo.objects.filter(user=empresa.user).order_by('-fe_creacion').order_by('-pk')#[:5]
	empleospostulantes = []
	for item in empleos:
		empleospostulantes.append({'id': item.pk, 'ca_postulantes': PostulanteEmpresaEmpleo.objects.filter(empleo=item).count()})

	if not empresa:
		return HttpResponseRedirect('/empresa/completar')
	else:
		return render_to_response('empresa-mostrar-id.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/empresa/ingresar')
#request.POST['email']
def empresa_empleo_agregar(request):
	if request.method == 'POST':
		formulario = EmpresaEmpleoForm(request.POST)
		if formulario.is_valid():
			obj = formulario.save(commit=False)
			obj.user = request.user
			obj.save()
			return HttpResponseRedirect('/empresa/empleo/mostrar')
	else:
		formulario = EmpresaEmpleoForm()
	return render_to_response('empresa-empleo-agregar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/empresa/ingresar')
def empresa_empleo_editar(request, id_empleo):
	empleo = Empleo.objects.get(pk=id_empleo)
	if request.method == 'POST':
		formulario = EmpresaEmpleoForm(request.POST, instance=empleo)
		if formulario.is_valid():
			obj = formulario.save(commit=False)
			obj.user = request.user
			obj.fe_modificacion = datetime.now()
			obj.save()
			return HttpResponseRedirect('/empresa')
	else:
		formulario = EmpresaEmpleoForm(instance=empleo)
	return render_to_response('empresa-empleo-editar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/empresa/ingresar')
def empresa_empleo_eliminar(request, id_empleo):
	e = get_object_or_404(Empleo, pk=id_empleo)
	e.delete()
	return HttpResponseRedirect('/empresa/empleo/mostrar/')

@login_required(login_url='/empresa/ingresar')
def empresa_empleo_clonar(request, id_empleo):
	empleo = Empleo.objects.get(pk=id_empleo)
	if request.method == 'POST':
		formulario = EmpresaEmpleoForm(request.POST)
		if formulario.is_valid():
			obj = formulario.save(commit=False)
			obj.user = request.user
			obj.fe_modificacion = datetime.now()
			obj.save()
			return HttpResponseRedirect('/empresa/empleo/mostrar')
	else:
		formulario = EmpresaEmpleoForm(instance=empleo)
	return render_to_response('empresa-empleo-agregar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/empresa/ingresar')
def empresa_empleo_mostrar(request):
	#empleos = Empleo.objects.filter(user=request.user).order_by('fe_creacion').reverse()[:15]
	empleos_list = Empleo.objects.filter(user=request.user).order_by('-fe_creacion', '-pk')
	paginator = Paginator(empleos_list, 15)
	page = request.GET.get('page')
	try:
		empleos = paginator.page(page)
	except PageNotAnInteger:
		empleos = paginator.page(1)
	except EmptyPage:
		empleos = paginator.page(paginator.num_pages)

	empleospostulantes = []
	for item in empleos:
		empleospostulantes.append({'id': item.pk, 'ca_postulantes': PostulanteEmpresaEmpleo.objects.filter(empleo=item).count()})
	return render_to_response('empresa-empleo-mostrar.html', locals(), context_instance=RequestContext(request))

def empleo_id(request, id_empleo):
	empleo = Empleo.objects.get(pk=id_empleo)
	return render_to_response('empleo-id.html', locals(), context_instance=RequestContext(request))

def empresa_empleo_id(request, id_empleo):
	empleo = Empleo.objects.get(pk=id_empleo)
	empleospostulantes = getEp(request, id_empleo)
	return render_to_response('empresa-empleo-id.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def empresa_postular_id(request, id_empleo):
	empleo = Empleo.objects.get(pk=id_empleo)
	user = request.user
	existe = PostulanteEmpresaEmpleo.objects.filter(empleo=empleo, user=user)
	if not existe:
		PostulanteEmpresaEmpleo.objects.create(empleo=empleo, user=user)
		return HttpResponseRedirect('/')
	else:
		postulando = True
		return render_to_response('empresa-empleo-id.html', locals(), context_instance=RequestContext(request))

def empresa_notificaciones(request):
	if request.method == 'POST':
		formulario = EmpresaNotificacionesForm(request.POST, request.FILES, instance=request.user.empresa)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/empresa')
	else:
		formulario = EmpresaNotificacionesForm(instance=request.user.empresa)
	return render_to_response('notificaciones.html', locals(), context_instance=RequestContext(request))

def postulante_crear(request):
	if request.method == 'POST':
		formulario = EmailUserCreationForm(request.POST)
		if formulario.is_valid():
			user = formulario.save()
			user.groups.add(Group.objects.get(pk=1)) #Postulante
			user.is_active = False
			user.save()
			acceso = authenticate(email=request.POST['email'], password=request.POST['password1'])
			if acceso is not None:
				login(request, acceso)
				return HttpResponseRedirect('/postulante/completar')
			else:
				return render_to_response('postulante-crear.html', locals(), context_instance=RequestContext(request))
	else:
		formulario = EmailUserCreationForm()
	return render_to_response('postulante-crear.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_completar(request):
	if request.method == 'POST':
		formulario = PostulanteCreationCompleteForm(request.POST, request.FILES)
		if formulario.is_valid():
			obj = formulario.save(commit=False)
			obj.user = request.user
			obj.save()
			user = request.user
			cd = _email_to_username(user.email)
			tocken = _email_to_username(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			RecuperarPassword.objects.create(
				usuario=cd,
				email=user.email,
				token=tocken
			);
			headers = ["from: Coopsol Empleos <no-responder@coopsolempleos.com>",
			"subject: Confirmacion de correo electronico",
			"to: " + user.email,
			"mime-version: 1.0",
			"content-type: text/html"]
			headers = "\r\n".join(headers)

			body = """<img src='http://www.coopsolempleos.com/static/images/logo.png'><p>
			Hola, el correo %s ha sido registrado en Coopsol Empleos,<p>
			Para confirmar tu direccion de correo electronico debes hacer click en el siguiente link<br/>
			<a href='http://www.coopsolempleos.com/activar/%s/%s'>http://www.coopsolempleos.com/activar/%s/%s</a>
			<p>
			Si el link no funciona copialo y pegalo en tu navegador
			<p>
			Si no te has registrado, favor hacer caso omiso a este mail
			<p>
			Gracias""" % (user.email,cd,tocken,cd,tocken)

			enviar_email([user.email], headers, body)
			if not request.user.is_anonymous():
				logout(request)
			return render_to_response('postulante-confirmar-correo.html', {'correo': user.email}, context_instance=RequestContext(request))
			#return HttpResponseRedirect('/postulante')
	else:
		formulario = PostulanteCreationCompleteForm()
	return render_to_response('postulante-completar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_editar(request):
	if request.method == 'POST':
		formulario = PostulanteChangeForm(request.POST, request.FILES, instance=request.user.postulante)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/postulante')
	else:
		formulario = PostulanteChangeForm(instance=request.user.postulante)
	return render_to_response('postulante-editar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_editar_password(request):
	if request.method == 'POST':
		formulario = PostulanteChangePasswordForm(data=request.POST, user=request.user)
		if formulario.is_valid():
			request.user.set_password(request.POST['password1'])
			request.user.save()
			return HttpResponseRedirect('/postulante')
	else:
		formulario = PostulanteChangePasswordForm(data=request.POST or None, user=request.user)
	return render_to_response('postulante-editar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_eliminar(request):
	if request.method == 'POST':
		formulario = ValidarPasswordForm(data=request.POST, user=request.user)
		if formulario.is_valid():
			request.user.is_active = False
			request.user.save()
			headers = ["from: Coopsol Empleos <no-responder@coopsolempleos.com>",
			"subject: Eliminacion de Cuenta",
			"to: " + request.user.email,
			"mime-version: 1.0",
			"content-type: text/html"]
			headers = "\r\n".join(headers)

			body = """<img src='http://www.coopsolempleos.com/static/images/logo.png'><p>
			Hola, el correo %s ha sido dado de baja</p><p>Gracias por utilizar 
			<a href='http://www.coopsolempleos.com'>Coopsol Empleo</a></p>""" % (request.user.email)

			enviar_email([request.user.email], headers, body)
			logout(request)
			return HttpResponseRedirect('/saludo-despedida')
	else:
		formulario = ValidarPasswordForm(user=request.user)
	return render_to_response('postulante-eliminar.html', locals(), context_instance=RequestContext(request))

def postulante_ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/postulante')
	if request.method == 'POST':
		formulario = EmailAuthenticationForm(request.POST)
		if formulario.is_valid:
			user = authenticate(email=request.POST['email'], password=request.POST['password'])
			if user:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(request.session.get('next'))
				else:
					return HttpResponseRedirect('/usuario-inactivo')
			else:
				return HttpResponseRedirect('/usuario-no-existe')
	else:
		formulario = EmailAuthenticationForm()
	if 'next' in request.REQUEST:
		request.session['next'] = request.REQUEST['next']
	else:
		request.session['next'] = '/'
	return render_to_response('postulante-ingresar.html', locals(), context_instance=RequestContext(request))

def usuario_inactivo(request):
	return render_to_response('usuario_inactivo.html', locals(), context_instance=RequestContext(request))

def usuario_no_existe(request):
	return render_to_response('usuario_no_existe.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_estudios_agregar(request):
	if request.method == 'POST':
		formulario = PostulanteEstudioForm(request.POST)
		if formulario.is_valid():
			obj = formulario.save(commit=False)
			obj.user = request.user
			obj.save()
			return HttpResponseRedirect('/postulante')
	else:
		formulario = PostulanteEstudioForm()
	return render_to_response('postulante-estudios-agregar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_estudios_editar(request, id_estudio):
	pe = get_object_or_404(PostulanteEstudio, pk=id_estudio, user=request.user)
	if request.method == 'POST':
		formulario = PostulanteEstudioForm(request.POST, instance=pe)
		if formulario.is_valid():
			obj = formulario.save(commit=False)
			obj.save()
			return HttpResponseRedirect('/postulante')
	else:
		formulario = PostulanteEstudioForm(instance=pe)
	return render_to_response('postulante-estudios-agregar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_estudios_eliminar(request, id_estudio):
	pe = get_object_or_404(PostulanteEstudio, pk=id_estudio, user=request.user)
	pe.delete()
	return HttpResponseRedirect('/postulante')

@login_required(login_url='/postulante/ingresar')
def postulante_empleos_agregar(request):
	if request.method == 'POST':
		formulario = PostulanteEmpleoForm(request.POST)
		if formulario.is_valid():
			obj = formulario.save(commit=False)
			obj.user = request.user
			obj.save()
			return HttpResponseRedirect('/postulante')
	else:
		formulario = PostulanteEmpleoForm()
	return render_to_response('postulante-empleos-agregar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_empleo_editar(request, id_empleo):
	pe = get_object_or_404(PostulanteEmpleo, pk=id_empleo, user=request.user)
	if request.method == 'POST':
		formulario = PostulanteEmpleoForm(request.POST, instance=pe)
		if formulario.is_valid():
			obj = formulario.save(commit=False)
			obj.save()
			return HttpResponseRedirect('/postulante')
	else:
		formulario = PostulanteEmpleoForm(instance=pe)
	return render_to_response('postulante-empleos-agregar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_empleo_eliminar(request, id_empleo):
	pe = get_object_or_404(PostulanteEmpleo, pk=id_empleo, user=request.user)
	pe.delete()
	return HttpResponseRedirect('/postulante')

@login_required(login_url='/postulante/ingresar')
def postulante_mostrar(request):
	try:
		postulante = Postulante.objects.get(user=request.user)
	except Exception:
		postulante = None
	estudios = PostulanteEstudio.objects.filter(user=request.user)
	empleos = PostulanteEmpleo.objects.filter(user=request.user)
	idiomas = PostulanteIdiomaNivel.objects.filter(user=request.user)
	programas = PostulanteProgramaNivel.objects.filter(user=request.user)
	if not postulante:
		return HttpResponseRedirect('/postulante/completar')
	else:
		if postulante.user.is_active:
			return render_to_response('postulante-mostrar.html', locals(), context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/usuario-inactivo')

@login_required(login_url='/empresa/ingresar')
def postulante_mostrar_id(request, id_postulante, id_empleo):
	postulante = Postulante.objects.get(user_id=id_postulante)
	estudios = PostulanteEstudio.objects.filter(user_id=id_postulante)
	empleos = PostulanteEmpleo.objects.filter(user_id=id_postulante)
	idiomas = PostulanteIdiomaNivel.objects.filter(user_id=id_postulante)
	request.id_postulante = id_postulante
	request.id_empleo = id_empleo
	if not postulante:
		return None #HttpResponseRedirect('/postulante/completar')
	else:
		return render_to_response('postulante-mostrar.html', locals(), context_instance=RequestContext(request))

def postulante_notificaciones(request):
	if request.method == 'POST':
		formulario = PostulanteNotificacionesForm(request.POST, request.FILES, instance=request.user.postulante)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/postulante')
	else:
		formulario = PostulanteNotificacionesForm(instance=request.user.postulante)
	return render_to_response('notificaciones.html', locals(), context_instance=RequestContext(request))

def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')

def sup_mostrar(request):
	return render_to_response('sup/sup.html',{}, context_instance=RequestContext(request))

def postulante_json(request):
	page = int(request.POST.get('page', 0))
	start = int(request.POST.get('start', 0))
	limit = int(request.POST.get('limit', 0))
	totalCount = Postulante.objects.all().count()
	postulantes = Postulante.objects.all()[start:limit*page]
	list = []
	for postulante in postulantes:
		item = {
			'id': postulante.pk,
			'email': postulante.user.email,
			'no_postulante': postulante.no_postulante,
			'ap_postulante': postulante.ap_postulante,
			'am_postulante': postulante.am_postulante,
			'nu_fijo': postulante.nu_fijo,
			'nu_movil': postulante.nu_movil,
			'fe_nacimiento': str(formats.date_format(postulante.fe_nacimiento, "SHORT_DATE_FORMAT")),
			'de_direccion': postulante.de_direccion,
			'ubigeo_id': postulante.ubigeo.pk,
			'no_ubigeo': postulante.ubigeo.name
		}
		list.append(item)
	context = {
		'totalCount': totalCount,
		'postulante': list,
		'success': True
	}
	return HttpResponse(json.dumps(context), mimetype="application/json")

def empresa_json(request):
	page = int(request.POST.get('page', 0))
	start = int(request.POST.get('start', 0))
	limit = int(request.POST.get('limit', 0))
	totalCount = Empresa.objects.all().count()
	empresas = Empresa.objects.all()[start:limit*page]
	list = []
	for empresa in empresas:
		item = {
			'id': empresa.pk,
			'email': empresa.user.email,
			'no_web': empresa.no_web,
			'nu_ruc': empresa.nu_ruc,
			'no_razon_social': empresa.no_razon_social,
			'no_comercial': empresa.no_comercial,
			'nu_fijo': empresa.nu_fijo,
			'nu_movil': empresa.nu_movil,
			'de_direccion': empresa.de_direccion,
			'ubigeo_id': empresa.ubigeo.pk,
			'no_ubigeo': empresa.ubigeo.name
		}
		list.append(item)
	context = {
		'totalCount': totalCount,
		'empresa': list,
		'success': True
	}
	return HttpResponse(json.dumps(context), mimetype="application/json")

def empleo_json(request):
	page = int(request.POST.get('page', 0))
	start = int(request.POST.get('start', 0))
	limit = int(request.POST.get('limit', 0))
	totalCount = Empleo.objects.all().count()
	empleos = Empleo.objects.all()[start:limit*page]
	list = []
	for empleo in empleos:
		item = {
			'id': empleo.pk,
			'no_empleo': empleo.no_empleo,
			'de_empleo': empleo.de_empleo,
			'de_requisitos': empleo.de_requisitos,
			'de_funciones': empleo.de_funciones,
			'va_sueldo': str(empleo.va_sueldo),
			'fe_creacion': str(formats.date_format(empleo.fe_creacion, "SHORT_DATE_FORMAT")),
			'area_id': empleo.area.pk,
			'no_area': empleo.area.no_area,
			'tipoempleo_id': empleo.tipoempleo.pk,
			'no_tipoempleo': empleo.tipoempleo.no_tipo_empleo,
			'ubigeo_id': empleo.ubigeo.pk,
			'no_ubigeo': empleo.ubigeo.name,
			'no_contacto': empleo.no_contacto,
			'no_contacto_telefono': empleo.no_contacto_telefono,
			'no_contacto_email': empleo.no_contacto_email,
			'user_id': empleo.user.pk,
			'no_comercial': empleo.user.empresa.no_comercial
		}
		list.append(item)
	context = {
		'totalCount': totalCount,
		'empleo': list,
		'success': True
	}
	return HttpResponse(json.dumps(context), mimetype="application/json")

def postulante_id_json(request, id_postulante):
	postulante = Postulante.objects.get(user_id=id_postulante)
	empleos = PostulanteEmpleo.objects.filter(user_id=id_postulante)
	estudios = PostulanteEstudio.objects.filter(user_id=id_postulante)
	idiomas = PostulanteIdiomaNivel.objects.filter(user_id=id_postulante)
	programas = PostulanteProgramaNivel.objects.filter(user_id=id_postulante)
	td = datetime.now() - datetime(postulante.fe_nacimiento.year, postulante.fe_nacimiento.month, postulante.fe_nacimiento.day)
	anios = td.days / 365
	_postulante = {
		'id': postulante.pk,
		'im_foto': str(postulante.im_foto),
		'no_postulante': postulante.no_postulante+' '+postulante.ap_postulante+' '+postulante.am_postulante,
		'de_direccion': postulante.de_direccion,
		'no_distrito': postulante.ubigeo.name,
		'email': postulante.user.email,
		'fe_nacimiento': str(postulante.fe_nacimiento),
		'anios': anios,
		'nu_fijo': postulante.nu_fijo,
		'nu_movil': postulante.nu_movil,
		'de_sobremi': postulante.de_sobremi,
		'empleos': [],
		'estudios': [],
		'idiomas': [],
		'programas': []
	}
	for empleo in empleos:
		_postulante['empleos'].append({
				'fe_periodo_ini': empleo.fe_periodo_ini,
				'fe_periodo_fin': empleo.fe_periodo_fin,
				'fl_actualidad': empleo.fl_actualidad,
				'no_cargo': empleo.no_cargo,
				'no_empresa': empleo.no_empresa,
				'no_referencia': empleo.no_referencia,
				'no_referencia_cargo': empleo.no_referencia_cargo,
				'nu_referencia_telefono': empleo.nu_referencia_telefono
			})
	for estudio in estudios:
		_postulante['estudios'].append({
				'fe_periodo_ini': estudio.fe_periodo_ini,
				'fe_periodo_fin': estudio.fe_periodo_fin,
				'fl_actualidad': estudio.fl_actualidad,
				'no_carrera': estudio.carrera.no_carrera,
				'no_institucion': estudio.institucion.no_universidad
			})
	for idioma in idiomas:
		_postulante['idiomas'].append({
				'no_idioma': idioma.idioma.no_idioma,
				'no_nivel': idioma.nivel.no_nivel
			})
	for programa in programas:
		_postulante['programas'].append({
				'no_programa': programa.programa.no_programa,
				'no_nivel': programa.nivel.no_nivel
			})
	
	return HttpResponse(json.dumps(_postulante), mimetype="application/json")

@login_required(login_url='/postulante/ingresar')
def mensaje_mostrar(request, id_filtro):
	if (id_filtro == '1'): #todo
		mensajes = MensajeDirecto.objects.filter(destinatario=request.user)
	elif (id_filtro == '2'): #sin leer
		mensajes = MensajeDirecto.objects.filter(destinatario=request.user, fl_revisado=0)
	elif (id_filtro == '3'): #leido
		mensajes = MensajeDirecto.objects.filter(destinatario=request.user, fl_revisado=1)
	return render_to_response('mensaje-mostrar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def mensaje_enviar(request, id_destinatario, id_empleo, id_mensaje):
	destinatario = User.objects.get(pk=id_destinatario)
	try:
		mensajedirecto = MensajeDirecto.objects.get(pk=id_mensaje)
	except Exception:
		mensajedirecto = None
	if request.method == 'POST':
		formulario = MensajeDirectoForm(request.POST)
		if formulario.is_valid():
			for group in request.user.groups.all():
				group_pk = group.pk
			obj = formulario.save(commit=False)
			obj.remitente = request.user
			_destinatario = User.objects.get(pk=id_destinatario)
			obj.destinatario = _destinatario
			if group_pk == 1:
				obj.postulanteempresaempleo = PostulanteEmpresaEmpleo.objects.get(empleo_id=id_empleo, user=request.user)
			elif group_pk == 2:
				obj.postulanteempresaempleo = PostulanteEmpresaEmpleo.objects.get(empleo_id=id_empleo, user=_destinatario)
			ultimo_id = obj.save()

			receivers = [_destinatario.email]

			headers = ["from: Coopsol Empleos <no-responder@coopsolempleos.com>",
			"subject: Nuevo mensaje desde Coopsol Empleos",
			"to: " + _destinatario.email,
			"mime-version: 1.0",
			"content-type: text/html"]

			headers = "\r\n".join(headers)
			body = """<img src='http://www.coopsolempleos.com/static/images/logo.png'><p>
			Ha recibido un mensaje nuevo, para revisarlo debe dirigirse a <a href='http://www.coopsolempleos.com/mensaje/leer/%s'>http://www.coopsolempleos.com/mensaje/leer/25</a>""" % ultimo_id

			enviar_email(receivers, headers, body)

			if group_pk == 1:
				return HttpResponseRedirect('/mensaje/mostrar/1')
			elif group_pk == 2:
				return HttpResponseRedirect('/mensaje/mostrar/1')
			else:
				return HttpResponseRedirect('/')
	else:
		if mensajedirecto is not None:
			formulario = MensajeDirectoForm({'de_asunto': 'RE: ' + mensajedirecto.de_asunto})
		else:
			formulario = MensajeDirectoForm()
	return render_to_response('mensaje-enviar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def mensaje_leer_id(request, id_mensaje):
	mensaje = get_object_or_404(MensajeDirecto, pk=id_mensaje)
	if mensaje.destinatario != request.user:
		return HttpResponseRedirect('/404')
	mensaje.fl_revisado = True
	mensaje.fe_revisado = datetime.now()
	mensaje.save()
	return render_to_response('mensaje-leer-id.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_idiomas_agregar(request):
	if request.method == 'POST':
		formulario = PostulanteIdiomaNivelForm(request.POST)
		if formulario.is_valid():
			obj = formulario.save(commit=False)
			obj.user = request.user
			obj.save()
			return HttpResponseRedirect('/postulante')
	else:
		formulario = PostulanteIdiomaNivelForm()
	return render_to_response('postulante-idiomas-agregar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_idiomas_editar(request, id_idioma):
	pin = get_object_or_404(PostulanteIdiomaNivel, pk=id_idioma, user=request.user)
	if request.method == 'POST':
		formulario = PostulanteIdiomaNivelForm(request.POST, instance=pin)
		if formulario.is_valid():
			obj = formulario.save(commit=False)
			obj.save()
			return HttpResponseRedirect('/postulante')
	else:
		formulario = PostulanteIdiomaNivelForm(instance=pin)
	return render_to_response('postulante-idiomas-agregar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_idiomas_eliminar(request, id_idioma):
	pin = get_object_or_404(PostulanteIdiomaNivel, pk=id_idioma, user=request.user)
	pin.delete()
	return HttpResponseRedirect('/postulante')

@login_required(login_url='/postulante/ingresar')
def postulante_postulaciones(request):
	postulanteEmpresaEmpleo = PostulanteEmpresaEmpleo.objects.filter(user_id=request.user.pk)
	return render_to_response('postulante-postulaciones.html', locals(), context_instance=RequestContext(request))

def _404(request):
	return render_to_response('404.html', locals(), context_instance=RequestContext(request))

def recuperar_password(request):
	if request.method == 'POST':
		formulario = RecuperarPasswordForm(request.POST)
		if formulario.is_valid():
			if User.objects.filter(email=request.POST['email']).count() == 0:
				return HttpResponseRedirect('/recuperar/error/%s' % request.POST['email'])

			receivers = [request.POST['email']]
			cd = _email_to_username(request.POST['email'])
			tocken = _email_to_username(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			RecuperarPassword.objects.create(
				usuario=cd,
				email=request.POST['email'],
				token=tocken
				);
			headers = ["from: Coopsol Empleos <no-responder@coopsolempleos.com>",
			"subject: Cambiar Clave de Acceso",
			"to: " + request.POST['email'],
			"mime-version: 1.0",
			"content-type: text/html"]

			headers = "\r\n".join(headers)
			body = """<img src='http://www.coopsolempleos.com/static/images/logo.png'><p>
			Para cambiar su clave haga click en el siguiente enlace <a href='http://www.coopsolempleos.com/recuperar/cambiar/%s/%s'>http://www.coopsolempleos.com/recuperar/cambiar/%s</a>""" % (cd,tocken,tocken)

			if enviar_email(receivers, headers, body) is None:
				return HttpResponseRedirect('/recuperar')
			else:
				return HttpResponseRedirect('/recuperar/email/%s' % request.POST['email'])
	else:
		formulario = RecuperarPasswordForm()
	return 	render_to_response('recuperar-password.html', locals(), context_instance=RequestContext(request))

def recuperar_error(request, email):
	return 	render_to_response('recuperar-error.html', locals(), context_instance=RequestContext(request))

def recuperar_password_cambiar(request, email, token):
	if request.method == 'POST':
		formulario = PostulanteRecuperarPasswordForm(request.POST)
		if formulario.is_valid():
			rp = RecuperarPassword.objects.get(usuario=email, token=token);
			user = User.objects.get(email=rp.email)
			user.set_password(request.POST['password2'])
			user.fl_usado = True
			user.save()
			return HttpResponseRedirect('/postulante')
	else:
		formulario = PostulanteRecuperarPasswordForm()
		try:
			rp = RecuperarPassword.objects.get(usuario=email, token=token, fl_usado=0);
		except Exception:
			return HttpResponseRedirect('/')
	return render_to_response('recuperar-password-cambiar.html', locals(), context_instance=RequestContext(request))

def recuperar_password_email_enviado(request, email):
	return 	render_to_response('recuperar-password-email-enviado.html', locals(), context_instance=RequestContext(request))

def activar(request, email, token):
	rp = get_object_or_404(RecuperarPassword, usuario=email, token=token);
	user = User.objects.get(email=rp.email)
	rp.fl_usado = True
	rp.save()
	user.is_active = True
	user.save()
	receivers = [user.email]
	headers = ["from: Coopsol Empleos <no-responder@coopsolempleos.com>",
	"subject: Registro completado",
	"to: " + user.email,
	"mime-version: 1.0",
	"content-type: text/html"]
	headers = "\r\n".join(headers)

	body = """<img src='http://www.coopsolempleos.com/static/images/logo.png'><p>
	Hola %s,<p>
	Gracias por registrarte a Coopsol Empleos""" % user.postulante

	enviar_email(receivers, headers, body)
	if not request.user.is_anonymous():
		logout(request)
	formulario = EmailAuthenticationForm()
	request.session['activo'] = True
	return render_to_response('postulante-ingresar.html', {'activo': True, 'formulario': formulario}, context_instance=RequestContext(request))
	#return HttpResponseRedirect('/postulante')

def universidad_json(request, name):
	universidades = Universidad.objects.filter(no_universidad__icontains=name)[:10]
	list = []
	for universidad in universidades:
		item = {
			'name': universidad.no_universidad
		}
		list.append(item)
	context = {
		'data': list
	}
	return HttpResponse(json.dumps(context), mimetype="application/json")

def carrera_json(request, name):
	carreras = Carrera.objects.filter(no_carrera__icontains=name)[:10]
	list = []
	for carrera in carreras:
		item = {
			'name': carrera.no_carrera
		}
		list.append(item)
	context = {
		'data': list
	}
	return HttpResponse(json.dumps(context), mimetype="application/json")

def idioma_json(request, name):
	idiomas = Idioma.objects.filter(no_idioma__icontains=name)[:10]
	list = []
	for idioma in idiomas:
		item = {
			'name': idioma.no_idioma
		}
		list.append(item)
	context = {
		'data': list
	}
	return HttpResponse(json.dumps(context), mimetype="application/json")

def programa_json(request, name):
	programas = Programa.objects.filter(no_programa__icontains=name)[:10]
	list = []
	for programa in programas:
		item = {
			'name': programa.no_programa
		}
		list.append(item)
	context = {
		'data': list
	}
	return HttpResponse(json.dumps(context), mimetype="application/json")	

def enviar_email(receivers, headers, body):
	sender = 'webmaster@coopsolempleos.com'

	try:
		smtpObj = smtplib.SMTP('192.168.0.4')
		smtpObj.sendmail(sender, receivers, headers + "\r\n\r\n" + body)
		return smtpObj
	except Exception:
		return None

@login_required(login_url='/postulante/ingresar')
def postulante_programas_agregar(request):
	if request.method == 'POST':
		formulario = PostulanteProgramaNivelForm(request.POST)
		if formulario.is_valid():
			obj = formulario.save(commit=False)
			obj.user = request.user
			obj.save()
			return HttpResponseRedirect('/postulante')
	else:
		formulario = PostulanteProgramaNivelForm()
	return render_to_response('postulante-idiomas-agregar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_programas_editar(request, id_programa):
	ppn = get_object_or_404(PostulanteProgramaNivel, pk=id_programa, user=request.user)
	if request.method == 'POST':
		formulario = PostulanteProgramaNivelForm(request.POST, instance=ppn)
		if formulario.is_valid():
			obj = formulario.save(commit=False)
			obj.save()
			return HttpResponseRedirect('/postulante')
	else:
		formulario = PostulanteProgramaNivelForm(instance=ppn)
	return render_to_response('postulante-idiomas-agregar.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/postulante/ingresar')
def postulante_programas_eliminar(request, id_programa):
	ppn = get_object_or_404(PostulanteProgramaNivel, pk=id_programa, user=request.user)
	ppn.delete()
	return HttpResponseRedirect('/postulante')

def saludo_despedida(request):
	return render_to_response('saludo-despedida.html', locals(), context_instance=RequestContext(request))

def empresa_eliminar(request):
	return render_to_response('empresa-eliminar.html', locals(), context_instance=RequestContext(request))

def busqueda_avanzada(request):
	formulario = BusquedaAvanzadaForm()
	return render_to_response('postulante-idiomas-agregar.html', {'formulario': formulario}, context_instance=RequestContext(request))

def distritos_json(request):
    #28692 = Lima
    distritos = Ubigeo.objects.filter(parent_id=28692).order_by('name')
    i = []
    for distrito in distritos:    	
		i.append({
			'id': distrito.pk,
			'nombre': '%s(%s)' % (distrito.name, Empleo.objects.filter(ubigeo_id=distrito.pk).count())
			})
    return HttpResponse(json.dumps(i), mimetype="application/json")

def areas_json(request):
	distrito_id = request.GET.get('distrito_id')
	if distrito_id:
		empleos = Empleo.objects.filter(ubigeo_id=distrito_id)
		areas = []

		for empleo in empleos:
			if empleo.area not in areas:
				areas.append(empleo.area)
	else:
		areas = Area.objects.all().order_by('no_area')
	i = []
	for area in areas:
		if distrito_id:
			count = Empleo.objects.filter(area_id=area.pk, ubigeo_id=distrito_id).count()
		else:
			count = Empleo.objects.filter(area_id=area.pk).count()
		i.append({
			'id': area.pk,
			'nombre': '%s(%s)' % (area.no_area, count)
		})
	return HttpResponse(json.dumps(i), mimetype="application/json")

def terminos_condiciones(request):
	return render_to_response('terminos-condiciones.html', context_instance=RequestContext(request))

def nosotros(request):
	return render_to_response('nosotros.html', context_instance=RequestContext(request))

def preguntas_frecuentes(request):
	return render_to_response('preguntas-frecuentes.html', context_instance=RequestContext(request))

def libro_reclamaciones(request):
	return render_to_response('libro-reclamaciones.html', context_instance=RequestContext(request))

def nuestros_clientes(request):
	return render_to_response('nuestros-clientes.html', context_instance=RequestContext(request))