# Sis-Ótica — Modelagem do Sistema e Requisitos

> Documento gerado a partir da inspeção real do código-fonte do repositório
> `santosgv/Sis-Otica` (branch `main`). Reflete o que **existe e está implementado**,
> não um planejamento — funcionalidades futuras são marcadas explicitamente como tal.

## 1. Visão Geral

Sistema de gestão para ótica: controle de Ordens de Serviço (OS), clientes, estoque de
produtos, financeiro (caixa, contas a receber/pagar), folha de colaboradores (comissão/
desconto) e notificações automáticas via WhatsApp.

## 2. Arquitetura Técnica

| Item | Valor |
|---|---|
| Framework | Django 5.2.4 |
| Linguagem | Python 3.x |
| Banco de dados | SQLite (ambiente de desenvolvimento) |
| Autenticação | Model de usuário customizado (`Autenticacao.USUARIO`), via `AUTH_USER_MODEL` |
| Auditoria | `django-simple-history` (histórico de alterações campo a campo) |
| API | Django REST Framework + `djangorestframework_simplejwt` (JWT) |
| Frontend | Django Templates + Bootstrap 5 + Font Awesome + JavaScript vanilla (drag-and-drop nativo, HTML5 `dragstart`/`drop`) |
| Timezone | `America/Sao_Paulo`, `USE_TZ=True` |
| Idioma | `pt-br` |
| Multi-tenant | Dependência `django_tenants` presente, mas **desativada** em `settings.py` (`SHARED_APPS`/`TENANT_APPS` comentados) — sistema roda hoje em modo single-tenant |

### 2.1 Apps Django

```
Backend/
├── Autenticacao/    → Usuário customizado, folha (comissão/desconto)
├── Core/            → Núcleo do negócio: clientes, OS, estoque, caixa legado
├── Financeiro/      → Módulo financeiro novo (contas a receber/pagar, caixa, estornos)
├── integracoes/     → Notificações via WhatsApp (Evolution API)
├── Cliente/         → Multi-tenant (django_tenants) — (branch Saas)
├── api/             → Reservado para endpoints DRF (estrutura mínima)
├── xml_nfe/         → Armazenamento de XMLs de Nota Fiscal Eletrônica importados
└── Sis/             → Configuração raiz do projeto
```

## 3. Modelagem de Dados

### 3.1 App `Autenticacao`

**`USUARIO`** (estende `AbstractUser` do Django)
| Campo | Tipo | Observação |
|---|---|---|
| `CPF` | CharField | opcional |
| `DATA_NASCIMENTO` | DateField | opcional |
| `STATUS` | choice | Ativo / Férias / Inativo |
| `FUNCAO` | choice | Vendedor (V) / Caixa (C) / Gerente (G) — usado em regras de permissão de tela nos templates |
| `salario_bruto`, `comissao_percentual`, `valor_hora` | FloatField | usados no cálculo de folha |
| `data_contratacao` | DateField | |

**`Ativacao`** — token de ativação de conta (`user` FK, `token`, `ativo`).

**`Desconto`** — desconto aplicado a um colaborador (`colaborador` FK, `tipo`, `percentual`); `calcular_valor()` = `salario_bruto * percentual/100`.

**`Comissao`** — comissão de vendas por período (`colaborador` FK, `valor_vendas`, `data_referencia`, `horas_extras`); calcula comissão, horas extras (1,5x) e salário líquido agregando os descontos do colaborador.

### 3.2 App `Core`

**`CLIENTE`** — cliente da ótica. `NOME`, `LOGRADOURO`, `CEP`, `NUMERO`, `BAIRRO`, `CIDADE`, `TELEFONE`, `CPF`, `DATA_NASCIMENTO`, `EMAIL`, `FOTO`, `STATUS` (Ativo/Inativo).

**`SERVICO`** / **`LABORATORIO`** — cadastros simples (`nome`, `ATIVO`), referenciados pela OS.

