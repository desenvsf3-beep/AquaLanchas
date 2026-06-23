from django.contrib import admin
from django.urls import path
from core import views, api

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_cliente, name='registro'),

    # API
    path('api/lanchas/', api.lancha_list, name='api_lanchas'),
    path('api/lanchas/<int:pk>/', api.lancha_detail, name='api_lancha_detail'),
    path('api/reservas/', api.reserva_list, name='api_reservas'),
    path('api/disponibilidade/', api.disponibilidade, name='api_disponibilidade'),
    path('api/clientes/', api.cliente_list, name='api_clientes'),

    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/lanchas/', views.admin_lanchas, name='admin_lanchas'),
    path('admin/lanchas/criar/', views.admin_lancha_criar, name='admin_lancha_criar'),
    path('admin/lanchas/<int:pk>/editar/', views.admin_lancha_editar, name='admin_lancha_editar'),
    path('admin/lanchas/<int:pk>/excluir/', views.admin_lancha_excluir, name='admin_lancha_excluir'),
    path('admin/lanchas/<int:pk>/toggle/', views.admin_toggle_lancha, name='admin_toggle_lancha'),
    path('admin/clientes/', views.admin_clientes, name='admin_clientes'),
    path('admin/funcionarios/', views.admin_funcionarios, name='admin_funcionarios'),
    path('admin/reservas/', views.admin_reservas, name='admin_reservas'),
    path('admin/reservas/<int:pk>/cancelar/', views.admin_reserva_cancelar, name='admin_reserva_cancelar'),

    # Funcionario
    path('func/dashboard/', views.func_dashboard, name='func_dashboard'),
    path('func/lanchas/', views.func_lanchas, name='func_lanchas'),
    path('func/reservar/', views.func_reservar, name='func_reservar'),
    path('func/reservas/', views.func_reservas, name='func_reservas'),
    path('func/clientes/cadastrar/', views.func_cadastrar_cliente, name='func_cadastrar_cliente'),

    # Cliente
    path('cliente/dashboard/', views.cliente_dashboard, name='cliente_dashboard'),
    path('cliente/lanchas/', views.cliente_lanchas, name='cliente_lanchas'),
    path('cliente/reservar/', views.cliente_reservar, name='cliente_reservar'),
    path('cliente/minhas-reservas/', views.cliente_minhas_reservas, name='cliente_minhas_reservas'),
    path('cliente/calendario/', views.cliente_calendario, name='cliente_calendario'),
    path('cliente/evento/<int:pk>/excluir/', views.cliente_evento_excluir, name='cliente_evento_excluir'),
    path('cliente/reserva/<int:pk>/cancelar/', views.cliente_cancelar_reserva, name='cliente_cancelar_reserva'),
]
