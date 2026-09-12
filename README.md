# Bar do Jaum — Agente de Vendas e Painel de Delivery Conversacional

Agente de vendas conversacional para delivery de bebidas, desenvolvido com **Python, FastAPI, Groq, Supabase/PostgreSQL e Redis**.

O projeto combina um agente de IA para atendimento de clientes via WhatsApp com um painel administrativo para acompanhamento de pedidos, métricas, simulação de conversas e visualização do histórico de mensagens.

O sistema foi desenvolvido com foco em:

* Atendimento conversacional.
* Consulta de produtos diretamente no banco de dados.
* Controle de estoque.
* Criação e acompanhamento de pedidos.
* Aprovação humana antes de ações irreversíveis.
* Histórico das conversas.
* Dashboard administrativo.
* Observabilidade de LLM com Langfuse.
* Arquitetura modular.
* Execução containerizada com Docker.

---

# 1. Documentação completa do projeto

Toda a documentação técnica e arquitetural do **Bar do Jaum — Delivery AI Agent** está disponível em uma página dedicada:

[Bar do Jaum — Delivery AI Agent](https://jeantheodoro.github.io/doc_agent_delivery/?utm_source=chatgpt.com)

A documentação apresenta uma visão completa do projeto, incluindo:

* Problema de negócio.
* Solução proposta.
* Personas.
* Arquitetura da aplicação.
* Workflow conversacional.
* Máquina de estados.
* PRD — Product Requirements Document.
* SPECs — Especificações técnicas.
* ADRs — Architecture Decision Records.
* Contratos da API.
* Estrutura do banco de dados.
* Human-in-the-Loop.
* Gestão de pedidos.
* Dashboard administrativo.
* Stack tecnológica.
* Segurança e guardrails.
* Separação entre LLM e regras determinísticas.
* Evolução arquitetural do projeto.

A documentação também apresenta diagramas dos fluxos de atendimento, arquitetura, estados dos pedidos e integração entre frontend, FastAPI, PostgreSQL/Supabase, Redis e demais componentes.

### Documentação por camada

```text
Documentação do Projeto
│
├── Problema
├── Solução
├── Personas
├── Arquitetura
├── Workflow
│
├── PRD
│   ├── Objetivos
│   ├── Escopo
│   ├── Requisitos funcionais
│   ├── Requisitos não funcionais
│   └── Métricas
│
├── SPECs
│   ├── Contratos da API
│   ├── Regras de negócio
│   ├── Máquina de estados
│   └── Responsabilidades técnicas
│
├── ADRs
│   ├── Monólito Modular
│   ├── PostgreSQL
│   ├── Human-in-the-Loop
│   ├── IA + Código Determinístico
│   └── Workflow Determinístico
│
├── Banco de Dados
├── Human-in-the-Loop
├── Dashboard
└── Stack Tecnológica
```

O princípio central documentado é separar a capacidade do LLM de interpretar linguagem natural das regras determinísticas executadas pelo backend.

---

# 2. Visão geral

O **JaumBot** atua como um vendedor virtual do Bar do Jaum.

O cliente pode enviar mensagens como:

```text
Quero duas Heineken e uma Coca-Cola
```

O agente interpreta a solicitação, consulta o catálogo oficial no banco de dados, verifica disponibilidade e conduz a conversa até obter os dados necessários para finalizar o pedido.

Antes da aprovação definitiva, o pedido permanece aguardando intervenção humana.

O sistema utiliza:

* **Groq API** para processamento com LLM.
* **Supabase/PostgreSQL** como fonte oficial de dados.
* **Redis** para sessões e infraestrutura do processamento assíncrono.
* **Celery** para tarefas em background.
* **Langfuse** para observabilidade de LLM.
* **FastAPI** como backend.
* **HTML, CSS e JavaScript** para o painel administrativo.

---

# 3. Arquitetura

A aplicação segue uma arquitetura modular baseada no fluxo:

```text
Cliente
   |
   v
WhatsApp / Webhook
   |
   v
Input Guardrail
   |
   v
Classifier
   |
   v
Sales Agent
   |
   +----------------------+
   |                      |
   v                      v
Search Products      Order Flow
   |                      |
   v                      v
Product Service      Order Service
   |                      |
   v                      v
PostgreSQL/Supabase   Pedido PENDING
                          |
                          v
                    Aprovação humana
                          |
                          v
                       APPROVED
```

---

# 4. Fluxo principal do agente

```text
Mensagem do cliente
        |
        v
Input Guardrail
        |
        v
Classificação da intenção
        |
        v
Sales Agent
        |
        +--------------------+
        |                    |
        v                    v
Consulta de produtos    Fluxo de pedido
        |                    |
        v                    v
Catálogo PostgreSQL      Session
                             |
                             v
                         Order Flow
                             |
                             v
                        Pedido PENDING
                             |
                             v
                     Aprovação humana
                             |
                             v
                         APPROVED
```

---

# 5. Guardrails

Antes da utilização do LLM, a mensagem passa por uma camada de proteção.

Os guardrails são responsáveis por identificar situações como:

* Prompt injection.
* Tentativas de manipulação do agente.
* Solicitações de acesso a informações internas.
* Solicitações para ignorar regras do sistema.
* Solicitações de atendimento humano.
* Mensagens que exigem escalonamento.

---

# 6. Provedor de LLM

O projeto utiliza atualmente a **API da Groq** como provedor de LLM.

O modelo utilizado é:

```env
GROQ_MODEL=openai/gpt-oss-120b
```

O provider é definido por:

```env
LLM_PROVIDER=groq
```

Portanto, o fluxo atual é:

```text
JaumBot
   |
   v
Groq API
   |
   v
openai/gpt-oss-120b
```

---

# 7. Banco de dados

O projeto utiliza **Supabase como infraestrutura do banco PostgreSQL**.

O PostgreSQL é a fonte oficial dos dados relacionados ao negócio.

As informações de:

* Produto.
* Descrição.
* Categoria.
* Volume.
* Preço.
* Estoque.
* Disponibilidade.

são obtidas do banco de dados.

A conexão é configurada através de:

```env
SUPABASE_DATABASE_URL=...
```

---

# 8. Configuração do ambiente

As variáveis de ambiente utilizadas pela aplicação devem ser configuradas em:

```text
src/.env
```

Exemplo:

```env
# =========================
# LANGFUSE
# =========================

LANGFUSE_SECRET_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_BASE_URL=


# =========================
# SUPABASE
# =========================

SUPABASE_DATABASE_URL=


# =========================
# GROQ
# =========================

GROQ_MODEL=openai/gpt-oss-120b
GROQ_API_KEY=


# =========================
# OPENAI
# =========================

OPENAI_API_KEY=
OPENAI_BASE_URL=
OPENAI_MODEL=


# =========================
# PROVIDER
# =========================

LLM_PROVIDER=groq


# =========================
# REDIS
# =========================

REDIS_URL=redis://redis:6379/0


# =========================
# EMAIL
# =========================

EMAIL_ORIGEM=
SENHA_APP=
EMAIL_DESTINO=
```

As credenciais reais não devem ser versionadas no Git.

---
# 9. Como executar a aplicação

O projeto foi preparado para ser executado através do **Docker Compose**.

Dessa forma, uma pessoa que clonar o repositório não precisa instalar Python, Redis, Celery ou configurar manualmente os serviços da aplicação.

É necessário apenas:

* Git
* Docker
* Docker Compose
* Credenciais dos serviços externos utilizados pelo projeto

---

## 9.1 Clonar o projeto

Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
```

---

## 9.2 Configurar as variáveis de ambiente

Antes de iniciar os containers, crie o arquivo:

```text
src/.env
```

Utilize o seguinte modelo:

```env
# =========================
# LANGFUSE
# =========================

LANGFUSE_SECRET_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_BASE_URL=


# =========================
# SUPABASE
# =========================

SUPABASE_DATABASE_URL=


# =========================
# GROQ
# =========================

GROQ_MODEL=openai/gpt-oss-120b
GROQ_API_KEY=


# =========================
# OPENAI
# =========================

OPENAI_API_KEY=
OPENAI_BASE_URL=
OPENAI_MODEL=


# =========================
# PROVIDER
# =========================

LLM_PROVIDER=groq


# =========================
# REDIS
# =========================

REDIS_URL=redis://redis:6379/0


# =========================
# EMAIL
# =========================

EMAIL_ORIGEM=
SENHA_APP=
EMAIL_DESTINO=
```

### Variáveis necessárias

Para executar o fluxo principal do agente, é necessário configurar principalmente:

```env
SUPABASE_DATABASE_URL=
GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-120b
LLM_PROVIDER=groq
REDIS_URL=redis://redis:6379/0
```

Para utilizar a observabilidade do Langfuse:

```env
LANGFUSE_SECRET_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_BASE_URL=
```

As configurações de e-mail devem ser preenchidas somente se a funcionalidade de envio de e-mails estiver sendo utilizada.

---

## 9.3 Serviços externos

O projeto utiliza alguns serviços externos que precisam estar configurados antes da execução.

### Groq

A aplicação utiliza a **API da Groq** para processamento das mensagens através do LLM.

É necessário possuir uma chave de API da Groq:

```env
GROQ_API_KEY=...
```

O modelo utilizado pelo projeto é:

```env
GROQ_MODEL=openai/gpt-oss-120b
```

E o provider:

```env
LLM_PROVIDER=groq
```

### Supabase

O projeto utiliza **Supabase/PostgreSQL** como banco de dados.

A conexão deve ser configurada através de:

```env
SUPABASE_DATABASE_URL=...
```

O banco deve estar preparado com a estrutura definida nos arquivos:

```text
sql/
├── create_table.sql
├── insert_dados.sql
├── query.sql
└── triggers.sql
```

### Langfuse

O Langfuse é utilizado para observabilidade das chamadas realizadas pelo agente.

As credenciais são configuradas através de:

```env
LANGFUSE_SECRET_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_BASE_URL=
```

---

## 9.4 Subir a aplicação

Depois de configurar o `src/.env`, execute na raiz do projeto:

```bash
docker compose up --build
```

Na primeira execução, o Docker irá:

1. Ler o `docker-compose.yml`.
2. Construir as imagens da aplicação.
3. Instalar as dependências.
4. Criar os containers.
5. Iniciar a API.
6. Iniciar o Redis.
7. Iniciar o worker do Celery.
8. Conectar a aplicação ao Supabase.
9. Permitir que o agente utilize a API da Groq.

Depois que os serviços estiverem iniciados, a aplicação estará disponível conforme as portas configuradas no `docker-compose.yml`.

---

## 9.5 Executar em segundo plano

Caso não queira manter o terminal ocupado com os logs:

```bash
docker compose up --build -d
```

O parâmetro `-d` executa os containers em segundo plano.

Depois disso, é possível verificar o estado dos serviços:

```bash
docker compose ps
```

---

## 9.6 Verificar os logs

Para acompanhar a execução da aplicação:

```bash
docker compose logs -f
```

Esse comando é especialmente útil na primeira execução para verificar se todos os serviços foram iniciados corretamente.

Caso seja necessário investigar um problema, os logs também permitem identificar:

* Erros de conexão com o banco.
* Problemas com Redis.
* Problemas na API da Groq.
* Erros de configuração.
* Falhas no worker.
* Erros da aplicação.

---

## 9.7 Acessar a aplicação

Com os containers executando, a aplicação pode ser acessada através do endereço configurado no Docker Compose.

Em uma configuração local padrão:

```text
http://127.0.0.1:8000
```

A API disponibiliza também os endpoints utilizados pelo painel administrativo e pelo agente.

---

## 9.8 Testar a API

A API pode ser testada utilizando o endpoint:

```text
POST /whatsapp/webhook
```

Exemplo:

```json
{
    "phone": "5511999999999",
    "message": "Quero duas Heineken"
}
```

Também estão disponíveis os endpoints administrativos:

```text
GET   /admin/orders/
GET   /admin/orders/{order_id}/details
PATCH /admin/orders/{order_id}/status
GET   /admin/orders/messages
GET   /admin/dashbord
```

---

## 9.9 Parar a aplicação

Para parar os containers:

```bash
docker compose down
```

Para iniciar novamente posteriormente:

```bash
docker compose up
```

Caso tenha ocorrido alguma alteração no Dockerfile ou nas dependências:

```bash
docker compose up --build
```

---

## 9.10 Fluxo completo para uma nova instalação

Para uma pessoa executando o projeto pela primeira vez:

```bash
# 1. Clonar
git clone <URL_DO_REPOSITORIO>

# 2. Entrar no projeto
cd projeto_agente_delivery_bar_jaum

# 3. Criar/configurar
src/.env

# 4. Subir a aplicação
docker compose up --build
```

Em uma segunda execução:

```bash
docker compose up
```

Para executar em segundo plano:

```bash
docker compose up -d
```

Para acompanhar os logs:

```bash
docker compose logs -f
```

Para verificar os containers:

```bash
docker compose ps
```

Para parar:

```bash
docker compose down
```

---

## 9.11 O que é necessário para executar o projeto

Em resumo, quem quiser executar o **Bar do Jaum** precisa ter:

```text
Computador
   |
   +-- Git
   |
   +-- Docker
   |
   +-- Docker Compose
   |
   +-- Projeto clonado
   |
   +-- src/.env configurado
   |
   +-- Conta/API Groq
   |
   +-- Banco Supabase configurado
   |
   +-- Langfuse configurado (opcional)
   |
   v
docker compose up --build
   |
   v
Aplicação executando
```

O objetivo dessa estrutura é permitir que o projeto seja reproduzido em outro ambiente sem a necessidade de instalar manualmente toda a stack Python e infraestrutura local.


---

# 10. Painel administrativo

O painel possui as seguintes áreas:

```text
Pedidos
Simulador
Administrativo
Mensagens
```

O frontend está organizado em:

```text
src/
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── app.js
```

---

# 11. Dashboard

O dashboard permite consultar:

* Total de pedidos.
* Receita total.
* Ticket médio.
* Produtos mais vendidos.
* Filtros por período.

Endpoint:

```http
GET /admin/dashbord?start_date=2026-09-01&end_date=2026-09-09
```

---

# 12. Endpoints principais

A aplicação disponibiliza uma API REST construída com **FastAPI**.

## WhatsApp Webhook

### POST `/whatsapp/webhook`

Recebe mensagens enviadas pelo cliente e encaminha a solicitação para o fluxo conversacional do agente.

```http
POST /whatsapp/webhook
```

Exemplo de payload:

```json
{
    "phone": "5511999999999",
    "message": "Quero duas Heineken"
}
```

---

# Admin Orders

## GET `/admin/orders/`

Retorna a lista de pedidos cadastrados.

```http
GET /admin/orders/
```

Utilizado pela aba **Pedidos** do painel administrativo.

---

## GET `/admin/orders/{order_id}/details`

Retorna os detalhes de um pedido específico.

```http
GET /admin/orders/{order_id}/details
```

Permite consultar informações como:

* Cliente.
* Telefone.
* Endereço.
* Forma de pagamento.
* Itens.
* Quantidades.
* Valores.
* Status do pedido.
* Informações relacionadas à aprovação.

---

## PATCH `/admin/orders/{order_id}/status`

Atualiza o status de um pedido.

```http
PATCH /admin/orders/{order_id}/status
```

Estados utilizados pelo sistema:

```text
PENDING
APPROVED
OUT_FOR_DELIVERY
COMPLETED
CANCELLED
```

---

## GET `/admin/orders/messages`

Retorna todas as mensagens registradas no sistema, com ou sem pedidos vinculados.

```http
GET /admin/orders/messages
```

Esse endpoint é utilizado pela aba **Mensagens** do painel administrativo.

Permite visualizar:

* Mensagens vinculadas a pedidos.
* Mensagens sem pedidos.
* Histórico das conversas.
* Diálogos entre cliente e agente.

---

# Admin Dashboard

## GET `/admin/dashbord`

Retorna o resumo das métricas administrativas e os produtos mais relevantes dentro de um intervalo de datas.

```http
GET /admin/dashbord
```

Parâmetros:

```text
start_date
end_date
```

Exemplo:

```http
GET /admin/dashbord?start_date=2026-09-01&end_date=2026-09-09
```

O endpoint é utilizado pela aba **Administrativo** do painel.

As informações retornadas incluem:

* Total de pedidos.
* Receita total.
* Ticket médio.
* Top produtos.

Exemplo:

```json
{
    "total_orders": 35,
    "total_revenue": 771.5,
    "average_ticket": 22.042857
}
```

---

# Resumo dos endpoints

| Método  | Endpoint                           | Descrição                                   |
| ------- | ---------------------------------- | ------------------------------------------- |
| `POST`  | `/whatsapp/webhook`                | Recebe mensagens do WhatsApp                |
| `GET`   | `/admin/orders/`                   | Lista todos os pedidos                      |
| `GET`   | `/admin/orders/{order_id}/details` | Consulta detalhes de um pedido              |
| `PATCH` | `/admin/orders/{order_id}/status`  | Atualiza o status do pedido                 |
| `GET`   | `/admin/orders/messages`           | Lista todas as mensagens, com ou sem pedido |
| `GET`   | `/admin/dashbord`                  | Retorna métricas e top produtos             |


---

# 13. Máquina de estados dos pedidos

```text
PENDING
   |
   | Aprovação humana
   v
APPROVED
   |
   | Despacho
   v
OUT_FOR_DELIVERY
   |
   | Entrega
   v
COMPLETED
```

Cancelamento:

```text
PENDING ─────────> CANCELLED
APPROVED ────────> CANCELLED
```

---

# 14. Human-in-the-Loop

O projeto utiliza aprovação humana antes do processamento operacional do pedido.

O fluxo é:

```text
Cliente
   |
   v
JaumBot
   |
   v
Pedido criado
   |
   v
PENDING
   |
   v
Painel Administrativo
   |
   v
Revisão Humana
   |
   +------------+
   |            |
 Aprovar      Rejeitar
   |            |
   v            v
APPROVED     CANCELLED
```

Essa abordagem mantém a IA responsável pela interpretação e conversação, enquanto o backend controla as operações críticas.

---

# 15. Documentação local

Além da documentação online, o projeto mantém os documentos dentro de:

```text
docs/
```

Principais arquivos:

```text
docs/
├── PRD.md
├── SPECs.md
├── ADRs.md
├── FLOWCHART.md
├── AMIRD.md
├── dialogos.md
└── status_aprroved.md
```

A documentação online funciona como uma visão consolidada e navegável desses artefatos e dos principais fluxos do projeto.

---

# 16. Tecnologias

### Backend

* Python 3.13
* FastAPI
* Pydantic
* SQLAlchemy
* PostgreSQL
* Supabase
* Redis
* Celery

### Inteligência Artificial

* Groq API
* `openai/gpt-oss-120b`
* LLM Agents
* Guardrails
* Prompt Engineering

### Observabilidade

* Langfuse

### Frontend

* HTML
* CSS
* JavaScript
* Tailwind CSS
* Lucide

### Infraestrutura

* Docker
* Docker Compose
* uv

---

# 17. Estrutura do projeto

```text
.
├── Dockerfile
├── README.md
├── assets
│   ├── Desafio_jn_2026-09-06 135808.mp4
│   └── Gravacao_da_aplicao_funciobado.mp4
├── celerybeat-schedule
├── docker-compose.yml
├── docs
│   ├── ADRs.md
│   ├── AMIRD.md
│   ├── FLOWCHART.md
│   ├── PRD.md
│   ├── SPECs.md
│   ├── dialogos.md
│   └── status_aprroved.md
├── pyproject.toml
├── sql
│   ├── create_table.sql
│   ├── insert_dados.sql
│   ├── query.sql
│   └── triggers.sql
├── src
│   ├── agent
│   ├── api
│   ├── core
│   ├── main.py
│   ├── models
│   ├── repositories
│   ├── schemas
│   ├── scripts
│   ├── services
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       └── app.js
│   ├── tasks
│   └── templates
│       └── index.html
├── teste_smt.py
└── uv.lock
```

---

# 18. Documentação online

Para conhecer a arquitetura, os requisitos, os fluxos, os contratos da API, a máquina de estados, o banco de dados, as decisões arquiteturais e o funcionamento completo do projeto:

**Bar do Jaum — Delivery AI Agent**

[Acessar documentação completa do projeto](https://jeantheodoro.github.io/doc_agent_delivery/?utm_source=chatgpt.com)

---

# 19. Status atual

O projeto possui atualmente:

* Agente conversacional.
* Groq como provider de LLM.
* Modelo `openai/gpt-oss-120b`.
* Supabase/PostgreSQL.
* Redis.
* Celery.
* Langfuse.
* Input Guardrails.
* Consulta de produtos.
* Fluxo de criação de pedidos.
* Human-in-the-Loop.
* Controle de estados dos pedidos.
* Painel administrativo.
* Dashboard de métricas.
* Simulador de conversas.
* Histórico de mensagens.
* Consulta de pedidos.
* Controle de status.
* Arquitetura modular FastAPI.
* Execução com Docker Compose.
* Documentação técnica online completa.
