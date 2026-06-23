from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Usuario, Lancha, Reserva, EventoCalendario
from .forms import (RegistroClienteForm, LanchaForm, ReservaForm,
                    ReservaClienteForm, EventoForm, CadastroFuncionarioForm, CadastroClienteForm)


def index(request):
    if request.user.is_authenticated:
        if request.user.tipo == 'admin':
            return redirect('admin_dashboard')
        elif request.user.tipo == 'funcionario':
            return redirect('func_dashboard')
        else:
            return redirect('cliente_dashboard')
    return render(request, 'core/index.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuario ou senha incorretos.')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def registro_cliente(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.first_name}! Cadastro realizado com sucesso.')
            return redirect('cliente_dashboard')
    else:
        form = RegistroClienteForm()
    return render(request, 'core/registro.html', {'form': form})


# ============ ADMIN ============
@login_required
def admin_dashboard(request):
    if request.user.tipo != 'admin':
        return redirect('index')
    ctx = {
        'total_lanchas': Lancha.objects.count(),
        'lanchas_ativas': Lancha.objects.filter(ativa=True).count(),
        'total_clientes': Usuario.objects.filter(tipo='cliente').count(),
        'total_reservas': Reserva.objects.count(),
        'reservas_recentes': Reserva.objects.select_related('cliente', 'lancha').order_by('-criado_em')[:5],
    }
    return render(request, 'core/admin/dashboard.html', ctx)


@login_required
def admin_lanchas(request):
    if request.user.tipo != 'admin':
        return redirect('index')
    lanchas = Lancha.objects.all().order_by('-criado_em')
    return render(request, 'core/admin/lanchas.html', {'lanchas': lanchas})


@login_required
def admin_lancha_criar(request):
    if request.user.tipo != 'admin':
        return redirect('index')
    if request.method == 'POST':
        form = LanchaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lancha cadastrada com sucesso!')
            return redirect('admin_lanchas')
    else:
        form = LanchaForm()
    return render(request, 'core/admin/lancha_form.html', {'form': form, 'titulo': 'Nova Lancha'})


@login_required
def admin_lancha_editar(request, pk):
    if request.user.tipo != 'admin':
        return redirect('index')
    lancha = get_object_or_404(Lancha, pk=pk)
    if request.method == 'POST':
        form = LanchaForm(request.POST, instance=lancha)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lancha atualizada!')
            return redirect('admin_lanchas')
    else:
        form = LanchaForm(instance=lancha)
    return render(request, 'core/admin/lancha_form.html', {'form': form, 'titulo': 'Editar Lancha', 'lancha': lancha})


@login_required
def admin_lancha_excluir(request, pk):
    if request.user.tipo != 'admin':
        return redirect('index')
    lancha = get_object_or_404(Lancha, pk=pk)
    if request.method == 'POST':
        lancha.delete()
        messages.success(request, 'Lancha excluida!')
        return redirect('admin_lanchas')
    return render(request, 'core/admin/confirmar_exclusao.html', {'objeto': lancha, 'tipo': 'lancha'})


@login_required
def admin_toggle_lancha(request, pk):
    if request.user.tipo != 'admin':
        return redirect('index')
    lancha = get_object_or_404(Lancha, pk=pk)
    lancha.ativa = not lancha.ativa
    lancha.save()
    status = 'ativada' if lancha.ativa else 'desativada'
    messages.success(request, f'Lancha {status} com sucesso!')
    return redirect('admin_lanchas')


@login_required
def admin_clientes(request):
    if request.user.tipo != 'admin':
        return redirect('index')
    clientes = Usuario.objects.filter(tipo='cliente').order_by('first_name')
    return render(request, 'core/admin/clientes.html', {'clientes': clientes})


@login_required
def admin_funcionarios(request):
    if request.user.tipo != 'admin':
        return redirect('index')
    funcionarios = Usuario.objects.filter(tipo='funcionario').order_by('first_name')
    if request.method == 'POST':
        form = CadastroFuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionario cadastrado!')
            return redirect('admin_funcionarios')
    else:
        form = CadastroFuncionarioForm()
    return render(request, 'core/admin/funcionarios.html', {'funcionarios': funcionarios, 'form': form})


@login_required
def admin_reservas(request):
    if request.user.tipo != 'admin':
        return redirect('index')
    reservas = Reserva.objects.select_related('cliente', 'lancha', 'criado_por').order_by('-criado_em')
    return render(request, 'core/admin/reservas.html', {'reservas': reservas})


@login_required
def admin_reserva_cancelar(request, pk):
    if request.user.tipo != 'admin':
        return redirect('index')
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.status = 'cancelada'
    reserva.save()
    messages.success(request, 'Reserva cancelada.')
    return redirect('admin_reservas')


