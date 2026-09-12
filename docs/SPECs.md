# Especificações Técnicas e Comportamentais (SPECs)

## Projeto: Bar do Jaum

---

## 1. Stack Tecnológica

### 1.1 Backend

* **Framework:** FastAPI
* **Linguagem:** Python 3.11+
* **Arquitetura:** Monólito Modular
* **Organização em camadas:**

```text
Router
   ↓
Service
   ↓
Repository
```

A aplicação deve manter a separação de responsabilidades entre as camadas de apresentação, regras de negócio e acesso aos dados.

### 1.2 Banco de Dados

* **SGBD:** PostgreSQL
* **Plataforma:** Supabase
* **Schema:** `delivery`

Todas as tabelas relacionadas ao domínio de delivery devem utilizar o schema `delivery`.

### 1.3 Frontend Administrativo

O painel administrativo deve utilizar:

* **HTML5**
* **Tailwind CSS** via CDN
* **Vanilla JavaScript**
* **Polling automático** para sincronização dos pedidos

O frontend administrativo deve consumir exclusivamente os endpoints disponibilizados pela API.

---

# 2. Contratos de API

## 2.1 Webhook do WhatsApp

Endpoint responsável pelo recebimento das mensagens enviadas pelo cliente.

### Método e Rota

```http
POST /whatsapp/webhook
```

### Payload de Entrada

```json
{
  "phone": "16999999999",
  "message": "Quero pedir uma Coca-Cola"
}
```

### Campos

| Campo     | Tipo     | Obrigatório | Descrição                     |
| --------- | -------- | ----------: | ----------------------------- |
| `phone`   | `string` |         Sim | Número de telefone do cliente |
| `message` | `string` |         Sim | Mensagem enviada pelo cliente |

### Payload de Saída

```json
{
  "status": "success",
  "reply_message": "Fala, campeão! Bem-vindo ao Bar do Jaum. O que vai ser hoje? Manda a braba ou gostaria de ver quais produtos temos: cervejas, refrigerantes e água."
}
```

### Campos da Resposta

| Campo           | Tipo     | Descrição                              |
| --------------- | -------- | -------------------------------------- |
| `status`        | `string` | Resultado do processamento da mensagem |
| `reply_message` | `string` | Resposta enviada ao cliente            |

---

# 3. Gestão de Pedidos — Painel Administrativo

## 3.1 Listagem de Pedidos

Endpoint responsável por retornar os pedidos disponíveis para o painel administrativo.

### Método e Rota

```http
GET /admin/orders/
```

### Payload de Saída

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

### Campos do Pedido

| Campo            | Tipo          | Descrição                     |
| ---------------- | ------------- | ----------------------------- |
| `id`             | `string`      | Identificador único do pedido |
| `customer_name`  | `string`      | Nome do cliente               |
| `customer_phone` | `string`      | Telefone do cliente           |
| `address`        | `string`      | Endereço de entrega           |
| `total_amount`   | `number`      | Valor total do pedido         |
| `payment_method` | `string`      | Forma de pagamento            |
| `cash_received`  | `number/null` | Valor recebido em dinheiro    |
| `change_due`     | `number/null` | Troco calculado               |
| `status`         | `string`      | Estado atual do pedido        |
| `created_at`     | `datetime`    | Data e hora de criação        |
| `items`          | `array`       | Itens pertencentes ao pedido  |

### Campos dos Itens

| Campo          | Tipo      | Descrição             |
| -------------- | --------- | --------------------- |
| `product_name` | `string`  | Nome do produto       |
| `category`     | `string`  | Categoria do produto  |
| `volume`       | `string`  | Volume ou tamanho     |
| `quantity`     | `integer` | Quantidade solicitada |
| `unit_price`   | `number`  | Preço unitário        |
| `subtotal`     | `number`  | Valor total do item   |

---

# 4. Atualização de Status do Pedido

Endpoint utilizado pelo painel administrativo para alterar o estado de um pedido.

### Método e Rota

```http
PATCH /admin/orders/{order_id}/status
```

