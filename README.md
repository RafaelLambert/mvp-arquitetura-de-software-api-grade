
# 🧾API Grade - MVP Back-end - PUC-Rio

Este repositório contém o microsserviço de **gestão de notas** do projeto MVP proposto pela PUC-Rio. O serviço foi desenvolvido em Python utilizando o framework Flask, com SQLAlchemy para a modelagem do banco de dados e Pydantic para validação de dados.

Ele fornece uma API REST documentada com Swagger para cadastro, consulta, atualização e exclusão de notas de estudantes, além de cálculo automático da média final.

---

## ⚙️Funcionalidades Principais

* **Cadastro de Notas:** Registra um conjunto de 4 notas vinculadas ao `student_id`.
* **Rollback de Cadastro:** Recadastra um conjunto de notas em caso de falha em outro serviço.
* **Consulta de Notas:** Retorna o conjunto de notas de um estudante a partir de seu `student_id`.
* **Atualização de Notas:** Atualiza as quatro notas de um estudante, recalculando a média final.
* **Remoção de Notas:** Exclui o conjunto de notas de um estudante a partir do `student_id`.

---

## 🛠️Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework Web:** Flask
* **Validação:** Pydantic
* **ORM:** SQLAlchemy
* **Extensões:** Flask-CORS, flask-openapi3
* **Documentação:** Swagger (via flask-openapi3)
* **Banco de Dados:** SQLite (padrão), com suporte a outros via SQLAlchemy
* **Testes:** nose2
* **Tipagem:** typing_extensions

---

## 🌐Endpoints da API

### 📄 Documentação

* **Rota:** `/`
* **Método:** GET
* **Descrição:** Redireciona para a interface de documentação Swagger/OpenAPI.

---

### ➕ Cadastro de Notas

* **Rota:** `/grade`
* **Método:** POST
* **Descrição:** Adiciona um conjunto vazio de notas para um estudante com base no `student_id`.
* **Body Exemplo:**

```json
{
  "student_id": 1
}
```

---

### 🔁 Rollback de Cadastro

* **Rota:** `/grade/rollback`
* **Método:** POST
* **Descrição:** Adiciona todas as notas novamente com base em dados completos, para operações de rollback.
* **Body Exemplo:**

```json
{
  "student_id": 1,
  "grade_1": 8.0,
  "grade_2": 7.5,
  "grade_3": 6.0,
  "grade_4": 9.0,
  "final_average": 7.625
}
```

---

### 🔎 Consulta de Notas

* **Rota:** `/grade`
* **Método:** GET
* **Query Param:** `student_id=1`
* **Descrição:** Retorna o conjunto de notas associado ao `student_id`.

---

### ✏️ Atualização de Notas

* **Rota:** `/grade`
* **Método:** PUT
* **Query Param:** `student_id=1`
* **Body Exemplo:**

```json
{
  "grade_1": 9.0,
  "grade_2": 8.5,
  "grade_3": 7.0,
  "grade_4": 8.0
}
```

---

### 🗑️ Remoção de Notas

* **Rota:** `/grade`
* **Método:** DELETE
* **Query Param:** `student_id=1`
* **Descrição:** Remove o conjunto de notas associado ao `student_id`.

---

## 🚀Como Executar o Projeto

### Executando Localmente com Virtual Enviroment

#### Pré-requisitos:

* Python 3.10+
* pip (gerenciador de pacotes)
* (Opcional) Ambiente virtual

#### Passos:

1. Clone este repositório:

```bash
git clone https://github.com/RafaelLambert/mvp-arquitetura-de-software-api-grade.git
cd mvp-arquitetura-de-software-api-grade
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
python app.py
```

A aplicação estará disponível em: [http://localhost:5002](http://localhost:5002)
A documentação Swagger estará disponível em: [http://localhost:5002/openapi](http://localhost:5002/openapi)

---

### 🐳Executando via Dockerfile

#### Pré-requisitos:

* Docker
* Docker Compose
* WSL2 (para usuários Windows)

#### Passos:

1. Clone este repositório:

```bash
git clone https://github.com/RafaelLambert/mvp-arquitetura-de-software-api-grade.git
cd mvp-arquitetura-de-software-api-grade
```

2. Abra um terminal no diretório do `Dockerfile` e entre na distro padrão:

```bash
wsl
```

3. Construir Imagem Docker:

```bash
docker build -t api-grade .
```

4. Verificar se a imagem foi criada:

```bash
docker images
```

5. Rodar o container:

```bash
docker run -d -p 5002:5002 --name container-grade api-grade
```

6. Verificar containers ativos:

```bash
docker ps
```

7. A aplicação será iniciada em:

* **API Grade:** [http://localhost:5002](http://localhost:5002)
* **Documentação Swagger:** [http://localhost:5002/openapi](http://localhost:5002/openapi)

---

### 🐳 Executando com Docker Compose

#### Pré-requisitos:

* Docker
* Docker Compose (no serviço de Gateway)
* WSL2 (para usuários Windows)

#### Passos:

1. Clone este e os demais repositórios que compõem o sistema de microserviços:

```bash
git clone https://github.com/RafaelLambert/mvp-arquitetura-de-software-api-escola-front.git
git clone https://github.com/RafaelLambert/mvp-arquitetura-de-software-api-gateway.git
git clone https://github.com/RafaelLambert/mvp-arquitetura-de-software-api-auth.git
git clone https://github.com/RafaelLambert/mvp-arquitetura-de-software-api-grade.git
git clone https://github.com/RafaelLambert/mvp-arquitetura-de-software-api-student.git
```

2. Certifique-se de que o `docker-compose.yml` está dentro do projeto *mvp-arquitetura-de-software-api-gateway*.
3. Execute o seguinte comando no diretório do gateway:

```bash
docker-compose up --build
```

4. A aplicação estará disponível em:

* **API Grade:** [http://localhost:5002](http://localhost:5002)
* **Documentação Swagger:** [http://localhost:5002/openapi](http://localhost:5002/openapi)

---

## 📄Licença

Este projeto foi desenvolvido como parte de um MVP para a PUC-Rio e é destinado exclusivamente a fins educacionais.
