import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Lancha, Reserva, Usuario, EventoCalendario
from django.utils import timezone
from datetime import datetime


def lancha_list(request):
    """GET /api/lanchas/ - Lista todas as lanchas"""
    lanchas = Lancha.objects.all()
    ativa = request.GET.get('ativa')
    if ativa is not None:
        lanchas = lanchas.filter(ativa=(ativa == 'true'))
    data = [{
        'id': l.id,
        'nome': l.nome,
        'descricao': l.descricao,
        'capacidade': l.capacidade,
        'preco_hora': float(l.preco_hora),
        'ativa': l.ativa,
        'imagem_url': l.imagem_url,
    } for l in lanchas]
    return JsonResponse({'lanchas': data})


@login_required
def lancha_detail(request, pk):
    """GET /api/lanchas/<id>/ - Detalhe de uma lancha"""
    try:
        l = Lancha.objects.get(pk=pk)
    except Lancha.DoesNotExist:
        return JsonResponse({'erro': 'Lancha nao encontrada'}, status=404)
    return JsonResponse({
        'id': l.id,
        'nome': l.nome,
        'descricao': l.descricao,
        'capacidade': l.capacidade,
        'preco_hora': float(l.preco_hora),
        'ativa': l.ativa,
        'imagem_url': l.imagem_url,
        'criado_em': l.criado_em.isoformat(),
    })


@login_required
def reserva_list(request):
    """GET /api/reservas/ - Lista reservas (admin/func veem todas, cliente vê só as suas)"""
    if request.user.tipo in ('admin', 'funcionario'):
        reservas = Reserva.objects.select_related('cliente', 'lancha').all().order_by('-criado_em')
    else:
        reservas = Reserva.objects.select_related('cliente', 'lancha').filter(cliente=request.user).order_by('-criado_em')
    data = [{
        'id': r.id,
        'cliente': r.cliente.get_full_name() or r.cliente.username,
        'lancha': r.lancha.nome,
        'data_inicio': r.data_inicio.isoformat(),
        'data_fim': r.data_fim.isoformat(),
        'quantidade_pessoas': r.quantidade_pessoas,
        'status': r.status,
        'valor_total': float(r.valor_total),
    } for r in reservas]
    return JsonResponse({'reservas': data})


@login_required
def disponibilidade(request):
    """GET /api/disponibilidade/?data_inicio=&data_fim= - Verifica disponibilidade"""
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    if not data_inicio or not data_fim:
        return JsonResponse({'erro': 'Informe data_inicio e data_fim'}, status=400)
    try:
        dt_inicio = datetime.fromisoformat(data_inicio)
        dt_fim = datetime.fromisoformat(data_fim)
    except ValueError:
        return JsonResponse({'erro': 'Formato de data invalido. Use ISO 8601.'}, status=400)

    lanchas = Lancha.objects.filter(ativa=True)
    resultado = []
    for lancha in lanchas:
        conflitos = Reserva.objects.filter(
            lancha=lancha,
            status__in=['confirmada', 'pendente'],
            data_inicio__lt=dt_fim,
            data_fim__gt=dt_inicio
        ).exists()
        resultado.append({
            'id': lancha.id,
            'nome': lancha.nome,
            'capacidade': lancha.capacidade,
            'preco_hora': float(lancha.preco_hora),
            'disponivel': not conflitos,
        })
    return JsonResponse({'lanchas': resultado, 'periodo': {'inicio': data_inicio, 'fim': data_fim}})


@login_required
def cliente_list(request):
    """GET /api/clientes/ - Lista clientes (admin/func apenas)"""
    if request.user.tipo not in ('admin', 'funcionario'):
        return JsonResponse({'erro': 'Acesso negado'}, status=403)
    clientes = Usuario.objects.filter(tipo='cliente').order_by('first_name')
    data = [{
        'id': c.id,
        'nome': c.get_full_name() or c.username,
        'email': c.email,
        'telefone': c.telefone,
        'cpf': c.cpf,
        'criado_em': c.criado_em.isoformat(),
    } for c in clientes]
    return JsonResponse({'clientes': data})
