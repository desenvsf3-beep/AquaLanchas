from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Lancha, Reserva, EventoCalendario


class RegistroClienteForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='Nome', required=True)
    last_name = forms.CharField(label='Sobrenome', required=True)
    telefone = forms.CharField(label='Telefone', required=True)
    cpf = forms.CharField(label='CPF', required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefone', 'cpf', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo = 'cliente'
        if commit:
            user.save()
        return user


class CadastroFuncionarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='Nome', required=True)
    last_name = forms.CharField(label='Sobrenome', required=True)
    telefone = forms.CharField(label='Telefone', required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo = 'funcionario'
        if commit:
            user.save()
        return user


class CadastroClienteForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='Nome', required=True)
    last_name = forms.CharField(label='Sobrenome', required=True)
    telefone = forms.CharField(label='Telefone', required=True)
    cpf = forms.CharField(label='CPF', required=False)
    endereco = forms.CharField(label='Endereco', required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefone', 'cpf', 'endereco', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo = 'cliente'
        if commit:
            user.save()
        return user


class LanchaForm(forms.ModelForm):
    class Meta:
        model = Lancha
        fields = ['nome', 'descricao', 'capacidade', 'preco_hora', 'ativa', 'imagem_url']
        labels = {
            'nome': 'Nome da Lancha',
            'descricao': 'Descricao',
            'capacidade': 'Capacidade (pessoas)',
            'preco_hora': 'Preco por Hora (R$)',
            'ativa': 'Lancha Ativa',
            'imagem_url': 'URL da Imagem',
        }
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'lancha', 'data_inicio', 'data_fim', 'quantidade_pessoas', 'observacoes']
        labels = {
            'cliente': 'Cliente',
            'lancha': 'Lancha',
            'data_inicio': 'Data/Hora de Inicio',
            'data_fim': 'Data/Hora de Fim',
            'quantidade_pessoas': 'Quantidade de Pessoas',
            'observacoes': 'Observacoes',
        }
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'data_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Usuario.objects.filter(tipo='cliente')
        self.fields['lancha'].queryset = Lancha.objects.filter(ativa=True)
        self.fields['data_inicio'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['data_fim'].input_formats = ['%Y-%m-%dT%H:%M']


class ReservaClienteForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['lancha', 'data_inicio', 'data_fim', 'quantidade_pessoas', 'observacoes']
        labels = {
            'lancha': 'Lancha',
            'data_inicio': 'Data/Hora de Inicio',
            'data_fim': 'Data/Hora de Fim',
            'quantidade_pessoas': 'Quantidade de Pessoas',
            'observacoes': 'Observacoes',
        }
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'data_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lancha'].queryset = Lancha.objects.filter(ativa=True)
        self.fields['data_inicio'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['data_fim'].input_formats = ['%Y-%m-%dT%H:%M']


class EventoForm(forms.ModelForm):
    class Meta:
        model = EventoCalendario
        fields = ['titulo', 'descricao', 'data', 'reserva']
        labels = {
            'titulo': 'Titulo do Evento',
            'descricao': 'Descricao',
            'data': 'Data',
            'reserva': 'Reserva Vinculada (opcional)',
        }
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reserva'].queryset = Reserva.objects.filter(cliente=user)
        self.fields['reserva'].required = False