**`ORDEN`** (Ordem de Serviço) — entidade central do sistema.
- Ciclo de vida via `STATUS`: `A` (Solicitado) → `L` (Laboratório) → `J` (Loja) → `E`
  (Entregue) / `F` (Finalizado) / `C` (Cancelado) — visualizado como quadro Kanban com
  drag-and-drop.
- Dados de venda: `VALOR`, `ENTRADA` (texto livre, parseado como decimal em runtime),
  `VALOR_PAGO`, `QUANTIDADE_PARCELA`, `FORMA_PAG`.
- Dados clínicos/óticos: grau de cada olho (`OD_ESF/CIL/EIXO`, `OE_ESF/CIL/EIXO`), `AD`,
  `DNP`, `P`, `DPA`, `DIAG`, `V`, `H`, `ALT`.
- Dados de produto: `ARM`, `MONTAGEM`, `LENTES`, `ARMACAO` (texto livre).
- `ANEXO`/`ASSINATURA` — upload de imagem.
- Auditoria completa via `simple_history` (`HistoricalORDEN`).
- Método `solicitar_avaliacao()` — indica se o cliente ainda não avaliou (`Review`) uma
  OS já entregue.

**`CAIXA`** (legado) — lançamento de caixa vinculado opcionalmente a uma `ORDEN`
(`REFERENCIA`). `TIPO` (Entrada/Saída), `VALOR` (**`Decimal`**), `FORMA` de pagamento, 
flags `ABERTO`/`FECHADO` usadas tanto para o
lançamento quanto para representar abertura/fechamento do dia.

**`ParcelaOrdem`** — parcelamento de uma `ORDEN`. `numero`, `data_vencimento`, `valor`
(Decimal), `pago`, `data_pagamento`, `forma_pagamento`, FK opcional para `CAIXA`.

**`Fornecedor`**, **`TipoUnitario`**, **`Estilo`**, **`Tipo`** — cadastros auxiliares de
estoque.

**`Produto`** — item de estoque. Código gerado automaticamente no `save()`
(`{nome}-{iniciais do fornecedor}-{UNIDADE}{ids}`), `preco_unitario`, `preco_venda`,
`quantidade`, `quantidade_minima`, `valor_total` (calculado). Suporta importação de NFe
(`importado`, `conferido`, `chavenfe`).

**`EntradaEstoque`** / **`SaidaEstoque`** / **`MovimentoEstoque`** — histórico de
movimentação de estoque por produto.

**`AlertaEstoque`** — alerta de estoque baixo (`produto`, `mensagem`, `lido`).

**`Review`** — avaliação do cliente pós-entrega (`cliente` FK, `nota` 1-5, `comentario`).

### 3.3 App `Financeiro`

Módulo financeiro completo, construído como **camada adicional sobre o `Core`** — nunca
altera o schema do `Core`; toda integração é via Foreign Key apontando do `Financeiro`
para `Core` (nunca o contrário).

| Model | Papel |
|---|---|
| `ContaFinanceira` | Caixa/banco/PIX — saldo sempre derivado dos movimentos, nunca armazenado direto |
| `CategoriaFinanceira` | Categoria hierárquica (receita/despesa), `categoria_pai` |
| `CentroCusto` | Centro de custo |
| `MovimentoFinanceiro` | Lançamento central — tipos: entrada, saída, transferência, estorno, ajuste, sangria, suprimento; auditado via `simple_history` |
| `RecebimentoParcela` | Liga uma `Core.ParcelaOrdem` a um `MovimentoFinanceiro` — permite recebimento parcial rastreado |
| `ContaPagar` / `ParcelaContaPagar` / `PagamentoParcelaContaPagar` | Espelham a estrutura de contas a receber, do lado de despesas/fornecedores |
| `FechamentoCaixa` | Um registro por abertura/fechamento de caixa, com conferência `saldo_esperado` x `saldo_contado` |
| `EstornoFinanceiro` | Liga um movimento ao seu inverso — nunca apaga o original |

