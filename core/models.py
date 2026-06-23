from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    TIPOS = [
        ('admin', 'Administrador'),
        ('funcionario', 'Funcionario'),
        ('cliente', 'Cliente'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPOS, default='cliente')
    telefone = models.CharField(max_length=20, blank=True)
    cpf = models.CharField(max_length=14, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_tipo_display()})"

    @property
    def is_admin_sistema(self):
        return self.tipo == 'admin'

    @property
    def is_funcionario(self):
        return self.tipo == 'funcionario'

    @property
    def is_cliente(self):
        return self.tipo == 'cliente'


class Lancha(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    capacidade = models.IntegerField()
    preco_hora = models.DecimalField(max_digits=10, decimal_places=2)
    ativa = models.BooleanField(default=True)
    imagem_url = models.URLField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Reserva(models.Model):
    STATUS = [
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('concluida', 'Concluida'),
    ]
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas')
    lancha = models.ForeignKey(Lancha, on_delete=models.CASCADE, related_name='reservas')
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    quantidade_pessoas = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default='confirmada')
    observacoes = models.TextField(blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    criado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservas_criadas')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva #{self.id} - {self.cliente.get_full_name() or self.cliente.username} - {self.lancha.nome}"

    def save(self, *args, **kwargs):
        if self.data_inicio and self.data_fim and self.lancha_id:
            horas = (self.data_fim - self.data_inicio).total_seconds() / 3600
            self.valor_total = round(horas * float(self.lancha.preco_hora), 2)
        super().save(*args, **kwargs)

    @property
    def duracao_horas(self):
        if self.data_inicio and self.data_fim:
            return round((self.data_fim - self.data_inicio).total_seconds() / 3600, 1)
        return 0


class EventoCalendario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data = models.DateField()
    reserva = models.ForeignKey(Reserva, on_delete=models.SET_NULL, null=True, blank=True, related_name='eventos')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.data}"

    class Meta:
        ordering = ['data']
