# PRD — Documento de Requisitos de Produto

## Projeto: Bar do Jaum — Agente de Vendas e Painel de Delivery Conversacional

---

# 1. Visão Geral e Contexto do Negócio

## 1.1 Nome do Negócio

**Bar do Jaum**

## 1.2 Dono / Cliente Contratante

**Seu Jaum**

Comerciante tradicional que busca modernizar o delivery de bebidas geladas e porções, mas exige controle total sobre o processo operacional.

## 1.3 Nome do Produto

**JaumBot**

Agente conversacional de vendas via WhatsApp integrado a um painel administrativo Web para gerenciamento do delivery.

## 1.4 Público-Alvo

### 1.4.1 Consumidor Final

Clientes locais que realizam compras por necessidade imediata e preferem interação por linguagem natural em vez de navegar por filtros e categorias tradicionais de e-commerce.

Exemplos de interações:

> "Quero algo gelado para ver o jogo."

> "Manda umas cervejas e um refrigerante."

> "O que vocês têm de cerveja?"

---

# 2. O Problema

O modelo tradicional de e-commerce exige que o cliente navegue por categorias, encontre produtos, selecione quantidades e monte um carrinho.

Esse fluxo não representa o comportamento esperado dos clientes do Bar do Jaum, que frequentemente preferem simplesmente enviar uma mensagem pelo WhatsApp descrevendo o que desejam.

O sistema deve permitir uma experiência de compra conversacional, mas sem abrir mão de controle, segurança e previsibilidade.

## 2.1 Riscos e Preocupações do Negócio

O sistema deve mitigar os seguintes riscos:

### 2.1.1 Alucinação de Produtos, Preços ou Prazos

* O agente não deve inventar produtos.
* O agente não deve inventar preços.
* O agente não deve informar estoque inexistente.
* Informações comerciais devem ser obtidas a partir da fonte oficial.

### 2.1.2 Manipulação da Inteligência Artificial

* Usuários mal-intencionados não devem conseguir manipular o comportamento interno do agente.
* O sistema deve possuir mecanismos de proteção contra prompt injection e tentativas de extração de informações internas.

### 2.1.3 Execuções Irreversíveis sem Revisão

* A IA não deve possuir autonomia para executar operações críticas sem controle.
* Pedidos gerados pelo agente devem passar por um checkpoint humano.

### 2.1.4 Custos Excessivos de IA

* O sistema deve evitar chamadas desnecessárias ao modelo.
* O contexto enviado ao LLM deve ser controlado.
* A arquitetura deve permitir monitoramento de consumo.

### 2.1.5 Vazamento de Dados

* Informações de clientes devem ser tratadas de forma controlada.
* O sistema deve evitar exposição desnecessária de dados sensíveis.

### 2.1.6 Falta de Auditabilidade

* Eventos relevantes devem ser rastreáveis.
* Alterações de pedidos devem permitir identificação do estado anterior e posterior.
* O histórico conversacional deve ser preservado quando aplicável.

---

# 3. Objetivos do Produto

O JaumBot deve:

* Automatizar o atendimento inicial dos clientes.
* Permitir pedidos através de linguagem natural.
* Consultar produtos diretamente no catálogo oficial.
* Evitar que a IA invente preços ou produtos.
* Criar pedidos estruturados a partir da conversa.
* Permitir revisão humana antes da execução de operações críticas.
* Disponibilizar um painel administrativo para gerenciamento dos pedidos.
* Permitir acompanhamento do ciclo de vida dos pedidos.
* Preservar histórico das conversas.
* Reduzir o tempo médio de atendimento.
* Manter controle sobre custos de utilização de IA.

---

# 4. Escopo da Versão 1 — MVP

## 4.1 Webhook do WhatsApp

Implementação de um agente stateful capaz de:

* Receber mensagens.
* Identificar o cliente através do telefone.
* Processar linguagem natural.
* Conduzir a venda passo a passo.
* Consultar produtos.
* Montar o pedido.
* Solicitar informações necessárias.
* Apresentar o pedido ao cliente.
* Encaminhar o pedido para aprovação.

### 4.1.1 Endpoint

```http
POST /whatsapp/webhook
```

---

## 4.2 Catálogo Relacional Rígido

