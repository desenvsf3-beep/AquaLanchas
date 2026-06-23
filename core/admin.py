from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Lancha, Reserva, EventoCalendario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'tipo']
    list_filter = ['tipo']
    fieldsets = UserAdmin.fieldsets + (('Extra', {'fields': ('tipo', 'telefone', 'cpf')}),)

@admin.register(Lancha)
class LanchaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'capacidade', 'preco_hora', 'ativa']
    list_filter = ['ativa']

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'lancha', 'data_inicio', 'data_fim', 'status', 'valor_total']
    list_filter = ['status', 'lancha']

@admin.register(EventoCalendario)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'data']