# ============ FUNCIONARIO ============
@login_required
def func_dashboard(request):
    if request.user.tipo not in ('admin', 'funcionario'):
        return redirect('index')
    lanchas_ativas = Lancha.objects.filter(ativa=True)
    reservas_hoje = Reserva.objects.filter(
        data_inicio__date=timezone.now().date(),
        status='confirmada'
    ).select_related('cliente', 'lancha')
    return render(request, 'core/func/dashboard.html', {
        'lanchas_ativas': lanchas_ativas,
        'reservas_hoje': reservas_hoje,
    })


@login_required
def func_lanchas(request):
    if request.user.tipo not in ('admin', 'funcionario'):
        return redirect('index')
    lanchas = Lancha.objects.all()
    return render(request, 'core/func/lanchas.html', {'lanchas': lanchas})


@login_required
def func_reservar(request):
    if request.user.tipo not in ('admin', 'funcionario'):
        return redirect('index')
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.criado_por = request.user
            reserva.save()
            messages.success(request, f'Reserva #{reserva.id} criada com sucesso!')
            return redirect('func_reservas')
    else:
        form = ReservaForm()
    return render(request, 'core/func/reserva_form.html', {'form': form})


@login_required
def func_reservas(request):
    if request.user.tipo not in ('admin', 'funcionario'):
        return redirect('index')
    reservas = Reserva.objects.select_related('cliente', 'lancha').order_by('-criado_em')
    return render(request, 'core/func/reservas.html', {'reservas': reservas})


@login_required
def func_cadastrar_cliente(request):
    if request.user.tipo not in ('admin', 'funcionario'):
        return redirect('index')
    if request.method == 'POST':
        form = CadastroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('func_dashboard')
    else:
        form = CadastroClienteForm()
    return render(request, 'core/func/cadastrar_cliente.html', {'form': form})


# ============ CLIENTE ============
@login_required
def cliente_dashboard(request):
    if request.user.tipo != 'cliente':
        return redirect('index')
    minhas_reservas = Reserva.objects.filter(cliente=request.user).order_by('-criado_em')[:5]
    proximos_eventos = EventoCalendario.objects.filter(
        usuario=request.user, data__gte=timezone.now().date()
    )[:3]
    return render(request, 'core/cliente/dashboard.html', {
        'minhas_reservas': minhas_reservas,
        'proximos_eventos': proximos_eventos,
    })


@login_required
def cliente_lanchas(request):
    if request.user.tipo != 'cliente':
        return redirect('index')
    lanchas = Lancha.objects.filter(ativa=True)
    return render(request, 'core/cliente/lanchas.html', {'lanchas': lanchas})


@login_required
def cliente_reservar(request):
    if request.user.tipo != 'cliente':
        return redirect('index')
    if request.method == 'POST':
        form = ReservaClienteForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = request.user
            reserva.criado_por = request.user
            reserva.save()
            messages.success(request, f'Reserva #{reserva.id} feita com sucesso!')
            return redirect('cliente_minhas_reservas')
    else:
        form = ReservaClienteForm()
    return render(request, 'core/cliente/reservar.html', {'form': form})


@login_required
def cliente_minhas_reservas(request):
    if request.user.tipo != 'cliente':
        return redirect('index')
    reservas = Reserva.objects.filter(cliente=request.user).order_by('-criado_em')
    return render(request, 'core/cliente/minhas_reservas.html', {'reservas': reservas})


@login_required
def cliente_calendario(request):
    if request.user.tipo != 'cliente':
        return redirect('index')
    eventos = EventoCalendario.objects.filter(usuario=request.user)
    eventos_json = []
    for e in eventos:
        color = '#0ea5e9'
        if e.reserva:
            color = '#10b981'
        eventos_json.append({
            'id': e.id,
            'title': e.titulo,
            'start': e.data.isoformat(),
            'color': color,
            'extendedProps': {
                'descricao': e.descricao,
                'reserva': str(e.reserva) if e.reserva else None,
            }
        })
    if request.method == 'POST':
        form = EventoForm(request.user, request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.usuario = request.user
            evento.save()
            messages.success(request, 'Evento adicionado ao calendario!')
            return redirect('cliente_calendario')
    else:
        form = EventoForm(request.user)
    return render(request, 'core/cliente/calendario.html', {
        'form': form,
        'eventos_json': eventos_json,
        'eventos': eventos,
    })


@login_required
def cliente_evento_excluir(request, pk):
    if request.user.tipo != 'cliente':
        return redirect('index')
    evento = get_object_or_404(EventoCalendario, pk=pk, usuario=request.user)
    evento.delete()
    messages.success(request, 'Evento removido.')
    return redirect('cliente_calendario')


@login_required
def cliente_cancelar_reserva(request, pk):
    if request.user.tipo != 'cliente':
        return redirect('index')
    reserva = get_object_or_404(Reserva, pk=pk, cliente=request.user)
    if reserva.status == 'confirmada':
        reserva.status = 'cancelada'
        reserva.save()
        messages.success(request, 'Reserva cancelada com sucesso.')
    return redirect('cliente_minhas_reservas')