Os dados comerciais devem ser obtidos diretamente do banco de dados relacional.

O agente não deve utilizar conhecimento próprio para determinar:

* Produtos disponíveis.
* Preços.
* Estoque.
* Categorias.
* Volumes.

A fonte oficial dos dados comerciais será o banco PostgreSQL.

Essa abordagem tem como objetivo reduzir alucinações e garantir conformidade entre as informações apresentadas ao cliente e os dados oficiais.

---

## 4.3 Painel Administrativo Web

O sistema deve disponibilizar um painel administrativo para gerenciamento dos pedidos.

O painel deve permitir:

* Visualizar pedidos.
* Visualizar detalhes do pedido.
* Acompanhar o status.
* Aprovar pedidos.
* Atualizar o status.
* Visualizar informações do cliente.
* Visualizar itens e valores.
* Consultar histórico de conversas.

A interface deve utilizar uma representação visual semelhante a um **Kanban**, organizada de acordo com o ciclo de vida dos pedidos.

---

## 4.4 Histórico de Chat

O painel deve permitir visualizar o histórico das conversas entre cliente e agente.

As mensagens devem ser apresentadas em formato de balões:

```text
Cliente

   │
   ▼

┌─────────────────────────┐
│ Quero duas cervejas.    │
└─────────────────────────┘

Bot

   │
   ▼

┌─────────────────────────┐
│ Claro! Qual cerveja?    │
└─────────────────────────┘
```

A identificação da conversa deve ser realizada através do telefone do cliente:

```text
customer_phone
```

---

## 4.5 Human-in-the-Loop

Pedidos criados pelo agente devem obrigatoriamente entrar no estado:

```text
PENDING
```

O pedido deve permanecer aguardando uma ação humana antes de avançar para o processamento operacional.

O operador deve realizar a aprovação através do painel administrativo.

Fluxo:

```text
Cliente
   ↓
WhatsApp
   ↓
Agente IA
   ↓
Pedido criado
   ↓
PENDING
   ↓
Revisão Humana
   ↓
APPROVED
```

---

# 5. Requisitos Funcionais

## 5.1 RF01 — Receber Mensagem

O sistema deve receber mensagens através do webhook do WhatsApp.

## 5.2 RF02 — Identificar Cliente

O sistema deve utilizar o telefone recebido para identificar ou criar a sessão do cliente.

## 5.3 RF03 — Processar Linguagem Natural

O agente deve interpretar solicitações realizadas em linguagem natural.

## 5.4 RF04 — Consultar Catálogo

O agente deve consultar o catálogo oficial antes de informar produtos, preços ou disponibilidade.

## 5.5 RF05 — Criar Pedido

O sistema deve transformar a intenção de compra em um pedido estruturado.

## 5.6 RF06 — Controlar Estado

O pedido deve possuir um estado correspondente à sua etapa atual.

## 5.7 RF07 — Aprovação Humana

Pedidos gerados pelo agente devem iniciar como `PENDING`.

## 5.8 RF08 — Gerenciar Pedidos

O painel administrativo deve permitir consultar e atualizar pedidos.

## 5.9 RF09 — Consultar Histórico

O administrador deve conseguir consultar o histórico da conversa relacionada ao cliente.

## 5.10 RF10 — Atualizar Status

O administrador deve conseguir alterar o status do pedido através da API.

---

# 6. Requisitos Não Funcionais

## 6.1 RNF01 — Segurança

O sistema deve possuir mecanismos de proteção contra:

* Prompt Injection.
* Tentativas de extração do System Prompt.
* Manipulação de contexto.
* Solicitações indevidas.
* Execuções não autorizadas.

## 6.2 RNF02 — Auditabilidade

Operações relevantes devem ser rastreáveis.

## 6.3 RNF03 — Confiabilidade

Informações comerciais devem possuir como fonte o banco de dados oficial.

## 6.4 RNF04 — Controle de Custos

Chamadas ao modelo devem ser minimizadas sempre que possível.

## 6.5 RNF05 — Separação de Responsabilidades

O sistema deve utilizar uma arquitetura em camadas:

```text
Router
   ↓
Service
   ↓
Repository
```

## 6.6 RNF06 — Escalabilidade Arquitetural

A solução inicial deve utilizar um **Monólito Modular**, permitindo evolução futura sem acoplamento excessivo entre os módulos.

