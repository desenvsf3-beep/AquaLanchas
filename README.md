# Aqua Lancha - Sistema de Reservas de Lanchas

## Como Rodar

### 1. Criar e ativar o ambiente virtual

**Linux / macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Iniciar o banco e dados de exemplo

```bash
python manage.py migrate
python seed.py
```

### 4. Rodar o servidor

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

---

## Logins

| Perfil      | Usuario    | Senha     |
|-------------|------------|-----------|
| Admin       | Admaqua    | 123@aqua  |
| Funcionario | func1      | func123   |
| Cliente     | cliente1   | cli123    |

---

## Estrutura

```
aqua_lancha/       -> Configuracoes do projeto (settings.py, urls.py)
core/
  models.py        -> Usuario, Lancha, Reserva, EventoCalendario
  views.py         -> Views por perfil (admin, func, cliente)
  forms.py         -> Formularios
  api.py           -> API REST JSON (/api/...)
  admin.py         -> Painel admin Django
  templates/core/
    admin/         -> Dashboard, lanchas, clientes, funcionarios, reservas
    func/          -> Dashboard, lanchas, reservas, cadastro cliente
    cliente/       -> Dashboard, lanchas, reservar, calendario
venv/              -> Ambiente virtual Python (nao commitar no git)
db.sqlite3         -> Banco de dados SQLite
requirements.txt   -> Dependencias do projeto
seed.py            -> Script de dados iniciais
```

## API REST

| Endpoint                  | Acesso      | Descricao                |
|---------------------------|-------------|--------------------------|
| GET /api/lanchas/         | Publico     | Lista lanchas            |
| GET /api/lanchas/<id>/    | Autenticado | Detalhe da lancha        |
| GET /api/reservas/        | Autenticado | Lista reservas           |
| GET /api/disponibilidade/ | Autenticado | Verifica disponibilidade |
| GET /api/clientes/        | Admin/Func  | Lista clientes           |

Exemplo:
GET /api/disponibilidade/?data_inicio=2025-12-01T10:00&data_fim=2025-12-01T14:00

## .gitignore recomendado

```
venv/
db.sqlite3
__pycache__/
*.pyc
.env
```
