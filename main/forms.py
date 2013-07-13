#encoding:utf-8
from django.forms import ModelForm, CharField, BooleanField, PasswordInput, HiddenInput, TextInput, Textarea
from django import forms
from main.models import Area, Empresa, Postulante, PostulanteEstudio, PostulanteEmpleo, Empleo, MensajeDirecto, PostulanteIdiomaNivel, Universidad, Carrera, PostulanteProgramaNivel, Idioma, Programa, EmpleoPregunta, EmpleoPreguntaPostulante
from django.forms import extras
from django.core.validators import validate_email
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from ubigeo.models import Ubigeo
from ubigeo.fields import UbigeoField
from ubigeo import constant
from django.core.files.images import get_image_dimensions
from captcha.fields import ReCaptchaField

#class _EmailUserCreationForm(EmailUserCreationForm):
#	captcha = ReCaptchaField(attrs={'theme' : 'clean'})

class PostulanteChangeForm(ModelForm):
	ubigeo = UbigeoField()
	im_foto = forms.ImageField(label='Foto', help_text='Resolucion sugerida 160x180', required=False)

	class Meta:
		model = Postulante
		exclude = ('user', 'fl_notificaciones',)

	def clean_ubigeo(self):
		ubigeo = self.cleaned_data.get("ubigeo")
		if ubigeo is None:
			raise forms.ValidationError("Este campo es obligatorio.")
		else:
			return ubigeo

class PostulanteChangePasswordForm(forms.Form):
	password0 = forms.CharField(label='Contraseña Actual', widget=PasswordInput())
	password1 = forms.CharField(label='Contraseña', widget=PasswordInput())
	password2 = forms.CharField(label='Contraseña (confirmación)', widget=PasswordInput(), help_text="Introduzca la misma contraseña que arriba, para verificación.")

	def __init__(self, user, *args, **kwargs):
		super(PostulanteChangePasswordForm, self).__init__(*args, **kwargs)
		self.user = user

	def clean_password0(self):
		valid = self.user.check_password(self.cleaned_data.get("password0"))
		if not valid:
			raise forms.ValidationError("Contraseña actual incorrecta")
		return valid

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 != password2:
			raise forms.ValidationError("Las contraseñas deben coincidir")
		return password2

class PostulanteRecuperarPasswordForm(forms.Form):
	password1 = forms.CharField(label='Contraseña', widget=PasswordInput())
	password2 = forms.CharField(label='Contraseña (confirmación)', widget=PasswordInput(), help_text="Introduzca la misma contraseña que arriba, para verificación.")

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 != password2:
			raise forms.ValidationError("Las contraseñas deben coincidir")
		return password2

class PostulanteCreationCompleteForm(ModelForm):
	my_default_errors = {
	    'required': 'Este campo es obligatorio',
	    'invalid': 'EL valor ingresado es invalido'
	}

	ubigeo = UbigeoField()
	im_foto = forms.ImageField(label='Foto', help_text='Resolucion sugerida 160x180', required=False)

	class Meta:
		model = Postulante
		exclude = ('user', 'fl_notificaciones', )

	#def clean_im_foto(self):
	#	picture = self.cleaned_data.get("im_foto")
	#	if not picture:
	#		return picture
	#	elif picture._size > 100000:
	#		raise forms.ValidationError("Archivo de imagen muy largo, reomendado <= 100KB")
	#	else:
	#		w, h = get_image_dimensions(picture)
	#		if w > 160:
	#			raise forms.ValidationError("La imagen tiene %ipx de ancho. No debe pasar de 160px" % w)
	#		if h > 180:
	#			raise forms.ValidationError("La imagen tiene %ipx de alto. No debe pasar de 180px" % h)
	#	return picture

	def clean_ubigeo(self):
		ubigeo = self.cleaned_data.get("ubigeo")
		if ubigeo is None:
			raise forms.ValidationError("Este campo es obligatorio.")
		else:
			return ubigeo