---

# 7. Métricas de Sucesso

O sucesso do MVP será acompanhado através das seguintes métricas.

## 7.1 Conversão

**Taxa de conversão de conversas em pedidos criados no banco.**

```text
Pedidos Criados
──────────────────────── × 100
Conversas Iniciadas
```

## 7.2 Tempo Médio de Atendimento

Redução do **Tempo Médio de Atendimento (TMA)** em comparação ao atendimento manual realizado no balcão.

## 7.3 Conformidade Comercial

Garantir:

```text
100%
```

de conformidade entre os valores informados pelo agente e os valores existentes no banco de dados oficial.

## 7.4 Segurança Operacional

Garantir:

```text
0
```

execuções automáticas irreversíveis sem aprovação humana.

---

# 8. Especificações Técnicas

## 8.1 Backend

* **Framework:** FastAPI
* **Linguagem:** Python 3.11+
* **Arquitetura:** Monólito Modular
* **API:** REST

### 8.1.1 Camadas

```text
Router
   ↓
Service
   ↓
Repository
```

### 8.1.2 Responsabilidades

| Camada     | Responsabilidade                    |
| ---------- | ----------------------------------- |
| Router     | Comunicação HTTP e contratos da API |
| Service    | Regras de negócio e orquestração    |
| Repository | Persistência e acesso ao banco      |

---

# 9. Banco de Dados

## 9.1 Tecnologia

* **SGBD:** PostgreSQL
* **Plataforma:** Supabase
* **Schema:** `delivery`

Todas as tabelas relacionadas ao domínio de delivery devem utilizar o schema:

```text
delivery
```

O banco representa a fonte oficial para dados comerciais do sistema.

---

# 10. Frontend Administrativo

O painel administrativo deve utilizar:

* HTML5
* Tailwind CSS via CDN
* Vanilla JavaScript
* Polling automático

O frontend deve consumir exclusivamente os endpoints disponibilizados pela API.

## 10.1 Sincronização

```text
Admin Frontend
      │
      │ GET /admin/orders/
      ▼
   FastAPI
      │
      ▼
 PostgreSQL
      │
      │ Dados atualizados
      ▼
   FastAPI
      │
      ▼
Admin Frontend
```

---

# 11. Contratos de API

## 11.1 Webhook do WhatsApp

### 11.1.1 Endpoint

```http
POST /whatsapp/webhook
```

### 11.1.2 Request

```json
{
  "phone": "16999999999",
  "message": "Quero pedir uma Coca-Cola"
}
```

### 11.1.3 Campos

| Campo     | Tipo     | Obrigatório | Descrição                     |
| --------- | -------- | ----------: | ----------------------------- |
| `phone`   | `string` |         Sim | Número de telefone do cliente |
| `message` | `string` |         Sim | Mensagem enviada pelo cliente |

### 11.1.4 Response

```json
{
  "status": "success",
  "reply_message": "Fala, campeão! Bem-vindo ao Bar do Jaum. O que vai ser hoje? Manda a braba ou gostaria de ver quais produtos temos: cervejas, refrigerantes e água."
}
```

---

# 12. Gestão de Pedidos

## 12.1 Listagem de Pedidos

### 12.1.1 Endpoint

```http
GET /admin/orders/
```

### 12.1.2 Response

```json
{
  "id": "5716E9D6",
  "customer_name": "Paulo",
  "customer_phone": "16997214456",
  "address": "Rua: São João, 569. Jd. Novo Dia.",
  "total_amount": 9.00,
  "payment_method": "pix",
  "cash_received": null,
  "change_due": null,
  "status": "OUT_FOR_DELIVERY",
  "created_at": "2026-09-09T13:24:31.671650",
  "items": [
    {
      "product_name": "Guaraná Antarctica",
      "category": "refrigerante",
      "volume": "350ml",
      "quantity": 1,
      "unit_price": 4.00,
      "subtotal": 4.00
    }
  ]
}
```

### 12.1.3 Campos do Pedido

