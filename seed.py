import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqua_lancha.settings')
django.setup()

from core.models import Usuario, Lancha, Reserva
from django.utils import timezone
from datetime import timedelta
import decimal

# Admin
if not Usuario.objects.filter(username='Admaqua').exists():
    admin = Usuario.objects.create_user(
        username='Admaqua',
        email='Admaqua@gmail.com',
        password='123@aqua',
        first_name='Admin',
        last_name='Aqua Lancha',
        tipo='admin'
    )
    print('Admin criado!')

# Funcionario demo
if not Usuario.objects.filter(username='func1').exists():
    func = Usuario.objects.create_user(
        username='func1',
        email='func1@aqua_lancha.com',
        password='func123',
        first_name='Carlos',
        last_name='Silva',
        tipo='funcionario',
        telefone='(11) 99999-0001'
    )
    print('Funcionario criado: func1 / func123')

# Cliente demo
if not Usuario.objects.filter(username='cliente1').exists():
    cli = Usuario.objects.create_user(
        username='cliente1',
        email='maria@email.com',
        password='cli123',
        first_name='Maria',
        last_name='Santos',
        tipo='cliente',
        telefone='(11) 99999-0002',
        cpf='123.456.789-00'
    )
    print('Cliente criado: cliente1 / cli123')
else:
    cli = Usuario.objects.get(username='cliente1')

# Lanchas
lanchas_data = [
    ('Sea Ray 260', 'Lancha esportiva com motor de alta performance, ideal para passeios rapidos.', 8, 350.00, 'https://images.unsplash.com/photo-1567899378494-47b22a2ae96a?w=600'),
    ('Phantom 320', 'Lancha luxuosa com cabine completa e area de descanso. Perfeita para viagens longas.', 12, 520.00, 'https://images.unsplash.com/photo-1605281317010-fe5ffe798166?w=600'),
    ('Express Cruiser', 'Ideal para familias. Espaco amplo, suave e confortavel.', 10, 420.00, 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=600'),
    ('Azimut 45', 'Iate de luxo com deck amplo, churrasqueira e sistema de som premium.', 20, 800.00, 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600'),
]

for nome, desc, cap, preco, img in lanchas_data:
    if not Lancha.objects.filter(nome=nome).exists():
        Lancha.objects.create(nome=nome, descricao=desc, capacidade=cap, preco_hora=decimal.Decimal(str(preco)), imagem_url=img)
        print(f'Lancha criada: {nome}')

# Reservas demo
if Reserva.objects.count() == 0 and Usuario.objects.filter(username='cliente1').exists():
    lanchas = list(Lancha.objects.all()[:2])
    cli = Usuario.objects.get(username='cliente1')
    admin = Usuario.objects.get(username='Admaqua')
    now = timezone.now().replace(minute=0, second=0, microsecond=0)
    Reserva.objects.create(
        cliente=cli, lancha=lanchas[0],
        data_inicio=now + timedelta(days=2),
        data_fim=now + timedelta(days=2, hours=4),
        quantidade_pessoas=6, status='confirmada', criado_por=cli
    )
    Reserva.objects.create(
        cliente=cli, lancha=lanchas[1],
        data_inicio=now + timedelta(days=5),
        data_fim=now + timedelta(days=5, hours=6),
        quantidade_pessoas=10, status='confirmada', criado_por=cli
    )
    print('Reservas demo criadas!')

print('\n=== SEED CONCLUIDO ===')
print('Admin:      Admaqua / 123@aqua')
print('Funcionario: func1 / func123')
print('Cliente:     cliente1 / cli123')
