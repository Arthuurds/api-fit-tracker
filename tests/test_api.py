from tests.conftest import criar_usuario_e_logar


def criar_exercicio(client, headers, nome="Supino reto", grupo="Peito"):
    resposta = client.post("/exercicios/", json={"nome": nome, "grupo_muscular": grupo}, headers=headers)
    assert resposta.status_code == 201
    return resposta.json()["id"]


# ---------- Usuários e login ----------

def test_cadastrar_usuario(client):
    resposta = client.post("/usuarios/", json={"nome": "Arthur", "email": "a@email.com", "senha": "senha123"})
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["email"] == "a@email.com"
    assert "senha" not in corpo and "senha_hash" not in corpo


def test_nao_permite_email_duplicado(client):
    dados = {"nome": "Arthur", "email": "a@email.com", "senha": "senha123"}
    client.post("/usuarios/", json=dados)
    assert client.post("/usuarios/", json=dados).status_code == 400


def test_recusa_senha_curta(client):
    resposta = client.post("/usuarios/", json={"nome": "Arthur", "email": "a@email.com", "senha": "123"})
    assert resposta.status_code == 422


def test_login_com_senha_errada(client):
    client.post("/usuarios/", json={"nome": "Arthur", "email": "a@email.com", "senha": "senha123"})
    resposta = client.post("/login/", data={"username": "a@email.com", "password": "errada"})
    assert resposta.status_code == 401


def test_usuarios_me_retorna_usuario_logado(client):
    headers = criar_usuario_e_logar(client)
    resposta = client.get("/usuarios/me", headers=headers)
    assert resposta.status_code == 200
    assert resposta.json()["email"] == "arthur@email.com"


def test_token_invalido_e_recusado(client):
    resposta = client.get("/usuarios/me", headers={"Authorization": "Bearer token-falso"})
    assert resposta.status_code == 401


# ---------- Rotas protegidas ----------

def test_rotas_exigem_login(client):
    assert client.get("/exercicios/").status_code == 401
    assert client.post("/exercicios/", json={"nome": "x", "grupo_muscular": "y"}).status_code == 401
    assert client.get("/registros").status_code == 401
    assert client.post("/registros", json={"exercicio_id": 1, "carga_kg": 10, "repeticoes": 5}).status_code == 401


# ---------- Registros de treino ----------

def test_registrar_treino_usa_usuario_do_token(client):
    headers = criar_usuario_e_logar(client)
    usuario_id = client.get("/usuarios/me", headers=headers).json()["id"]
    exercicio_id = criar_exercicio(client, headers)

    resposta = client.post(
        "/registros",
        json={"exercicio_id": exercicio_id, "carga_kg": 60, "repeticoes": 10},
        headers=headers,
    )
    assert resposta.status_code == 201
    assert resposta.json()["usuario_id"] == usuario_id


def test_usuario_ve_apenas_os_proprios_registros(client):
    headers_arthur = criar_usuario_e_logar(client, "arthur@email.com")
    headers_maria = criar_usuario_e_logar(client, "maria@email.com")
    exercicio_id = criar_exercicio(client, headers_arthur)

    client.post("/registros", json={"exercicio_id": exercicio_id, "carga_kg": 60, "repeticoes": 10}, headers=headers_arthur)
    client.post("/registros", json={"exercicio_id": exercicio_id, "carga_kg": 30, "repeticoes": 12}, headers=headers_maria)

    registros_arthur = client.get("/registros", headers=headers_arthur).json()
    assert len(registros_arthur) == 1
    assert registros_arthur[0]["carga_kg"] == 60


def test_filtrar_registros_por_exercicio(client):
    headers = criar_usuario_e_logar(client)
    supino = criar_exercicio(client, headers, "Supino reto", "Peito")
    agachamento = criar_exercicio(client, headers, "Agachamento", "Pernas")
    client.post("/registros", json={"exercicio_id": supino, "carga_kg": 60, "repeticoes": 10}, headers=headers)
    client.post("/registros", json={"exercicio_id": agachamento, "carga_kg": 80, "repeticoes": 8}, headers=headers)

    resposta = client.get(f"/registros?exercicio_id={agachamento}", headers=headers)
    assert [r["exercicio_id"] for r in resposta.json()] == [agachamento]


def test_recusa_registro_de_exercicio_inexistente(client):
    headers = criar_usuario_e_logar(client)
    resposta = client.post("/registros", json={"exercicio_id": 999, "carga_kg": 60, "repeticoes": 10}, headers=headers)
    assert resposta.status_code == 404


def test_recusa_valores_invalidos(client):
    headers = criar_usuario_e_logar(client)
    exercicio_id = criar_exercicio(client, headers)
    negativos = {"exercicio_id": exercicio_id, "carga_kg": -5, "repeticoes": 10}
    zero_repeticoes = {"exercicio_id": exercicio_id, "carga_kg": 60, "repeticoes": 0}
    assert client.post("/registros", json=negativos, headers=headers).status_code == 422
    assert client.post("/registros", json=zero_repeticoes, headers=headers).status_code == 422