| Campo            | Tipo          | Descrição                  |
| ---------------- | ------------- | -------------------------- |
| `id`             | `string`      | Identificador único        |
| `customer_name`  | `string`      | Nome do cliente            |
| `customer_phone` | `string`      | Telefone                   |
| `address`        | `string`      | Endereço de entrega        |
| `total_amount`   | `number`      | Valor total                |
| `payment_method` | `string`      | Forma de pagamento         |
| `cash_received`  | `number/null` | Valor recebido em dinheiro |
| `change_due`     | `number/null` | Troco                      |
| `status`         | `string`      | Status do pedido           |
| `created_at`     | `datetime`    | Data e hora de criação     |
| `items`          | `array`       | Itens do pedido            |

---

# 13. Atualização de Status

## 13.1 Endpoint

```http
PATCH /admin/orders/{order_id}/status
```

## 13.2 Path Parameter

| Parâmetro  | Tipo     | Descrição               |
| ---------- | -------- | ----------------------- |
| `order_id` | `string` | Identificador do pedido |

## 13.3 Request

```json
{
  "status": "OUT_FOR_DELIVERY"
}
```

## 13.4 Response

```json
{
  "message": "Status atualizado com sucesso",
  "order_id": "01F98BEF",
  "new_status": "OUT_FOR_DELIVERY"
}
```

---

# 14. Máquina de Estados dos Pedidos

O ciclo de vida do pedido é controlado através do campo `status`.

## 14.1 Estados

### 14.1.1 `PENDING`

Pedido recebido via WhatsApp, aguardando validação, fechamento do carrinho e/ou aprovação humana.

### 14.1.2 `APPROVED`

Pedido confirmado e aprovado, aguardando separação pelo operador.

### 14.1.3 `OUT_FOR_DELIVERY`

Pedido despachado para entrega com o motoboy.

### 14.1.4 `COMPLETED`

Pedido entregue ao cliente e finalizado com sucesso.

### 14.1.5 `CANCELLED`

Pedido cancelado pelo cliente ou pelo estabelecimento.

---

# 15. Fluxo Principal

```text
┌─────────────┐
│   PENDING   │
│             │
│ Pedido      │
│ recebido    │
└──────┬──────┘
       │
       │ Aprovação humana
       ▼
┌─────────────┐
│  APPROVED   │
│             │
│ Pedido      │
│ aprovado    │
└──────┬──────┘
       │
       │ Despacho
       ▼
┌─────────────────────┐
│ OUT_FOR_DELIVERY     │
│                     │
│ Pedido em entrega   │
└──────────┬──────────┘
           │
           │ Entrega realizada
           ▼
┌─────────────┐
│  COMPLETED  │
│             │
│ Pedido      │
│ finalizado  │
└─────────────┘
```

---

# 16. Fluxo de Cancelamento

Um pedido pode ser cancelado conforme as regras de negócio.

```text
PENDING
   │
   │ Cancelamento
   ▼
CANCELLED
```

```text
APPROVED
   │
   │ Cancelamento
   ▼
CANCELLED
```

## 16.1 Fluxo Consolidado

```text
                    ┌─────────────┐
                    │   PENDING   │
                    └──────┬──────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             │ Aprovação                 │ Cancelamento
             ▼                           ▼
      ┌─────────────┐             ┌─────────────┐
      │  APPROVED   │             │  CANCELLED  │
      └──────┬──────┘             └─────────────┘
             │
             │ Despacho
             ▼
      ┌─────────────────────┐
      │ OUT_FOR_DELIVERY    │
      └──────────┬──────────┘
                 │
                 │ Entrega
                 ▼
          ┌─────────────┐
          │  COMPLETED  │
          └─────────────┘
```

---

# 17. Estados Permitidos

```text
PENDING
APPROVED
OUT_FOR_DELIVERY
COMPLETED
CANCELLED
```

## 17.1 Fluxo Principal

```text
PENDING
   ↓
APPROVED
   ↓
OUT_FOR_DELIVERY
   ↓
COMPLETED
```

## 17.2 Fluxo de Cancelamento

```text
PENDING ─────────────► CANCELLED

APPROVED ────────────► CANCELLED
```

---

# 18. Princípios Arquiteturais

O projeto deve seguir os seguintes princípios:

* **Separação de responsabilidades**
* **Baixo acoplamento**
* **Alta coesão**
* **Regras de negócio concentradas nos Services**
* **Acesso ao banco concentrado nos Repositories**
* **Routers responsáveis pela camada HTTP**
* **Contratos de API bem definidos**
* **Banco de dados como fonte oficial dos dados comerciais**
* **Frontend desacoplado do backend**
* **Comunicação através de API REST**
* **Controle humano para operações críticas**
* **Monólito Modular como arquitetura inicial**

---

# 19. Componentes Principais

| Componente     | Tecnologia / Estratégia        |
| -------------- | ------------------------------ |
| Backend        | FastAPI                        |
| Linguagem      | Python 3.11+                   |
| Arquitetura    | Monólito Modular               |
| API            | REST                           |
| Banco          | PostgreSQL                     |
| Plataforma     | Supabase                       |
| Schema         | `delivery`                     |
| Frontend Admin | HTML5                          |
| Estilização    | Tailwind CSS                   |
| JavaScript     | Vanilla JavaScript             |
| Sincronização  | Polling automático             |
| Integração     | WhatsApp                       |
| IA             | Agente conversacional          |
| Segurança      | Guardrails + Human-in-the-Loop |
| Catálogo       | Banco relacional               |

---

# 20. Endpoints Principais

| Método  | Endpoint                          | Responsabilidade              |
| ------- | --------------------------------- | ----------------------------- |
| `POST`  | `/whatsapp/webhook`               | Receber mensagens do WhatsApp |
| `GET`   | `/admin/orders/`                  | Listar pedidos                |
| `PATCH` | `/admin/orders/{order_id}/status` | Atualizar status              |

---

# 21. Visão Geral da Arquitetura

```text
                         ┌─────────────────┐
                         │    WhatsApp     │
                         └────────┬────────┘
                                  │
                                  │ Mensagem
                                  ▼
                         ┌─────────────────┐
                         │ FastAPI Webhook │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     Router      │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     Service     │
                         │                 │
                         │ Regras de       │
                         │ negócio         │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Repository    │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   PostgreSQL    │
                         │    Supabase     │
                         │                 │
                         │ schema:         │
                         │ delivery        │
                         └─────────────────┘
```

---

# 22. Fluxo Geral do Produto

```text
┌──────────────┐
│   Cliente    │
└──────┬───────┘
       │
       │ WhatsApp
       ▼
┌──────────────┐
│   Webhook    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Agente IA  │
└──────┬───────┘
       │
       ├──────────────► Consulta catálogo
       │                       │
       │                       ▼
       │                ┌──────────────┐
       │                │ PostgreSQL   │
       │                │ delivery     │
       │                └──────────────┘
       │
       ▼
┌──────────────┐
│    Pedido    │
│   PENDING    │
└──────┬───────┘
       │
       │ Revisão humana
       ▼
┌──────────────┐
│   APPROVED   │
└──────┬───────┘
       │
       │ Separação / despacho
       ▼
┌──────────────────────┐
│  OUT_FOR_DELIVERY    │
└──────────┬───────────┘
           │
           │ Entrega
           ▼
┌──────────────┐
│  COMPLETED   │
└──────────────┘
```

---

# 23. Objetivo deste Documento

Este documento consolida os requisitos de produto e as especificações técnicas do **Bar do Jaum — JaumBot**.

Ele deve servir como referência para:

* Desenvolvimento do backend.
* Desenvolvimento do agente conversacional.
* Desenvolvimento do painel administrativo.
* Modelagem e persistência dos dados.
* Definição dos contratos da API.
* Implementação da máquina de estados.
* Implementação dos mecanismos de segurança.
* Implementação do Human-in-the-Loop.
* Evolução da arquitetura.
* Validação das decisões arquiteturais.

As decisões que justificam as escolhas arquiteturais e técnicas devem ser registradas separadamente no arquivo:

```text
ADRs.md
```

---

# 24. Documentação do Projeto

Estrutura recomendada:

```text
/
├── README.md
├── PRD.md
├── SPECs.md
├── ADRs.md
└── ...
```

### 24.1 README.md

Apresentação, instalação, execução e visão geral do projeto.

### 24.2 PRD.md

Requisitos de produto, objetivos, escopo e regras funcionais.

### 24.3 SPECs.md

Especificações técnicas, contratos de API e máquina de estados.

### 24.4 ADRs.md

Registro das decisões arquiteturais.