### Path Parameter

| Parâmetro  | Tipo     | Descrição                     |
| ---------- | -------- | ----------------------------- |
| `order_id` | `string` | Identificador único do pedido |

### Payload de Entrada

```json
{
  "status": "OUT_FOR_DELIVERY"
}
```

### Payload de Saída

```json
{
  "message": "Status atualizado com sucesso",
  "order_id": "01F98BEF",
  "new_status": "OUT_FOR_DELIVERY"
}
```

### Campos da Resposta

| Campo        | Tipo     | Descrição                           |
| ------------ | -------- | ----------------------------------- |
| `message`    | `string` | Mensagem de confirmação da operação |
| `order_id`   | `string` | Identificador do pedido atualizado  |
| `new_status` | `string` | Novo status do pedido               |

---

# 5. Máquina de Estados dos Pedidos

O ciclo de vida de um pedido é controlado através do campo `status`.

## 5.1 Estados

### `PENDING`

Pedido recebido via WhatsApp, aguardando validação ou fechamento do carrinho.

### `APPROVED`

Pedido confirmado pelo cliente ou sistema, aguardando separação pelo operador.

### `OUT_FOR_DELIVERY`

Pedido despachado para entrega com o motoboy.

### `COMPLETED`

Pedido entregue ao cliente e finalizado com sucesso.

### `CANCELLED`

Pedido cancelado pelo cliente ou pelo estabelecimento.

---

# 6. Tabela de Estados

| Status             | Descrição                                            | Etapa         |
| ------------------ | ---------------------------------------------------- | ------------- |
| `PENDING`          | Pedido recebido e aguardando validação ou fechamento | Recebimento   |
| `APPROVED`         | Pedido confirmado e aguardando separação             | Processamento |
| `OUT_FOR_DELIVERY` | Pedido enviado para entrega                          | Entrega       |
| `COMPLETED`        | Pedido entregue e finalizado                         | Finalizado    |
| `CANCELLED`        | Pedido cancelado                                     | Encerrado     |

---

# 7. Fluxo Principal do Pedido

O fluxo esperado para um pedido confirmado é:

```text
┌─────────────┐
│   PENDING   │
│             │
│ Pedido      │
│ recebido    │
└──────┬──────┘
       │
       │ Confirmação
       ▼
┌─────────────┐
│  APPROVED   │
│             │
│ Pedido      │
│ confirmado  │
└──────┬──────┘
       │
       │ Despacho
       ▼
┌─────────────────────┐
│  OUT_FOR_DELIVERY   │
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

# 8. Fluxo de Cancelamento

O pedido pode ser cancelado durante o processo, conforme as regras de negócio da aplicação.

### A partir de `PENDING`

```text
PENDING
   │
   │ Cancelamento
   ▼
CANCELLED
```

### A partir de `APPROVED`

```text
APPROVED
   │
   │ Cancelamento
   ▼
CANCELLED
```

Representação consolidada:

```text
                    ┌─────────────┐
                    │   PENDING   │
                    └──────┬──────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             │ Confirmação               │ Cancelamento
             ▼                           ▼
      ┌─────────────┐             ┌─────────────┐
      │  APPROVED   │             │  CANCELLED  │
      └──────┬──────┘             └─────────────┘
             │
             │ Despacho
             ▼
      ┌─────────────────────┐
      │  OUT_FOR_DELIVERY   │
      └──────────┬──────────┘
                 │
                 │ Entrega
                 ▼
          ┌─────────────┐
          │  COMPLETED  │
          └─────────────┘
```

---

# 9. Resumo da Arquitetura

A arquitetura do projeto segue o padrão de **Monólito Modular**, mantendo separação clara entre as responsabilidades.

```text
                         ┌─────────────────┐
                         │    WhatsApp     │
                         └────────┬────────┘
                                  │
                                  │ Mensagem
                                  ▼
                         ┌─────────────────┐
                         │ FastAPI Webhook │
                         │                 │
                         │ POST            │
                         │ /whatsapp/     │
                         │ webhook         │
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
                         │                 │
                         │ Acesso aos      │
                         │ dados          │
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

