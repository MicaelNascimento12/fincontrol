# FinControl

Sistema de Gestão Financeira Pessoal com Dashboard Analítico, desenvolvido com Python, FastAPI, MySQL e JavaScript.

---

## Sobre o Projeto

O FinControl é uma aplicação Full Stack para gerenciamento financeiro pessoal, permitindo o controle de receitas, despesas, categorias e indicadores financeiros através de uma interface web moderna integrada a uma API REST.

O projeto foi desenvolvido utilizando conceitos de Engenharia de Software, modelagem de banco de dados relacional, arquitetura em camadas e autenticação baseada em JWT.

---

## Funcionalidades

### Autenticação

* Cadastro de usuários
* Login com JWT
* Controle de sessão
* Proteção de rotas

### Categorias

* Criação de categorias personalizadas
* Edição de categorias
* Exclusão de categorias
* Categorias padrão automáticas

### Transações

* Cadastro de receitas
* Cadastro de despesas
* Atualização de transações
* Exclusão de transações
* Filtros por categoria e tipo

### Dashboard

* Saldo atual
* Total de receitas
* Total de despesas
* Gastos por categoria
* Fluxo financeiro mensal

### Relatórios

* Filtro por período
* Filtro por categoria
* Filtro por tipo
* Resumo financeiro consolidado

### Perfil

* Atualização de informações do usuário
* Alteração de senha
* Gerenciamento seguro da conta

---

## Tecnologias Utilizadas

### Back-End

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* JWT Authentication
* Bcrypt

### Banco de Dados

* MySQL
* Modelagem Relacional
* Constraints
* Relacionamentos
* Índices

### Front-End

* HTML5
* CSS3
* JavaScript (ES6+)
* Chart.js
* Lucide Icons

### Ferramentas

* Git
* GitHub
* VS Code
* Postman

---

## Principais Competências Demonstradas

* Modelagem de Banco de Dados Relacional
* Desenvolvimento de APIs REST
* Arquitetura em Camadas
* Repository Pattern
* Service Layer Pattern
* Autenticação e Autorização com JWT
* Integração Front-End e Back-End
* Consultas e Manipulação de Dados
* Visualização de Dados
* Controle de Versão com Git

---

## Arquitetura

O projeto segue uma arquitetura em camadas para separação de responsabilidades e facilidade de manutenção.

```text
Frontend
│
├── Pages
├── JavaScript
├── CSS
│
Backend
│
├── Routers
├── Services
├── Repositories
├── Schemas
├── Models
├── Core
│
Database
```

### Camadas

**Routers**

* Recebem e tratam as requisições HTTP.

**Services**

* Implementam as regras de negócio.

**Repositories**

* Realizam o acesso ao banco de dados.

**Schemas**

* Validam dados de entrada e saída.

**Models**

* Representam as entidades persistidas.

---

## Estrutura do Projeto

```text
fincontrol/

├── backend/
│   ├── routers/
│   ├── services/
│   ├── repositories/
│   ├── schemas/
│   ├── models/
│   ├── core/
│   └── main.py
│
├── frontend/
│   ├── pages/
│   ├── javascript/
│   ├── css/
│   └── assets/
│
├── database/
├── docs/
└── README.md
```

---

## Como Executar

### Clonar o repositório

```bash
git clone https://github.com/MicaelNascimento12/fincontrol.git
```

### Criar ambiente virtual

```bash
python -m venv venv
```

### Ativar ambiente virtual

Windows:

```bash
venv\Scripts\activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Configurar variáveis de ambiente

Criar um arquivo `.env`:

```env
DATABASE_URL=mysql+pymysql://usuario:senha@localhost/fincontrol

SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
```

### Executar a API

```bash
uvicorn main:app --reload
```

### Executar o Front-End

Abrir a pasta `frontend` utilizando a extensão Live Server do VS Code.

---

## Capturas de Tela

### Dashboard

<img width="1510" height="881" alt="image" src="https://github.com/user-attachments/assets/174ff21b-3adc-4dcf-868b-f36dbbead00b" />


### Transações

<img width="1500" height="883" alt="image" src="https://github.com/user-attachments/assets/9834fd56-d271-450b-9f35-d318051316b0" />


### Categorias

<img width="1516" height="881" alt="image" src="https://github.com/user-attachments/assets/29d88450-e193-42d6-b474-9a12b5891b43" />


### Relatórios

<img width="1496" height="884" alt="image" src="https://github.com/user-attachments/assets/8c16653c-c8e5-4438-bc19-b0444c60a990" />


### Perfil

<img width="1514" height="882" alt="image" src="https://github.com/user-attachments/assets/4a351cc3-8f79-4f87-ad2e-f7c1cbcd9960" />


---

## Autor

Micael Nascimento Sousa

LinkedIn:
[www.linkedin.com/in/micael-nascimento-sousa](http://www.linkedin.com/in/micael-nascimento-sousa)