class PostulanteEstudioForm(ModelForm):
	institucion = forms.CharField(max_length=255)
	carrera = forms.CharField(max_length=255)

	fl_actualidad = forms.BooleanField(label='Carrera aun en curso', required=False)

	def __init__(self, *args, **kwargs):
		super(PostulanteEstudioForm, self).__init__(*args, **kwargs)
		try:
			self.initial['institucion'] = self.instance.institucion
			self.initial['carrera'] = self.instance.carrera
		except Exception:
			return None

	class Meta:
		model = PostulanteEstudio
		exclude = ('user')

	def clean_institucion(self):
		institucion = self.cleaned_data.get("institucion")
		try:
			obj = Universidad.objects.get(no_universidad=institucion)
		except Exception:
			obj = Universidad.objects.create(
				no_universidad = institucion
			)
		return obj

	def clean_carrera(self):
		carrera = self.cleaned_data.get("carrera")
		try:
			obj = Carrera.objects.get(no_carrera=carrera)
		except Exception:
			obj = Carrera.objects.create(
				no_carrera = carrera
			)
		return obj

class PostulanteEmpleoForm(ModelForm):
	fl_actualidad = forms.BooleanField(label='Empleo actual', required=False)
	class Meta:
		model = PostulanteEmpleo
		exclude = ('user')

class EmpresaCreationCompleteForm(ModelForm):

	ubigeo = UbigeoField(label='Region', ubigeo=constant.ONLY_PERU)
	#im_logo = forms.ImageField(label='Logo', help_text='Resolucion aceptada 160x180', required=False)
	nu_ruc = forms.CharField(label='RUC', max_length=11, widget=TextInput(attrs={'class': 'solo-numeros'}))

	class Meta:
		model = Empresa
		exclude = ('user', 'fl_notificaciones', )

	def clean_ubigeo(self):
		ubigeo = self.cleaned_data.get("ubigeo")
		if ubigeo is None:
			raise forms.ValidationError("Este campo es obligatorio.")
		else:
			return ubigeo

	#def clean_im_logo(self):
	#	picture = self.cleaned_data.get("im_logo")
	#	if not picture:
	#		raise forms.ValidationError("No hay archivo")
	#	elif picture._size > 100000:
	#		raise forms.ValidationError("Archivo de imagen muy largo, reomendado <= 100KB")
	#	else:
	#		w, h = get_image_dimensions(picture)
	#		if w > 160:
	#			raise forms.ValidationError("La imagen tiene %ipx de ancho. No debe pasar de 160px" % w)
	#		if h > 180:
	#			raise forms.ValidationError("La imagen tiene %ipx de alto. No debe pasar de 180px" % h)
	#	return picture

class EmpresaChangeForm(ModelForm):
	ubigeo = UbigeoField()
	#im_logo = forms.ImageField(label='Logo', help_text='Resolucion sugerida 160x180', required=False)

	class Meta:
		model = Empresa
		exclude = ('user', 'fl_notificaciones', )

	def clean_ubigeo(self):
		ubigeo = self.cleaned_data.get("ubigeo")
		if ubigeo is None:
			raise forms.ValidationError("Este campo es obligatorio.")
		else:
			return ubigeo

class EmpresaEmpleoForm(ModelForm):
	ubigeo = UbigeoField() #ubigeo=constant.ONLY_PERU
	#pregunta_1 = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'ancho_410 pregunta'}), required=False)
	pregunta_1 = forms.CharField();
	pregunta_2 = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'ancho_410 pregunta'}), required=False)
	pregunta_3 = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'ancho_410 pregunta'}), required=False)
	pregunta_4 = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'ancho_410 pregunta'}), required=False)
	pregunta_5 = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'ancho_410 pregunta'}), required=False)
	pregunta_6 = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'ancho_410 pregunta'}), required=False)
	pregunta_7 = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'ancho_410 pregunta'}), required=False)
	pregunta_8 = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'ancho_410 pregunta'}), required=False)
	pregunta_9 = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'ancho_410 pregunta'}), required=False)
	pregunta_10 = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'ancho_410 pregunta'}), required=False)
	#extra_field_count = forms.CharField(max_length=255, widget=forms.HiddenInput())

	def __init__(self, empleopreguntas, *args, **kwargs):
		super(EmpresaEmpleoForm, self).__init__(*args, **kwargs)
		#empleopreguntas = kwargs.pop('empleopreguntas', None)
		self.fields['pregunta_1'].widget.attrs['class'] = 'ancho_410 pregunta'
		i=1
		for empleopregunta in empleopreguntas:
			self.fields['pregunta_%d'%i].initial = empleopregunta.pregunta
			i+=1
	#def __init__(self, *args, **kwargs):
	#	extra_fields = kwargs.pop('extra', 0)
	#	super(EmpresaEmpleoForm, self).__init__(*args, **kwargs)
	#	self.fields['extra_field_count'].initial = extra_fields
	#	for index in range(extra_fields):
	#		self.fields['extra_field_{index}'.format(index=index)] = forms.CharField(max_length=255)

	class Meta:
		model = Empleo
		exclude = ('user')

	def clean_ubigeo(self):
			ubigeo = self.cleaned_data['ubigeo']
			if not ubigeo:
				raise forms.ValidationError("El ubigeo no puede ser vacio")
			else:
				return ubigeo