Possui Service Layer dedicado (`services.py`, `relatorios.py`) com toda a regra de
negócio (nenhuma lógica financeira em views/templates), views/templates próprias
(dashboard, contas a receber, contas a pagar, caixa) e testes automatizados.

### 3.4 App `integracoes` (WhatsApp)

**`WhatsAppConfig`** — configuração única da instância WhatsApp (via Evolution API):
`instance_name`, `numero_vinculado`, `ativo`, toggles de notificação
(`notif_os_criada`, `notif_troca_status`, `notif_os_entregue`, `notif_cancelamento`,
`notif_lembrete_anual`), contadores de envio. Consulta o estado de conexão **ao vivo** na
Evolution API (não armazenado em banco).

**`LembreteAnualEnviado`** — controla envio único do lembrete anual por OS/ciclo, para o
job periódico não reenviar repetidamente.

Alertas disparados automaticamente via signal (`post_save` em `Core.ORDEN`, detectando
transição real de status) e manualmente via view de reenvio.

## 4. Requisitos Funcionais

### RF01 — Gestão de Clientes
Cadastrar, listar, editar clientes com dados pessoais, foto e endereço. Cliente pode
avaliar (1-5 estrelas + comentário) uma OS após entrega.

### RF02 — Gestão de Ordens de Serviço
Criar OS vinculada a cliente, vendedor, serviço e laboratório, com dados de receita
óptica completos, valor, forma de pagamento e parcelamento. Acompanhar via quadro Kanban
com mudança de status por arrastar-e-soltar (`A → L → J → E`, ou `C` para cancelamento).
Anexar imagem e assinatura do cliente. Gerar PDF/carnê de pagamento.

### RF03 — Parcelamento de OS
Dividir o valor da OS em N parcelas com vencimentos, registrar pagamento (integral ou
parcial) de cada parcela.

### RF04 — Controle de Caixa (legado, `Core`)
Abrir/fechar caixa do dia, registrar entradas/saídas manuais, vincular lançamento a uma
OS.

### RF05 — Módulo Financeiro (`Financeiro`)
Contas financeiras múltiplas (caixa/banco/PIX), categorias e centros de custo, contas a
receber (integradas às parcelas de OS) e a pagar (fornecedores/despesas), com:
- Recebimento/pagamento parcial, rejeitando valor que exceda o saldo em aberto.
- Estorno que preserva o lançamento original e cria o inverso, nunca apaga histórico.
- Estorno automático de valores recebidos quando uma OS é cancelada.
- Abertura/fechamento de caixa com conferência de saldo esperado x contado (exige motivo
  se houver diferença).
- Sangria e suprimento como tipos de movimento próprios (nunca contam como
  despesa/receita operacional).
- Dashboard com indicadores (saldo, entradas/saídas do dia e mês, total a
  receber/pagar/vencido, próximos vencimentos).
- Relatórios de fluxo de caixa (realizado e projetado), contas a receber/pagar por
  status, receitas/despesas por categoria/cliente/fornecedor/centro de custo.

### RF06 — Gestão de Estoque
Cadastrar produtos (com fornecedor, tipo, estilo), controlar entrada/saída/movimentação,
alertar quando quantidade abaixo do mínimo. Suporta importação de dados a partir de XML
de Nota Fiscal Eletrônica.

### RF07 — Gestão de Colaboradores/Folha
Cadastrar colaborador com função (vendedor/caixa/gerente), calcular comissão sobre
vendas, horas extras e descontos, apurar salário líquido.

### RF08 — Notificações via WhatsApp
Configurar e conectar uma instância WhatsApp (Evolution API/QR code). Enviar
automaticamente: confirmação de OS criada, troca de status (laboratório/pronto para
retirada), aviso de entrega, aviso de cancelamento — cada um controlável
individualmente. Enviar lembrete anual de exame de vista (job periódico). Permitir
reenvio manual de qualquer alerta.

### RF09 — Autenticação e Ativação de Conta
Login customizado, ativação de conta por token, redefinição de senha.

## 5. Requisitos Não Funcionais

