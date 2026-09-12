# ADRs — Arquitetura e Decisões de Projeto

## Projeto: Bar do Jaum

Este documento registra as principais decisões arquiteturais e técnicas tomadas durante o desenvolvimento do **Delivery do Bar do Jaum**.

O objetivo dos ADRs (*Architecture Decision Records*) é documentar não apenas **qual decisão foi tomada**, mas também o **contexto, as alternativas consideradas e as consequências** dessa decisão.

---

## ADR 01: Adoção de Monólito Modular em FastAPI vs. Microsserviços

**Status:** Aceito

### Contexto

O projeto precisa evoluir rapidamente mantendo uma arquitetura organizada, testável e de fácil manutenção.

A adoção prematura de microsserviços adicionaria complexidade operacional, incluindo comunicação entre serviços, observabilidade distribuída, gerenciamento de deploys e maior necessidade de infraestrutura.

### Alternativas

* Microsserviços distribuídos.
* Monólito tradicional sem separação de responsabilidades.
* Monólito modular organizado em camadas.

### Decisão

Adotar um **monólito modular em FastAPI**, estruturado seguindo a separação:

```text
Router
   ↓
Service
   ↓
Repository
   ↓
Database
```

Os principais componentes são isolados por responsabilidade, permitindo evolução independente dentro do mesmo processo de aplicação.

### Consequências

**Positivas:**

* Redução da complexidade de infraestrutura.
* Deploy simplificado.
* Menor overhead de comunicação entre componentes.
* Facilidade de desenvolvimento e testes.
* Separação clara entre regras de negócio e persistência.
* Possibilidade de futura extração de módulos para serviços independentes.

**Negativas:**

* Escalabilidade inicialmente concentrada na aplicação.
* Falhas críticas podem afetar o processo principal.
* Uma futura migração para microsserviços exigirá definição adicional de contratos entre módulos.

---

# ADR 02: Catálogo Relacional como Fonte de Verdade para Produtos

**Status:** Aceito

### Contexto

O agente precisa consultar produtos, preços, disponibilidade e estoque durante a conversa.

Essas informações possuem caráter transacional e não podem depender da memória ou da geração probabilística de um LLM.

O principal requisito é impedir que o agente invente produtos, preços ou quantidades disponíveis.

### Alternativas

* Utilizar uma base vetorial com embeddings para recuperação do catálogo.
* Utilizar RAG para recuperar informações de produtos.
* Consultar diretamente o catálogo relacional no PostgreSQL.
* Combinar RAG com consultas relacionais.

### Decisão

Utilizar o **PostgreSQL como fonte oficial de verdade para o catálogo e estoque**.

O LLM pode interpretar a intenção do cliente e sugerir produtos, mas a validação definitiva deve ser realizada pelo código determinístico.

O fluxo adotado é:

```text
Mensagem do cliente
        ↓
LLM / Classifier
        ↓
Produto identificado
        ↓
PostgreSQL
        ↓
Disponibilidade + preço + estoque
        ↓
Resposta ao cliente
```

O LLM **não calcula preços, não define estoque e não inventa disponibilidade**.

### Consequências

**Positivas:**

* Preços provenientes diretamente da fonte transacional.
* Estoque consultado em tempo real.
* Redução do risco de alucinação de catálogo.
* Menor latência para consultas estruturadas.
* Menor complexidade de infraestrutura.
* Não há necessidade de manter um índice vetorial para informações transacionais.

**Negativas:**

* Consultas semânticas complexas exigem tratamento adicional.
* O catálogo precisa possuir uma estratégia adequada de busca textual.
* O LLM continua sujeito a erros na interpretação da intenção ou do nome do produto.

---

# ADR 03: Vínculo de Mensagens por Telefone e Associação Tardia de Pedidos

**Status:** Aceito

### Contexto

A conversa no WhatsApp começa antes de o pedido existir formalmente.

O cliente pode enviar diversas mensagens antes de informar todos os dados necessários para a criação do pedido.

Por esse motivo, as mensagens iniciais não podem depender exclusivamente de um `order_id`.

### Alternativas

* Salvar mensagens somente associadas a `order_id`.
* Criar o pedido imediatamente no início da conversa.
* Utilizar uma sessão identificada pelo telefone do cliente e associar o pedido posteriormente.

### Decisão

Utilizar o **`customer_phone` como identificador da sessão conversacional**, mantendo o `order_id` inicialmente nulo.

Quando o pedido for efetivamente criado, o `order_id` passa a ser associado à sessão e às informações correspondentes.

Fluxo:

```text
WhatsApp
   ↓
customer_phone
   ↓
Customer Session
   ↓
Mensagens / Estado da conversa
   ↓
Criação do pedido
   ↓
order_id associado
```

### Consequências

**Positivas:**

* Permite iniciar a conversa sem pedido previamente criado.
* Preserva o histórico desde o primeiro contato.
* Facilita a recuperação do estado conversacional.
* Permite associar posteriormente a conversa ao pedido.
* Melhora a rastreabilidade e auditoria.

**Negativas:**

* O telefone precisa ser tratado como identificador consistente.
* É necessário controlar sessões expiradas.
* A associação entre sessão e pedido precisa ser realizada de maneira determinística.

---

# ADR 04: Aprovação Humana Obrigatória — Human-in-the-Loop

**Status:** Aceito

### Contexto

