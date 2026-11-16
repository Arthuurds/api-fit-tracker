# Fit Tracker API

API para acompanhamento de treinos e progressão de carga, feita em **Python com FastAPI**.

O usuário se cadastra, faz login e recebe um **token JWT**. A API guarda os exercícios e cada execução registrada (carga e repetições), formando o histórico de treinos de cada usuário.

## Funcionalidades

- **Cadastro de usuários** com senha armazenada como hash (bcrypt)
- **Login** com retorno de token JWT (validade de 30 minutos)
- **Rota protegida** `/usuarios/me`, que retorna os dados do usuário logado
- **Cadastro e listagem de exercícios** (nome e grupo muscular)
- **Registro de execuções**: carga em kg, número de repetições e data
- **Histórico de treinos** por usuário
- **Documentação automática** com Swagger UI, gerada pelo FastAPI

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3 |
| Framework | FastAPI + Uvicorn |
| Banco de dados | SQLite + SQLAlchemy (ORM) |
| Validação | Pydantic |
| Segurança | python-jose (JWT) e passlib/bcrypt (hash de senha) |

## Estrutura do projeto

```
app/
├── main.py       # Criação da aplicação e rotas
├── models.py     # Tabelas: Usuario, Exercicio, RegistroExecucao
├── schemas.py    # Modelos Pydantic de entrada e saída
├── database.py   # Conexão com o SQLite e sessão do banco
└── auth.py       # Hash de senha, geração e validação do JWT
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
| GET | `/usuarios/me` | Dados do usuário logado (exige token) |
| POST | `/exercicios/` | Cadastra um exercício |
| GET | `/exercicios/` | Lista os exercícios |
| POST | `/registros` | Registra a execução de um exercício |
| GET | `/registros/usuarios/{usuario_id}` | Histórico de treinos de um usuário |

## Exemplo de uso

```bash
# Cadastrar usuário
curl -X POST http://127.0.0.1:8000/usuarios/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "Arthur", "email": "arthur@email.com", "senha": "123456"}'

# Registrar um treino
curl -X POST http://127.0.0.1:8000/registros \
  -H "Content-Type: application/json" \
  -d '{"usuario_id": 1, "exercicio_id": 1, "carga_kg": 60, "repeticoes": 10}'
```

## Próximos passos

- Proteger as rotas de exercícios e registros com o token JWT
- Usar o usuário do token no registro de treino, em vez de enviar `usuario_id`
- Adicionar testes automatizados com `pytest`

## Autor

**Arthur Dornas**: estudante de Engenharia de Software (PUC Minas) e Técnico em Desenvolvimento de Sistemas (Senac)
[GitHub](https://github.com/Arthuurds) · [LinkedIn](https://www.linkedin.com/in/arthur-dornas-8971663a8/)
