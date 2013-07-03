from main.models import Area, Empleo, Empresa, MensajeDirecto, TipoEmpleo, Ubigeo
from emailusernames.forms import EmailUserCreationForm
from main.forms import BusquedaAvanzadaForm

def globals(request):
	areas = Area.objects.all()[:10]
	empleosareas = []
	for item in Area.objects.all():
		empleosareas.append({'id': item.id, 'ca_empleos': Empleo.objects.filter(area=item).count()})

	empresas = Empresa.objects.all()[:10]
	empleosempresas = []
	for item in Empresa.objects.all():
		empleosempresas.append({'id': item.id,'ca_empleos': Empleo.objects.filter(user_id=item.user.id).count()})

	tipoempleos = TipoEmpleo.objects.all()
	empleostipoempleos = []
	for item in TipoEmpleo.objects.all():
		empleostipoempleos.append({'id': item.id,'ca_empleos': Empleo.objects.filter(tipoempleo=item).count()})

	mensajesCount = 0
	if not request.user.is_anonymous():
		mensajesCount = MensajeDirecto.objects.filter(destinatario=request.user, fl_revisado=0).count()

	formulario_d = EmailUserCreationForm()

	distrito = ""
	departamento = ""

	#if not request.user.is_anonymous():
	if request.user.groups.filter(pk=1).count() > 0:
		distrito = request.user.postulante.ubigeo
		departamento = Ubigeo.objects.get(pk=distrito.parent_id)

	formularioBA = BusquedaAvanzadaForm()

	data = {
		'areas': areas,
		'empleosareas': empleosareas,
		'empresas': empresas,
		'empleosempresas': empleosempresas,
		'tipoempleos': tipoempleos,
		'empleostipoempleos': empleostipoempleos,
		'mensajesCount': mensajesCount,
		'formulario_d': formulario_d,
		'distrito': distrito,
		'departamento': departamento,
		'formularioBA': formularioBA
	}
	return data