O agente pode interpretar mensagens, montar o carrinho e coletar os dados necessários para a entrega.

Entretanto, o projeto não deve permitir que uma decisão automatizada incorreta resulte diretamente no despacho de um pedido.

O objetivo é manter uma etapa de supervisão humana antes da liberação operacional.

### Alternativas

* Automação completa de ponta a ponta.
* Aprovação humana opcional.
* Aprovação humana obrigatória antes do processamento do pedido.

### Decisão

Adotar **Human-in-the-Loop obrigatório**.

Todo pedido completo deve entrar em um estado de aprovação antes de ser liberado para processamento.

Fluxo:

```text
Cliente
   ↓
Agente IA
   ↓
Pedido completo
   ↓
Aguardando aprovação
   ↓
Painel administrativo
   ├── Aprovar → Processar pedido
   └── Rejeitar → Cancelar pedido
```

A aprovação deve ser realizada explicitamente pela equipe através do painel administrativo.

### Consequências

**Positivas:**

* Redução do risco operacional.
* Supervisão humana antes da execução.
* Maior controle sobre pedidos e pagamentos.
* Possibilidade de intervenção em situações excepcionais.
* Auditoria da decisão de aprovação.

**Negativas:**

* O processamento depende da disponibilidade da equipe.
* Pode aumentar o tempo total de atendimento.
* Exige um painel administrativo funcional.
* Introduz uma etapa adicional no workflow.

---

# ADR 05: Separação entre Inteligência Probabilística e Regras Determinísticas

**Status:** Aceito

### Contexto

O sistema utiliza LLM para compreender linguagem natural. Entretanto, algumas operações possuem impacto direto no negócio e não devem depender de comportamento probabilístico.

Preço, estoque, cálculo do pedido, validações e transações precisam produzir resultados previsíveis.

### Alternativas

* Permitir que o LLM execute diretamente regras de negócio.
* Utilizar o LLM para decidir todas as etapas do workflow.
* Separar interpretação de linguagem das regras determinísticas.

### Decisão

Adotar uma separação explícita de responsabilidades:

```text
LLM
│
├── Conversar
├── Interpretar intenção
├── Extrair entidades
└── Sugerir itens
        │
        ▼
Código Determinístico
│
├── Consultar estoque
├── Validar produtos
├── Calcular valores
├── Validar dados
├── Criar pedido
├── Atualizar estado
└── Registrar transações
```

O LLM atua como camada de **interpretação**, enquanto Python/FastAPI controla a **execução das regras de negócio**.

### Consequências

**Positivas:**

* Maior previsibilidade.
* Redução de decisões críticas tomadas pelo LLM.
* Maior facilidade de testes automatizados.
* Regras de negócio centralizadas no código.
* Maior segurança para operações financeiras e de estoque.

**Negativas:**

* Maior quantidade de código determinístico.
* Necessidade de definir contratos claros entre LLM e aplicação.
* Algumas conversas exigem tratamento adicional para transformar linguagem natural em ações estruturadas.

---

# ADR 06: Workflow Determinístico com Máquina de Estados

**Status:** Aceito

### Contexto

Um agente conversacional pode receber informações fora de ordem.

Por exemplo, o cliente pode informar produtos antes do nome, endereço antes do pagamento ou enviar todos os dados em uma única mensagem.

Um fluxo baseado exclusivamente em prompts poderia produzir comportamentos inconsistentes.

### Alternativas

* Fluxo controlado exclusivamente pelo LLM.
* Workflow baseado em agentes autônomos.
* Máquina de estados determinística.

### Decisão

Utilizar uma **máquina de estados explícita** para controlar o ciclo de vida do atendimento.

Estados principais:

```text
INITIAL
   ↓
COLLECTING_ORDER
   ↓
AWAITING_DELIVERY_DATA
   ↓
AWAITING_PAYMENT
   ↓
AWAITING_CONFIRMATION
   ↓
AWAITING_HUMAN_APPROVAL
   ├── COMPLETED
   └── CANCELLED
```

O LLM interpreta a mensagem, mas o workflow determina qual transição pode ocorrer.

### Consequências

**Positivas:**

* Comportamento previsível.
* Transições auditáveis.
* Facilidade de testes.
* Menor dependência do comportamento do LLM.
* Maior controle sobre cenários incompletos ou fora de ordem.

**Negativas:**

* Maior quantidade de estados e regras.
* Necessidade de manutenção das transições.
* Novos fluxos exigem atualização da máquina de estados.

---

# Resumo das decisões

| ADR    | Decisão                           | Objetivo                                |
| ------ | --------------------------------- | --------------------------------------- |
| ADR 01 | Monólito modular FastAPI          | Reduzir complexidade operacional        |
| ADR 02 | PostgreSQL como fonte do catálogo | Garantir dados transacionais confiáveis |
| ADR 03 | Sessão por `customer_phone`       | Preservar conversa antes do pedido      |
| ADR 04 | Human-in-the-Loop obrigatório     | Evitar processamento sem supervisão     |
| ADR 05 | LLM + código determinístico       | Separar interpretação de execução       |
| ADR 06 | Workflow com máquina de estados   | Garantir fluxo previsível               |

---

## Princípio arquitetural central

> **A IA entende o que o cliente quer. O código determina o que o sistema pode fazer.**

Essa separação é o principal princípio arquitetural do **Delivery do Bar do Jaum**.