# 10. Arquitetura do Painel Administrativo

O painel administrativo utiliza uma aplicação frontend simples, sem framework JavaScript, consumindo a API REST do backend.

```text
┌──────────────────────────────┐
│      Admin Frontend          │
│                              │
│ HTML5                        │
│ Tailwind CSS                 │
│ Vanilla JavaScript           │
└───────────────┬──────────────┘
                │
                │ HTTP / REST
                ▼
┌──────────────────────────────┐
│        FastAPI Admin         │
│                              │
│ GET                          │
│ /admin/orders/               │
│                              │
│ PATCH                        │
│ /admin/orders/{order_id}/    │
│ status                       │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│     PostgreSQL / Supabase    │
│                              │
│       schema: delivery       │
└──────────────────────────────┘
```

---

# 11. Sincronização do Painel

O frontend administrativo deve utilizar **polling automático** para consultar periodicamente a API e manter os pedidos atualizados.

Fluxo:

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
      │
      │ Atualização da interface
      ▼
   Lista de pedidos
```

O polling deve permitir que alterações realizadas no backend sejam refletidas automaticamente no painel administrativo.

---

# 12. Princípios Arquiteturais

O projeto deve seguir os seguintes princípios:

* **Separação de responsabilidades**
* **Baixo acoplamento entre módulos**
* **Alta coesão**
* **Regras de negócio concentradas nos Services**
* **Acesso ao banco concentrado nos Repositories**
* **Routers responsáveis pela camada HTTP**
* **Contratos de API bem definidos**
* **Persistência utilizando PostgreSQL**
* **Uso do schema `delivery`**
* **Frontend desacoplado do backend**
* **Comunicação através de API REST**

---

# 13. Resumo Técnico

| Componente          | Tecnologia                    |
| ------------------- | ----------------------------- |
| Backend             | FastAPI                       |
| Linguagem           | Python 3.11+                  |
| Arquitetura         | Monólito Modular              |
| API                 | REST                          |
| Banco de Dados      | PostgreSQL                    |
| Plataforma de Banco | Supabase                      |
| Schema              | `delivery`                    |
| Frontend Admin      | HTML5                         |
| Estilização         | Tailwind CSS                  |
| JavaScript          | Vanilla JavaScript            |
| Sincronização       | Polling automático            |
| Camadas             | Router → Service → Repository |

---

# 14. Endpoints Principais

| Método  | Endpoint                          | Responsabilidade              |
| ------- | --------------------------------- | ----------------------------- |
| `POST`  | `/whatsapp/webhook`               | Receber mensagens do WhatsApp |
| `GET`   | `/admin/orders/`                  | Listar pedidos                |
| `PATCH` | `/admin/orders/{order_id}/status` | Atualizar status do pedido    |

---

# 15. Status Permitidos

Os status utilizados pelo domínio de pedidos são:

```text
PENDING
APPROVED
OUT_FOR_DELIVERY
COMPLETED
CANCELLED
```

Fluxo principal:

```text
PENDING
   ↓
APPROVED
   ↓
OUT_FOR_DELIVERY
   ↓
COMPLETED
```

Fluxo de cancelamento:

```text
PENDING ──────────► CANCELLED

APPROVED ─────────► CANCELLED
```

---

## 16. Objetivo das SPECs

Este documento define as **especificações técnicas e comportamentais** do projeto **Bar do Jaum**, servindo como referência para:

* Desenvolvimento do backend.
* Desenvolvimento do painel administrativo.
* Definição dos contratos da API.
* Implementação das regras de negócio.
* Implementação da máquina de estados dos pedidos.
* Integração com o WhatsApp.
* Persistência dos dados.
* Evolução da arquitetura.
* Validação das decisões técnicas registradas nos ADRs.

As decisões arquiteturais que justificam as escolhas descritas neste documento devem ser registradas no arquivo **`ADRs.md`**.