### RNF01 — Persistência de dinheiro
Valores monetários devem ser `DecimalField`, nunca `float`, para evitar erro de
arredondamento. **Estado atual: parcialmente atendido** — `Core.ORDEN.VALOR`,
`ParcelaOrdem.valor` e todo o `Financeiro` já usam Decimal; `Core.CAIXA.VALOR` e os
campos monetários de `Autenticacao` (`salario_bruto`, `comissao_percentual`,
`valor_hora`) ainda são `FloatField` — débito técnico conhecido, não corrigido para não
alterar schema do `Core` fora do escopo combinado.

### RNF02 — Auditoria
Toda alteração em `ORDEN` e nos models centrais do `Financeiro` deve ser rastreável
(quem, quando, valor antes/depois) via `django-simple-history`. Atendido para `ORDEN` e a
maior parte do `Financeiro`; não atendido para `ParcelaOrdem`, `CAIXA` e os models de
`Autenticacao`.

### RNF03 — Integridade financeira
Nenhuma operação financeira deve deixar o sistema em estado inconsistente (parcela
marcada como paga sem movimento correspondente, ou vice-versa). Atendido no `Financeiro`
via `transaction.atomic()` em toda operação de baixa/estorno/fechamento.

### RNF04 — Concorrência
Duas baixas simultâneas da mesma parcela não podem ambas ter sucesso. Implementado via
`select_for_update()` no `Financeiro`. **Ressalva:** validado apenas contra SQLite (onde
o lock de linha é no-op — a proteção observada vem do lock de arquivo do SQLite);
recomendação de revalidar contra PostgreSQL antes de produção.

### RNF05 — Resiliência de integrações externas
Falha na Evolution API (WhatsApp) não pode impedir a operação principal (salvar a OS).
Atendido — o signal de notificação captura todas as exceções e apenas loga, nunca
propaga.

### RNF06 — Autenticação obrigatória
Toda tela do sistema exige login (`@login_required`), exceto login/ativação/recuperação
de senha.

### RNF07 — Idioma e fuso horário
Interface e formatação de data/hora em português do Brasil, fuso `America/Sao_Paulo`.

### RNF08 — Auditabilidade de testes
Funcionalidades novas (módulo `Financeiro`) devem ter suíte de testes automatizados
cobrindo regras de negócio, casos extremos e regressão. Não atendido uniformemente nos
apps mais antigos (`Core`/`Autenticacao`/`integracoes` têm cobertura parcial).

## 6. Regras de Negócio Relevantes

- Uma OS cancelada (`STATUS='C'`) tem suas parcelas não pagas removidas automaticamente;
  parcelas já pagas são preservadas (nunca apagar histórico financeiro).
- Excedente em recebimento/pagamento de parcela é **rejeitado**, não gera crédito.
- Sangria/suprimento nunca são contabilizados como despesa/receita operacional nos
  relatórios.
- Fechamento de caixa com diferença entre esperado e contado exige motivo obrigatório.
- Categoria financeira em uso não pode ser excluída fisicamente (`PROTECT`).
- Cada conta financeira só pode ter um caixa aberto por vez (`UniqueConstraint` no
  banco, não só validação de aplicação).

## 7. Limitações e Débitos Técnicos Conhecidos

- Multi-tenant (`django_tenants`) presente como dependência mas desativado — sistema
  single-tenant hoje.
- Duas fontes de dados de caixa coexistindo: `Core.CAIXA` (legado, usado pela tela
  `/Caixa` original) e `Financeiro.MovimentoFinanceiro` (fonte da verdade do módulo
  novo, tela própria em `/financeiro/caixa/`) — ponte de escrita dupla mantida até uma
  decisão de unificação.
- Permissões granulares (`receive_payment`, `open_cash` etc.) definidas no
  `Financeiro` mas não conectadas às views — todo usuário autenticado acessa tudo.
- Sem API REST pública para o módulo `Financeiro` (só views HTML server-rendered).
- `app api/` existe na estrutura de pastas mas não está registrado em `INSTALLED_APPS`.