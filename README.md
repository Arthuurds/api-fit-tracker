# Fit Tracker API

API para acompanhamento de treinos e progressão de carga, feita em **Python com FastAPI**.

O usuário se cadastra, faz login e recebe um **token JWT**. A API guarda os exercícios e cada execução registrada (carga e repetições), formando o histórico de treinos de cada usuário.

## Funcionalidades

- **Cadastro de usuários** com senha armazenada como hash (bcrypt)
- **Login** com retorno de token JWT (validade de 30 minutos)
- **Rotas protegidas**: exercícios e registros só funcionam com o token
- **Cadastro e listagem de exercícios** (nome e grupo muscular)
- **Registro de execuções** sempre no nome do usuário logado (o ID vem do token, não do corpo da requisição)
- **Histórico de treinos** do próprio usuário, com filtro por exercício
- **Validação dos dados**: senha com no mínimo 6 caracteres, carga não negativa e repetições maiores que zero
- **Testes automatizados** com pytest
- **Documentação automática** com Swagger UI, gerada pelo FastAPI

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3 |
| Framework | FastAPI + Uvicorn |
| Banco de dados | SQLite + SQLAlchemy (ORM) |
| Validação | Pydantic |
| Segurança | python-jose (JWT) e passlib/bcrypt (hash de senha) |
| Testes | pytest + TestClient do FastAPI |

## Estrutura do projeto

```
app/
├── main.py       # Criação da aplicação e rotas
├── models.py     # Tabelas: Usuario, Exercicio, RegistroExecucao
├── schemas.py    # Modelos Pydantic de entrada e saída
├── database.py   # Conexão com o SQLite e sessão do banco
└── auth.py       # Hash de senha, geração e validação do JWT
tests/
└── test_api.py   # Testes de cadastro, login, rotas protegidas e registros
```

## Modelo de dados

```
Usuario (id, nome, email, senha_hash)
   │ 1
   │
   │ N
RegistroExecucao (id, usuario_id, exercicio_id, carga_kg, repeticoes, data)
   │ N
   │
   │ 1
Exercicio (id, nome, grupo_muscular)
```

## Como executar

**Pré-requisito:** Python 3.10 ou superior.

1. Clone o repositório e entre na pasta:
   ```bash
   git clone https://github.com/Arthuurds/api-fit-tracker.git
   cd api-fit-tracker
   ```
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   venv\Scripts\activate         # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Defina a chave secreta do JWT:
   ```bash
   export SECRET_KEY=uma_chave_longa_e_secreta       # Linux / macOS
   $env:SECRET_KEY="uma_chave_longa_e_secreta"       # Windows (PowerShell)
   ```
5. Inicie o servidor:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Acesse a documentação em **http://127.0.0.1:8000/docs**

O banco `fit_tracker.db` é criado automaticamente na primeira execução.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/usuarios/` | Cadastra um usuário |
| POST | `/login/` | Faz login (form `username` = e-mail, `password`) e retorna o token |
| GET | `/usuarios/me` | Dados do usuário logado 🔒 |
| POST | `/exercicios/` | Cadastra um exercício 🔒 |
| GET | `/exercicios/` | Lista os exercícios 🔒 |
| POST | `/registros` | Registra uma execução para o usuário logado 🔒 |
| GET | `/registros?exercicio_id=` | Histórico do usuário logado, com filtro opcional 🔒 |

🔒 = exige o cabeçalho `Authorization: Bearer <token>`. No Swagger (`/docs`), use o botão **Authorize**.

## Exemplo de uso

```bash
# Cadastrar usuário
curl -X POST http://127.0.0.1:8000/usuarios/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "Arthur", "email": "arthur@email.com", "senha": "123456"}'

# Fazer login e pegar o token
curl -X POST http://127.0.0.1:8000/login/ \
  -d "username=arthur@email.com&password=123456"

# Registrar um treino com o token recebido
curl -X POST http://127.0.0.1:8000/registros \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"exercicio_id": 1, "carga_kg": 60, "repeticoes": 10}'
```

## Testes

```bash
pip install -r requirements-dev.txt
pytest
```

## Configuração opcional

| Variável | Para que serve | Padrão |
|---|---|---|
| `SECRET_KEY` | Chave de assinatura do JWT | chave de desenvolvimento |
| `DATABASE_URL` | Endereço do banco | `sqlite:///./fit_tracker.db` |
| `CORS_ORIGINS` | Sites que podem chamar a API pelo navegador, separados por vírgula | nenhum |

## Autor

**Arthur Dornas**: estudante de Engenharia de Software (PUC Minas) e Técnico em Desenvolvimento de Sistemas (Senac)
[GitHub](https://github.com/Arthuurds) · [LinkedIn](https://www.linkedin.com/in/arthur-dornas-8971663a8/)
