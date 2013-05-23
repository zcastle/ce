from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
##from django_facebook import signals
from django.http import HttpResponseRedirect
##from main.models import MyFacebookProfileModel
from django.contrib.auth.models import User

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coopsolempleos.views.home', name='home'),
    # url(r'^coopsolempleos/', include('coopsolempleos.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root': settings.MEDIA_ROOT,}
    ),
    url(r'^ubigeo/', include('ubigeo.urls')),
    url(r'', include('social_auth.urls')),

    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^accounts/', include('django_facebook.auth_urls')), #Don't add this line if you use django registration or userena for registration and auth.

    url(r'^$', 'main.views.home'),
    url(r'^buscar/$', 'main.views.buscar'),

    url(r'^empresa/$', 'main.views.empresa_mostrar'),
    url(r'^empresa/mostrar/(?P<id_empresa>\d+)$', 'main.views.empresa_mostrar_id'),
    url(r'^empresa/(?P<id_empresa>\d+)$', 'main.views.listar_por_empresas'),
    url(r'^empresas/$', 'main.views.listar_empresas'),
    url(r'^empresa/crear$', 'main.views.empresa_crear'),
    url(r'^empresa/completar$', 'main.views.empresa_completar'),
    url(r'^empresa/editar/$', 'main.views.empresa_editar'),
    url(r'^empresa/ingresar/$', 'main.views.empresa_ingresar'),
    url(r'^empresa/eliminar/$', 'main.views.empresa_eliminar'),
    url(r'^empresa/empleo/agregar/$', 'main.views.empresa_empleo_agregar'),
    url(r'^empresa/empleo/editar/(?P<id_empleo>\d+)$', 'main.views.empresa_empleo_editar'),
    url(r'^empresa/empleo/eliminar/(?P<id_empleo>\d+)$', 'main.views.empresa_empleo_eliminar'),
    url(r'^empresa/empleo/mostrar/$', 'main.views.empresa_empleo_mostrar'),
    url(r'^empresa/empleo/clonar/(?P<id_empleo>\d+)$', 'main.views.empresa_empleo_clonar'),
    url(r'^empresa/empleo/(?P<id_empleo>\d+)$', 'main.views.empresa_empleo_id'),
    url(r'^empresa/postular/(?P<id_empleo>\d+)$', 'main.views.empresa_postular_id'),
    url(r'^empresa/notificaciones/$', 'main.views.empresa_notificaciones'),
    
    url(r'^postulante/$', 'main.views.postulante_mostrar'),
    url(r'^postulante/(?P<id_postulante>\d+)/(?P<id_empleo>\d+)$', 'main.views.postulante_mostrar_id'),
    url(r'^postulante/crear$', 'main.views.postulante_crear'),
    url(r'^postulante/completar$', 'main.views.postulante_completar'),
    url(r'^postulante/editar/$', 'main.views.postulante_editar'),
    url(r'^postulante/editar/password/$', 'main.views.postulante_editar_password'),
    url(r'^postulante/ingresar/$', 'main.views.postulante_ingresar'),
    url(r'^postulante/eliminar/$', 'main.views.postulante_eliminar'),
    url(r'^postulante/estudios/agregar/$', 'main.views.postulante_estudios_agregar'),
    url(r'^postulante/estudios/editar/(?P<id_estudio>\d+)$', 'main.views.postulante_estudios_editar'),
    url(r'^postulante/estudios/eliminar/(?P<id_estudio>\d+)$', 'main.views.postulante_estudios_eliminar'),
    url(r'^postulante/empleos/agregar/$', 'main.views.postulante_empleos_agregar'),
    url(r'^postulante/empleos/editar/(?P<id_empleo>\d+)$', 'main.views.postulante_empleo_editar'),
    url(r'^postulante/empleos/eliminar/(?P<id_empleo>\d+)$', 'main.views.postulante_empleo_eliminar'),
    url(r'^postulante/idiomas/agregar/$', 'main.views.postulante_idiomas_agregar'),
    url(r'^postulante/idiomas/editar/(?P<id_idioma>\d+)$', 'main.views.postulante_idiomas_editar'),
    url(r'^postulante/idiomas/eliminar/(?P<id_idioma>\d+)$', 'main.views.postulante_idiomas_eliminar'),
    url(r'^postulante/programas/agregar/$', 'main.views.postulante_programas_agregar'),
    url(r'^postulante/programas/editar/(?P<id_programa>\d+)$', 'main.views.postulante_programas_editar'),
    url(r'^postulante/programas/eliminar/(?P<id_programa>\d+)$', 'main.views.postulante_programas_eliminar'),
    url(r'^postulante/postulaciones/$', 'main.views.postulante_postulaciones'),
    url(r'^postulante/notificaciones/$', 'main.views.postulante_notificaciones'),
    
    url(r'^area/(?P<id_area>\d+)$', 'main.views.listar_por_areas'),
    url(r'^areas/$', 'main.views.listar_areas'),
    url(r'^empleo/(?P<id_empleo>\d+)$', 'main.views.empleo_id'),
    url(r'^cerrar/$', 'main.views.cerrar'),
    url(r'^sup/$', 'main.views.sup_mostrar'),
    url(r'^sup/postulante_json$', 'main.views.postulante_json'),
    url(r'^sup/empresa_json$', 'main.views.empresa_json'),
    url(r'^sup/empleo_json$', 'main.views.empleo_json'),
    url(r'^sup/postulante_id_json/(?P<id_postulante>\d+)$', 'main.views.postulante_id_json'),

    url(r'^mensaje/mostrar/(?P<id_filtro>\d+)$', 'main.views.mensaje_mostrar'),
    url(r'^mensaje/leer/(?P<id_mensaje>\d+)$', 'main.views.mensaje_leer_id'),
    url(r'^mensaje/enviar/(?P<id_destinatario>\d+)/(?P<id_empleo>\d+)/(?P<id_mensaje>\d+)$', 'main.views.mensaje_enviar'),

    url(r'^tipoempleo/(?P<id_tipo_empleo>\d+)$', 'main.views.listar_por_tipo_empleo'),

    url(r'^recuperar/$', 'main.views.recuperar_password'),
    url(r'^recuperar/cambiar/(?P<email>.+)/(?P<token>.+)$', 'main.views.recuperar_password_cambiar'),
    url(r'^recuperar/email/(?P<email>.+)$', 'main.views.recuperar_password_email_enviado'),
    url(r'^recuperar/error/(?P<email>.+)$', 'main.views.recuperar_error'),

    url(r'^404$', 'main.views._404'),

    url(r'^universidad-json/(?P<name>.+)$', 'main.views.universidad_json'),
    url(r'^carrera-json/(?P<name>.+)$', 'main.views.carrera_json'),
    url(r'^idioma-json/(?P<name>.+)$', 'main.views.idioma_json'),
    url(r'^programa-json/(?P<name>.+)$', 'main.views.programa_json'),

    url(r'^usuario-inactivo/$', 'main.views.usuario_inactivo'),
    url(r'^usuario-no-existe/$', 'main.views.usuario_no_existe'),
    url(r'^activar/(?P<email>.+)/(?P<token>.+)$', 'main.views.activar'),
    
    url(r'^saludo-despedida/$', 'main.views.saludo_despedida'),
    url(r'^distritos-json/$', 'main.views.distritos_json'),
    url(r'^areas-json/$', 'main.views.areas_json'),

    url(r'^terminos-condiciones/$', 'main.views.terminos_condiciones'),
    url(r'^nosotros/$', 'main.views.nosotros'),
    url(r'^preguntas-frecuentes/$', 'main.views.preguntas_frecuentes'),
    url(r'^libro-reclamaciones/$', 'main.views.libro_reclamaciones'),
    #url(r'^facebook_debug/', 'facebook-login.html', {'template':'facebook_debug.html'}), 
)