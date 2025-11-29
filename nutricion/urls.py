from django.urls import path
from . import views
urlpatterns = [
    # path('',views.index, name='index'),
    path('', views.index, name='index'),
    path('create_alimento/', views.crear_alimento, name='create_alimento'),
    path('lista_alimentos/', views.lista_alimentos, name='lista_alimentos'),
    path('editar_alimento/<int:alimento_id>/', views.editar_alimento, name='editar_alimento'),
    path('eliminar_alimento/<int:alimento_id>/', views.eliminar_alimento, name='eliminar_alimento'),
    path('ver_alimento/<int:alimento_id>/', views.alimento_detail, name='ver_alimento'),
    ## crud dieta
    path('lista_dietas/', views.lista_dietas, name='lista_dietas'),
    path('create_dieta/', views.crear_dieta, name='create_dieta'),
    path('alimentos_dieta/', views.alimentos_dieta, name='alimentos_dieta'),
    path('vaciar_alimento_dieta/', views.vaciar_alimento_dieta, name='vaciar_alimento_dieta'),
    path('borrar_alimento_dieta/<int:alimento_id>/', views.borrar_alimento_dieta, name='borrar_alimento_dieta'),
    path('validar_alimentos/',views.validar_alimentos, name='validar_alimentos'),
    path('ver_dieta/<int:dieta_id>/', views.ver_dieta, name='ver_dieta'),
    path('editar_dieta/<int:dieta_id>/', views.editar_dieta, name='editar_dieta'),
    path('eliminar_dieta/<int:dieta_id>/', views.eliminar_dieta, name='eliminar_dieta'),
    # primera consulta
    path('primera_consulta/', views.primera_consulta, name='primera_consulta'),
    path('crear_paciente/', views.crear_paciente, name='crear_paciente'),
    path('agregar_sintoma_motivo_consulta/', views.agregar_sintoma_motivo_consulta, name='agregar_sintoma_motivo_consulta'),
    path('vaciar_sintomas_seleccionados/', views.vaciar_sintomas_seleccionados, name='vaciar_sintomas_seleccionados'),
    path('motivo_consulta/', views.motivo_consulta, name='motivo_consulta'),
    path('alimentos_habitos/', views.alimentos_habitos, name='alimentos_habitos'),
    path('agregar_alimento/', views.agregar_alimento, name='agregar_alimento'),
    path('vaciar_lista_alimentos_seleccionados/', views.vaciar_lista_alimentos_seleccionados, name='vaciar_lista_alimentos_seleccionados'),
    path('crear_atropometria/', views.crear_atropometria, name='crear_atropometria'),
    path('informacion_general/', views.informacion_general, name='informacion_general'),
]
