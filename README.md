# AquaLanchas
Projeto Orientação Java(web)
AquaLanchas um sistema web com a finalidade de gerenciar e organizar reservas de lanchas.

Com foco em facilitar a comunicação entre o cliente e o responsável pela administração do processo de reservas;

Conta com automatização do processo de reservas;

Organização ao cadastro do cliente e embarcação;

Controle e disponibilidade de lanchas;

Impedir conflitos de agendamento;

Gera relatórios para controle de gestão;

Melhorar eficácia operacional do negócio;

•	Administrador (ADMIN – parte administrativa):

o	Controle total do sistema  o Gerenciamento de usuários  o Acesso a relatórios 

•	Funcionário: ( Parte em que será distribuídos os acessos necessários); 

o	Cadastro de clientes;  
o	Realização de reservas;  
o	Consulta de disponibilidade; 

REQUISITOS DO SISTEMA 
  
 Requisitos Funcionais: 
O sistema AquaLanchas deve permitir: 

•	RF01 – Realizar login no sistema  
•	RF02 – Cadastrar clientes  
•	RF03 – Editar e excluir clientes  
•	RF04 – Cadastrar lanchas  
•	RF05 – Editar e excluir lanchas  
•	RF06 – Registrar reservas de lanchas 
•	RF07 – Cancelar reservas  
•	RF08 – Consultar disponibilidade de lanchas por data  
•	RF09 – Exibir calendário de reservas 
•	RF10 – Gerar relatórios por período  
•	RF11 – Gerar relatórios por cliente  
•	RF12 – Gerenciar usuários do sistema (ADMIN)  
•	RF13 – Controlar acesso por tipo de usuário (ADMIN e FUNCIONÁRIO)  
 
 Requisitos Não Funcionais: 
 
•	RNF01 – O sistema deve ser acessado via navegador (web)  
•	RNF02 – O sistema deve possuir autenticação de usuários (JWT)  -

TALVÉZ TERÁ:

•	RNF03 – O sistema deve responder rapidamente às ações do usuário  
•	RNF04 – O sistema deve garantir integridade dos dados  
•	RNF05 – O sistema deve possuir interface amigável e intuitiva 

•	RNF06 – O sistema deve restringir acessos conforme o perfil do usuário 
 
️ ARQUITETURA DO SISTEMA 
O sistema AquaLanchas segue uma arquitetura baseada em separação de camadas:

🔹 Front-end 
•	Desenvolvido em HTML, CSS e JavaScript;  
•	Responsável pela interface do usuário; 

🔹 Back-end  
•	Framework: Django + Django REST Framework;  
•	Responsável pelas regras de negócio e APIs;  

🔹 Banco de Dados
•	Armazenamento de clientes, lanchas, reservas e usuários  (Mysql);

🔹 Comunicação 
•	API REST com autenticação via JWT; 
 
 
 
Padrões do projeto: 

•	MVC (Model-View-Controller)  
•	CRUD (Create, Read, Update, Delete)  
•	Separação de responsabilidades 

  Diagrama de Classe (Descrição) 
  
Classe Cliente;

•	id  

•	nome 

•	cpf 

•	email  

•	telefone 

•	endereço 

Classe Lancha;

•	id  

•	nome  

•	capacidade  

•	valor  

•	descrição  

•	status 

Classe Reserva; 

•	id  

•	data  

•	local 

•	valor  

•	horario 

•	cliente_id 

• lancha_id  

Classe Usuário; 

•	id  

•	matricula 

•	email  

•	senha  
 
O relacionamento que iremos usar como modelo, será o seguinte: 

•	Cliente → faz → Reserva;  
•	Lancha → possui → Reserva;  
•	Reserva → pertence a Cliente e Lancha;  
•	Usuário → gerencia sistema;

Diagrama de Domínio 
•	Cliente realiza reservas; 
•	Lancha é utilizada nas reservas;  
•	Usuário controla o sistema; 