class MensajeDirectoForm(ModelForm):
	class Meta:
		model = MensajeDirecto
		exclude = ('fl_revisado', 'fe_revisado', 'de_adjunto', 'remitente', 'destinatario', 'postulanteempresaempleo')

class PostulanteIdiomaNivelForm(ModelForm):
	idioma = forms.CharField(max_length=255)

	def __init__(self, *args, **kwargs):
		super(PostulanteIdiomaNivelForm, self).__init__(*args, **kwargs)
		try:
			self.initial['idioma'] = self.instance.idioma
		except Exception:
			return None

	class Meta:
		model = PostulanteIdiomaNivel
		exclude = ('user')

	def clean_idioma(self):
		idioma = self.cleaned_data.get("idioma")
		try:
			obj = Idioma.objects.get(no_idioma=idioma)
		except Exception:
			obj = Idioma.objects.create(
				no_idioma = idioma
			)
		return obj

class RecuperarPasswordForm(forms.Form):
	email = forms.EmailField(label='Correo Electronico')

	def clean_email(self):
		email = self.cleaned_data.get("email")
		if email is None:
			raise forms.ValidationError("Debe ingresar un correo electronico valido")
		return email

class PostulanteProgramaNivelForm(ModelForm):
	programa = forms.CharField(max_length=255)

	def __init__(self, *args, **kwargs):
		super(PostulanteProgramaNivelForm, self).__init__(*args, **kwargs)
		try:
			self.initial['programa'] = self.instance.programa
		except Exception:
			return None

	class Meta:
		model = PostulanteProgramaNivel
		exclude = ('user')

	def clean_programa(self):
		programa = self.cleaned_data.get("programa")
		try:
			obj = Programa.objects.get(no_programa=programa)
		except Exception:
			obj = Programa.objects.create(
				no_programa = programa
			)
		return obj

class EmpresaNotificacionesForm(ModelForm):
	class Meta:
		model = Empresa
		fields =('fl_notificaciones',)

class PostulanteNotificacionesForm(ModelForm):
	class Meta:
		model = Postulante
		fields =('fl_notificaciones',)

class ValidarPasswordForm(forms.Form):
	password = forms.CharField(label='Contraseña', widget=PasswordInput())

	def __init__(self, user, *args, **kwargs):
		super(ValidarPasswordForm, self).__init__(*args, **kwargs)
		self.user = user
		
	def clean_password(self):
		valid = self.user.check_password(self.cleaned_data.get("password"))
		if not valid:
			raise forms.ValidationError("Contraseña incorrecta")
		return valid

class BusquedaAvanzadaForm(forms.Form):
	#departamento = forms.ModelChoiceField(Ubigeo.objects.filter(political_division=1), widget=forms.Select)
	#provincias = forms.ModelChoiceField(Ubigeo.objects.filter(political_division=1), widget=forms.Select)
	distritos = forms.ChoiceField()
	areas = forms.ChoiceField()
	#text = forms.CharField(widget=HiddenInput(attrs={'name': 'tex_buscar'}))
	#text = forms.HiddenInput()

class EmpresaPostularPreguntasForm(forms.Form):

	def __init__(self, empleopreguntas, *args, **kwargs):
		super(EmpresaPostularPreguntasForm, self).__init__(*args, **kwargs)
		#i=1
		for i, empleopregunta in enumerate(empleopreguntas): # for i, question in enumerate(extra):
			i+=1
			self.fields['pregunta_%s'%i] = forms.CharField(label=empleopregunta.pregunta, max_length=255, required=True) #self.fields['fieldname_%s' % i] = forms.CharField(label=question)
			self.fields['pregunta_%s'%i].widget.attrs['class'] = 'ancho_410'
	#def __init__(self, *args, **kwargs):
	#	extra_fields = kwargs.pop('extra', 0)
	#	super(EmpresaEmpleoForm, self).__init__(*args, **kwargs)
	#	self.fields['extra_field_count'].initial = extra_fields
	#	for index in range(extra_fields):
	#		self.fields['extra_field_{index}'.format(index=index)] = forms.CharField(max_length=255)