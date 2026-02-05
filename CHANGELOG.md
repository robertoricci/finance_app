# 🚀 CHANGELOG

## ✨ Versão 1.6 - Acompanhamento de Orçamento Não Utilizado

### 💰 Nova Tela: Visualização de Saldo Disponível

Implementação de uma visão completa para acompanhar o orçamento planejado vs utilizado, mostrando claramente o que ainda está disponível.

#### 🎯 Objetivo
Responder às perguntas:
- "Quanto do meu orçamento eu já usei?"
- "Quanto ainda tenho disponível para gastar?"
- "Quais categorias ainda têm saldo?"
- "Em quais meses economizei mais?"

---

### 📊 Funcionalidades Implementadas

#### 1️⃣ Resumo Anual

**4 KPIs Principais:**
- 💰 Total Planejado (ano)
- 💸 Total Utilizado (ano)
- 💵 Total Disponível (ano)
- 📊 % Utilizado (ano)

**Análise Automática:**
- ✅ Quantos meses com saldo disponível
- ⚠️ Quantos meses estouraram
- 💡 Quantos meses sem orçamento

---

#### 2️⃣ Gráfico: Disponível vs Utilizado

**Tipo:** Barras Empilhadas por Mês

**Visualização:**
- 🔴 Parte inferior: Utilizado
- 🟢 Parte superior: Disponível
- 📊 Altura total = Orçamento planejado

**Interpretação Visual:**
- Barra toda vermelha = Gastou tudo
- Barra com muito verde = Muita economia
- Barra maior que planejado = Estourou

---

#### 3️⃣ Detalhamento Mês a Mês (12 Abas)

**Para cada mês:**

**KPIs do Mês:**
- Planejado
- Utilizado (com % do total)
- Disponível (com indicador de cor)
- Barra de progresso visual

**Gráfico de Barras Horizontais:**
- Barra azul clara: Orçamento planejado (fundo)
- Barra colorida: Valor utilizado (frente)
  - 🟢 Verde: Dentro do orçamento
  - 🔴 Vermelho: Estourou o orçamento

**Tabela Detalhada por Categoria:**
- Categoria
- Planejado
- Utilizado
- Disponível
- % Usado
- Status (🟢 Disponível / 🔴 Estourou / ⚖️ Exato)

**Alertas Inteligentes:**
- ⚠️ Lista categorias que estouraram
- ✅ Mostra saldo disponível total
- 💰 Top 3 categorias com maior saldo

---

#### 4️⃣ Insights e Recomendações

**Melhores Meses:**
- Top 3 meses com mais saldo disponível
- Valores e percentuais

**Meses de Atenção:**
- Top 3 meses que estouraram
- Ou que usaram quase tudo (>95%)

**Recomendações Automáticas:**

**Se tem saldo positivo:**
- ✅ Parabeniza pelo controle
- 💡 Sugere investir o excedente
- 📊 Mostra percentual economizado

**Se estourou:**
- ⚠️ Alerta sobre o estouro
- 📝 Lista ações recomendadas
- 🎯 Sugere revisão de categorias

---

### 📍 Como Acessar

**Menu Lateral → 💰 Acompanhamento**

Localização no sistema:
1. Faça login
2. No menu lateral, clique em "💰 Acompanhamento"
3. Selecione o ano
4. Visualize:
   - Resumo anual
   - Gráfico consolidado
   - Abas mês a mês (12 meses)
   - Insights e recomendações

---

### 🎨 Características Visuais

**Sistema de Cores:**
- 🟢 Verde: Saldo disponível / Dentro do orçamento
- 🔴 Vermelho: Utilizado / Estourou orçamento
- 🔵 Azul: Planejado (fundo)
- 🟡 Amarelo: Alertas gerais

**Elementos Interativos:**
- Tabs para cada mês
- Gráficos com hover detalhado
- Tabelas com scroll
- Expandir/colapsar seções

**Formatação:**
- Todos os valores em R$
- Percentuais com 1 casa decimal
- Barras de progresso visuais
- Status com emojis

---

### 💡 Casos de Uso

#### Cenário 1: Planejamento de Gastos
```
Situação: É dia 15 e você quer saber quanto ainda pode gastar

Ação:
1. Acessar "Acompanhamento"
2. Ir na aba do mês atual
3. Ver "Disponível" por categoria

Resultado:
"Alimentação: R$ 400 disponíveis
Lazer: R$ 150 disponíveis"
→ Pode gastar até esses valores
```

#### Cenário 2: Identificar Economia
```
Situação: Quer saber em quais meses economizou

Ação:
1. Ver seção "Melhores Meses"
2. Identificar top 3

Resultado:
"Junho: R$ 800 disponíveis
Maio: R$ 650 disponíveis
Março: R$ 500 disponíveis"
→ Padrão de economia identificado
```

#### Cenário 3: Revisar Categoria Problemática
```
Situação: Sempre estoura "Alimentação"

Ação:
1. Ver detalhamento mês a mês
2. Verificar categoria em cada mês

Resultado:
"Jan: Estourou R$ 200
Fev: Estourou R$ 150
Mar: Estourou R$ 300"
→ Precisa ajustar orçamento desta categoria
```

#### Cenário 4: Realocação de Orçamento
```
Situação: Tem saldo em uma categoria, precisa em outra

Ação:
1. Ver "Top 3 categorias com maior saldo"
2. Identificar onde tem sobra

Resultado:
"Lazer: R$ 300 não utilizados
Saúde: R$ 200 não utilizados"
→ Pode realocar ou economizar para próximo mês
```

---

### 🎯 Benefícios

**Controle Financeiro:**
- ✅ Visão clara do que ainda pode gastar
- ✅ Evita estourar orçamento
- ✅ Identifica categorias problemáticas

**Planejamento:**
- 📊 Histórico completo do ano
- 📈 Padrões de consumo identificados
- 🎯 Metas de economia acompanhadas

**Tomada de Decisão:**
- 💡 Insights automáticos
- ⚠️ Alertas proativos
- 📝 Recomendações práticas

**Transparência:**
- 👁️ Tudo visível e claro
- 📊 Múltiplas visualizações
- 📋 Dados detalhados

---

### 📊 Integração com Sistema

**Dados Utilizados:**
- Orçamentos (tabela `orcamentos_mensais`)
- Lançamentos (tabela `lancamentos`)
- Categorias (tabela `categorias`)

**Cálculos:**
```
Disponível = Planejado - Utilizado
% Utilizado = (Utilizado / Planejado) × 100
Status = "Disponível" se Disponível > 0 else "Estourou"
```

**Atualizações:**
- Em tempo real
- Baseado nos lançamentos mais recentes
- Sincronizado com dashboard e planejamento

---

### ✅ Checklist de Uso

- [ ] Defini orçamento para todos os meses?
- [ ] Verifiquei o resumo anual?
- [ ] Identifiquei meses com saldo?
- [ ] Revisei categorias que estouraram?
- [ ] Li as recomendações automáticas?
- [ ] Ajustei orçamento conforme necessário?

---

### 🆕 Diferenciais

**Antes:**
- Precisava calcular manualmente o disponível
- Não sabia quanto podia gastar
- Difícil identificar padrões

**Agora:**
- ✅ Cálculo automático do disponível
- ✅ Visualização clara por mês e categoria
- ✅ Insights e alertas automáticos
- ✅ 12 meses em uma tela
- ✅ Recomendações personalizadas

---

## ✨ Versão 1.5 - KPIs Financeiros Profissionais

### 📊 5 Novos Indicadores na Visão Mensal

Implementação de KPIs com rigor técnico financeiro e visualizações profissionais.

#### KPI 1: Distribuição de Despesas por Categoria
**Objetivo:** Identificar para onde o dinheiro está sendo direcionado

**Fórmula:**
```
Percentual = (Despesas da Categoria / Total de Despesas) × 100
```

**Visualização:** Gráfico de Donut
- Centro mostra total de despesas
- Cada fatia colorida por categoria
- Percentual e valor em cada fatia
- Cores das próprias categorias cadastradas

**Interpretação:**
- ✅ TOP 3 categorias exibidas ao lado
- ⚠️ Alerta se alguma categoria > 40% dos gastos
- 💡 Identifica categorias de maior impacto

---

#### KPI 2: Evolução Mensal de Gastos
**Objetivo:** Analisar tendência dos gastos ao longo do tempo

**Fórmula:**
```
Gastos Mensais = Σ(Despesas) agrupado por mês
```

**Visualização:** Gráfico de Linha com Área Preenchida
- Linha vermelha com marcadores
- Área preenchida semitransparente
- Últimos 6 meses de dados
- Valores em cada ponto

**Interpretação:**
- 📈 Tendência de alta = Perda de controle
- 📉 Tendência de queda = Controle melhorando
- 📊 Média dos 6 meses calculada
- 💰 Variação percentual vs início do período

---

#### KPI 3: Fluxo de Caixa Mensal
**Objetivo:** Comparar entradas e saídas no mesmo período

**Fórmula:**
```
Fluxo de Caixa = Σ(Entradas) - Σ(Saídas)
```

**Visualização:** Barras Agrupadas + Marcador de Saldo
- Barra verde: Entradas
- Barra vermelha: Saídas
- Diamante azul: Saldo resultante
- Valores dentro das barras

**Interpretação:**
- ✅ Superávit: Gastou menos que recebeu
- ⚠️ Déficit: Gastou mais que recebeu
- ⚖️ Equilíbrio: Entradas = Saídas
- 📊 Taxa de economia calculada

---

#### KPI 4: Percentual de Comprometimento da Renda
**Objetivo:** Avaliar quanto da renda está comprometida com despesas

**Fórmula:**
```
Comprometimento (%) = (Σ Saídas / Σ Entradas) × 100
```

**Visualização:** Gauge (Velocímetro)
- Faixas coloridas:
  - 0-50%: Verde (Saudável)
  - 50-70%: Amarelo (Atenção)
  - 70-100%: Vermelho (Risco)
- Ponteiro indica valor atual
- Delta vs referência de 50%

**Interpretação:**
- ✅ 0-50%: Saudável - Excelente controle
- ⚠️ 50-70%: Atenção - Monitore os gastos
- 🔴 70-100%: Risco Alto - Reduza despesas urgente

---

#### KPI 5: Saldo Acumulado
**Objetivo:** Acompanhar evolução do capital ao longo do tempo

**Fórmula:**
```
Saldo Acumulado(t) = Σ(Entradas até t) - Σ(Saídas até t)
```

**Visualização:** Gráfico de Área
- Linha azul com área preenchida
- Últimos 6 meses acumulados
- Linha zero como referência
- Valores em cada mês

**Interpretação:**
- 📈 Crescimento: Capacidade de poupança
- 📉 Queda: Consumo excessivo
- 📊 Taxa de crescimento do período
- 💰 Saldo atual (acumulado 6 meses)

---

### 📋 Localização dos KPIs

**Dashboard → Visão Mensal**

Seção nova: "📊 Indicadores Financeiros Profissionais"

Ordem de exibição:
1. KPI 1: Distribuição de Despesas
2. KPI 2: Evolução Mensal
3. KPI 3: Fluxo de Caixa
4. KPI 4: Comprometimento da Renda
5. KPI 5: Saldo Acumulado

Cada KPI tem:
- ✅ Título e objetivo claro
- ✅ Gráfico profissional
- ✅ Painel de interpretação
- ✅ Métricas complementares
- ✅ Alertas quando aplicável

---

### 💡 Benefícios dos KPIs

#### Para Usuários Leigos
- 📊 Visualizações simples e intuitivas
- 🎨 Sistema de cores (verde/amarelo/vermelho)
- 📝 Interpretação em linguagem clara
- ⚠️ Alertas automáticos

#### Para Usuários Avançados
- 📈 Análise de tendências
- 💰 Métricas financeiras profissionais
- 📊 Comparativos temporais
- 🎯 Benchmarks de referência

#### Para Planejamento
- 🔍 Identifica problemas rapidamente
- 📉 Mostra evolução ao longo do tempo
- 🎯 Estabelece metas claras
- 💡 Sugere áreas de melhoria

---

### 🎯 Casos de Uso

#### Cenário 1: Análise de Gastos
```
KPI 1 mostra: Alimentação = 45%
→ ALERTA! Categoria muito alta
→ Ação: Revisar gastos com alimentação
```

#### Cenário 2: Controle de Tendência
```
KPI 2 mostra: Aumento de 15% nos últimos 6 meses
→ ATENÇÃO! Gastos crescendo
→ Ação: Implementar controle mais rígido
```

#### Cenário 3: Saúde Financeira
```
KPI 4 mostra: 35% de comprometimento
→ SAUDÁVEL! Zona verde
→ Ação: Manter o controle atual
```

---

### ✅ Especificações Técnicas

**Campos do Banco Utilizados:**
- `valor` ✅
- `tipo` (entrada/saída) ✅
- `categoria` ✅
- `data` ✅

**Cálculos Implementados:**
- Agregações por categoria ✅
- Agrupamento temporal ✅
- Cálculos acumulativos ✅
- Percentuais e taxas ✅

**Filtros Aplicáveis:**
- Por mês específico ✅
- Por ano específico ✅
- Últimos 6 meses ✅

**Performance:**
- Queries otimizadas ✅
- Cache de dados ✅
- Renderização eficiente ✅

---

## ✨ Versão 1.4 - Gráficos de Controle Financeiro

### 🎯 Novos Gráficos de Análise

#### 📊 Gráfico: Controle Orçamentário Mensal
**Tipo:** Barras Agrupadas  
**Objetivo:** Comparar visualmente Entradas, Despesas e Orçamento lado a lado

**Mostra:**
- ✅ Barra Verde: Entradas do mês
- ✅ Barra Vermelha: Despesas realizadas
- ✅ Barra Azul tracejada: Orçamento planejado
- ✅ Comparação visual mês a mês

**Indicadores abaixo do gráfico:**
- ⚠️ Quantos meses gastou mais que recebeu
- ⚠️ Quantos meses estourou o orçamento
- 📊 Média de % gasto no ano

#### 📉 Gráfico: Análise de Desvios do Orçamento
**Tipo:** Dois gráficos lado a lado

**Gráfico 1 - Desvios Mensais (Barras):**
- 🟢 Verde (acima do zero): Economizou vs planejado
- 🔴 Vermelho (abaixo do zero): Estourou o orçamento
- 📏 Linha de referência no zero
- 💰 Valores em cada barra

**Gráfico 2 - Pizza de Controle:**
- ✅ Setor Verde: Meses dentro do orçamento
- ⚠️ Setor Vermelho: Meses acima do orçamento
- 🎯 Centro: X/12 meses controlados
- 📊 Percentuais visíveis

**Estatísticas de Desvio (4 cards):**
- 💰 Desvio Total do ano
- ✅ Maior economia (mês)
- ⚠️ Maior estouro (mês)
- 📊 Desvio médio mensal

#### 🚦 Gráfico: Semáforo Financeiro
**Tipo:** Barras coloridas por status  
**Objetivo:** Identificar rapidamente meses problemáticos

**Sistema de Cores:**
- 🔴 **Vermelho**: Gastou mais do que recebeu (saldo negativo)
- 🟡 **Amarelo**: Economizou menos de 10% da renda
- 🟢 **Verde**: Economizou 10% ou mais da renda

**Análise abaixo (3 cards):**
- 🔴 Quantos meses no vermelho (gastando mais)
- 🟡 Quantos meses no amarelo (economia baixa)
- 🟢 Quantos meses no verde (boa economia)

**Cada card mostra:**
- Número de meses naquela faixa
- Status e recomendação
- Emoji de alerta ou sucesso

---

### 💡 Por Que Esses Gráficos São Importantes?

#### 🎯 Controle Orçamentário
**Problema que resolve:**
- "Estou gastando mais do que ganho?"
- "Estou seguindo meu orçamento?"

**Como ajuda:**
- Visualização imediata de 3 métricas lado a lado
- Identifica meses críticos rapidamente
- Mostra se o orçamento está realista

#### 📉 Análise de Desvios
**Problema que resolve:**
- "Em quais meses eu estourei o orçamento?"
- "Quanto estou economizando vs planejado?"

**Como ajuda:**
- Mostra exatamente quanto economizou ou estourou
- Pizza mostra % de controle anual
- Estatísticas detalhadas de performance

#### 🚦 Semáforo Financeiro
**Problema que resolve:**
- "Preciso de uma visão rápida: está bom ou ruim?"
- "Quantos meses estou no vermelho?"

**Como ajuda:**
- Sistema de cores intuitivo (vermelho/amarelo/verde)
- Identifica rapidamente meses problemáticos
- Define meta clara: economizar 10% ou mais

---

### 📊 Total de Gráficos na Visão Anual

Agora você tem **7 gráficos completos:**

1. ✅ Fluxo de Caixa Mensal (Área)
2. ✅ Saldo Mês a Mês (Barras)
3. ✅ Planejado vs Realizado (Linhas)
4. ✅ % de Gastos (Barras Coloridas)
5. ✅ **Controle Orçamentário (Barras Agrupadas)** 🆕
6. ✅ **Análise de Desvios (Barras + Pizza)** 🆕
7. ✅ **Semáforo Financeiro (Barras por Status)** 🆕

---

### 🎯 Como Usar os Novos Gráficos

#### Cenário 1: Identificar Problema
1. Olhe o **Semáforo Financeiro**
2. Veja quantos meses estão no vermelho
3. Se houver meses vermelhos, tome ação imediata

#### Cenário 2: Avaliar Controle Orçamentário
1. Olhe o **Controle Orçamentário**
2. Compare as 3 barras de cada mês
3. Se despesa > entrada: 🔴 Problema
4. Se despesa > planejado: ⚠️ Atenção

#### Cenário 3: Análise de Performance
1. Olhe **Análise de Desvios**
2. Verifique a pizza: X/12 meses controlados
3. Veja estatísticas: está economizando ou estourando?
4. Identifique mês de maior estouro para investigar

---

### ✅ Resumo das Melhorias

**Antes (v1.3):**
- 4 gráficos
- Análise básica
- Foco em totais

**Agora (v1.4):**
- 7 gráficos completos
- Análise detalhada de controle
- Sistema de alertas (vermelho/amarelo/verde)
- Estatísticas de desvio
- Identificação clara de problemas
- Comparação visual tripla

---

## ✨ Versão 1.3 - Visão Anual Completa

### 📆 Nova Funcionalidade: Dashboard Anual

#### 🎯 Visão Geral
- ✅ **Aba "Visão Anual"** no Dashboard
- ✅ Análise completa de todo o ano
- ✅ Seleção de qualquer ano (2020-2030)
- ✅ Comparação mês a mês automática

#### 📊 KPIs Anuais
- ✅ Total de Entradas do Ano
- ✅ Total de Despesas do Ano
- ✅ Saldo Anual Acumulado
- ✅ Média Mensal de Saldo

#### 📈 Gráficos Analíticos

**1. Fluxo de Caixa Mensal (Área)**
- Linha de Entradas (verde)
- Linha de Despesas (vermelho)
- Visualização de tendências ao longo do ano
- Hover interativo com valores

**2. Saldo Mês a Mês (Barras)**
- Barras verdes: Saldo positivo
- Barras vermelhas: Saldo negativo
- Valores exibidos em cada barra
- Linha de referência no zero

**3. Planejado vs Realizado (Linhas)**
- Linha tracejada: Orçamento planejado
- Linha sólida: Despesas realizadas
- Comparação visual de aderência ao orçamento
- Identificação de meses fora do planejamento

**4. Percentual de Gastos (Barras Coloridas)**
- Escala de cores:
  - Verde: Baixo percentual
  - Amarelo: Médio percentual
  - Vermelho: Alto percentual
- Linha de 100% (gastou tudo)
- % exibido em cada barra

#### 📋 Tabela Detalhada Ano Completo

**Colunas:**
- ✅ Mês
- ✅ Entradas
- ✅ Despesas
- ✅ Saldo
- ✅ Planejado (orçamento)
- ✅ Diferença do Planejado
- ✅ % Gasto

**Recursos:**
- ✅ Linha de TOTAIS no final
- ✅ Formatação monetária brasileira
- ✅ 500px de altura (scrollable)
- ✅ Download em CSV
- ✅ Visualização completa de 12 meses

#### 💡 Insights Automáticos

**Análise Inteligente:**
- ✅ **Melhor Mês** - Mês com maior saldo
- ✅ **Pior Mês** - Mês com menor saldo
- ✅ **Mais Econômico** - Mês que mais economizou vs planejado
- ✅ Cards coloridos (verde/vermelho/azul)

#### 📥 Exportação
- ✅ Botão de download da tabela anual
- ✅ Formato CSV
- ✅ Nome do arquivo: `relatorio_anual_YYYY.csv`
- ✅ Pronto para Excel/Google Sheets

---

## ✨ Versão 1.2 - Lançamentos Parcelados e Dashboard Melhorado

### 🎯 Lançamentos Aprimorados

#### 📋 Telas Separadas
- ✅ **Aba "Nova Entrada"** - Tela dedicada para registro de entradas
- ✅ **Aba "Nova Despesa"** - Tela dedicada para registro de despesas
- ✅ Interface mais clara e intuitiva
- ✅ Campos específicos para cada tipo

#### 💳 Sistema de Parcelamento
- ✅ **Lançamentos Recorrentes/Parcelados**
  - Checkbox para ativar parcelamento
  - Número de meses/parcelas (2 a 60)
  - Dois modos de parcelamento:
    - **Valor total dividido** - Divide o valor total pelas parcelas
    - **Valor fixo por mês** - Repete o mesmo valor em cada mês

- ✅ **Preview de Parcelas**
  - Mostra quantas parcelas serão criadas
  - Mostra o valor de cada parcela

- ✅ **Descrição Automática**
  - Adiciona "(Parcela X/Y)" automaticamente
  - Mantém descrição original

- ✅ **Criação em Lote**
  - Cria todos os lançamentos de uma vez
  - Distribui automaticamente pelos meses
  - Feedback de sucesso/erro para cada parcela

**Exemplo de uso:**
- Compra parcelada em 12x de R$ 1.200,00
- Sistema cria 12 lançamentos de R$ 100,00 cada
- Um para cada mês subsequente

### 📊 Dashboard Melhorado

#### 💰 Visão de Saldo Aprimorada

**KPIs Principais:**
- ✅ Total de Entradas
- ✅ Total de Despesas
- ✅ **Saldo do Mês** (com indicador visual)
- ✅ **% Gasto** - Percentual de despesas sobre entradas

**Barra Visual de Saldo:**
- ✅ Comparação visual Entradas vs Despesas
- ✅ Cores diferenciadas (verde/vermelho)
- ✅ Status do saldo (Positivo/Negativo)
- ✅ Valores exibidos na barra

#### 📈 Comparativo Mensal (NOVO!)

**Gráfico de Evolução - Últimos 6 Meses:**
- ✅ Linha de Entradas (verde)
- ✅ Linha de Despesas (vermelho)
- ✅ Valores exibidos em cada ponto
- ✅ Navegação interativa
- ✅ Hover com detalhes

**Gráfico de Saldo Mensal:**
- ✅ Barras de saldo por mês
- ✅ Cores dinâmicas:
  - Verde para saldo positivo
  - Vermelho para saldo negativo
- ✅ Linha de referência no zero
- ✅ Valores exibidos nas barras

**Análise Temporal:**
- ✅ Visualização de tendências
- ✅ Identificação de padrões de gastos
- ✅ Comparação entre períodos
- ✅ Histórico completo de 6 meses

### 🎨 Melhorias Visuais

- ✅ Layout mais organizado
- ✅ Seções bem definidas
- ✅ Cores consistentes (verde/vermelho para positivo/negativo)
- ✅ Gráficos interativos com Plotly
- ✅ Feedback visual de status

---

## 📊 Como Usar as Novas Funcionalidades

### Visão Anual

1. **Acessar Dashboard**
2. Clicar na aba **"📆 Visão Anual"**
3. Selecionar o ano desejado
4. Visualizar:
   - KPIs anuais
   - 4 gráficos diferentes
   - Tabela detalhada mês a mês
   - Insights automáticos
5. Baixar relatório CSV se desejar

### Analisar Tendências

- Compare meses do ano
- Identifique padrões sazonais
- Veja evolução de gastos
- Planeje melhor o próximo ano

### Usar a Tabela

- Role para ver todos os 12 meses
- Confira linha de TOTAIS
- Compare planejado vs realizado
- Baixe para análise externa

---

## 🎯 Casos de Uso

### Exemplo 1: Análise de Fim de Ano
- Selecionar ano atual
- Ver totais anuais
- Identificar melhor e pior mês
- Planejar próximo ano

### Exemplo 2: Comparação Anual
- Alternar entre anos
- Comparar crescimento
- Analisar evolução de gastos

### Exemplo 3: Planejamento Orçamentário
- Ver diferença planejado vs realizado
- Identificar meses que extrapolaram
- Ajustar orçamento para próximo ano

---

## 📈 Benefícios

1. **Visão Macro**
   - Entenda todo o ano de uma vez
   - Identifique padrões sazonais

2. **Tomada de Decisão**
   - Dados completos para planejamento
   - Insights automáticos

3. **Comparação Fácil**
   - 4 tipos de gráficos diferentes
   - Tabela completa exportável

4. **Profissionalismo**
   - Relatórios de qualidade
   - Pronto para apresentações

---

## ✅ Testado e Funcionando

Todas as funcionalidades foram testadas e estão operacionais:
- ✅ Visão anual com todos os gráficos
- ✅ Tabela com 12 meses + totais
- ✅ Insights automáticos
- ✅ Download CSV
- ✅ Alternância entre anos
- ✅ Integração com orçamentos

---

**Versão Atual:** 1.3  
**Data:** 04/02/2026  
**Status:** Pronto para uso! 🚀

## ✨ Novas Funcionalidades

### 🎯 Lançamentos Aprimorados

#### 📋 Telas Separadas
- ✅ **Aba "Nova Entrada"** - Tela dedicada para registro de entradas
- ✅ **Aba "Nova Despesa"** - Tela dedicada para registro de despesas
- ✅ Interface mais clara e intuitiva
- ✅ Campos específicos para cada tipo

#### 💳 Sistema de Parcelamento
- ✅ **Lançamentos Recorrentes/Parcelados**
  - Checkbox para ativar parcelamento
  - Número de meses/parcelas (2 a 60)
  - Dois modos de parcelamento:
    - **Valor total dividido** - Divide o valor total pelas parcelas
    - **Valor fixo por mês** - Repete o mesmo valor em cada mês

- ✅ **Preview de Parcelas**
  - Mostra quantas parcelas serão criadas
  - Mostra o valor de cada parcela

- ✅ **Descrição Automática**
  - Adiciona "(Parcela X/Y)" automaticamente
  - Mantém descrição original

- ✅ **Criação em Lote**
  - Cria todos os lançamentos de uma vez
  - Distribui automaticamente pelos meses
  - Feedback de sucesso/erro para cada parcela

**Exemplo de uso:**
- Compra parcelada em 12x de R$ 1.200,00
- Sistema cria 12 lançamentos de R$ 100,00 cada
- Um para cada mês subsequente

### 📊 Dashboard Melhorado

#### 💰 Visão de Saldo Aprimorada

**KPIs Principais:**
- ✅ Total de Entradas
- ✅ Total de Despesas
- ✅ **Saldo do Mês** (com indicador visual)
- ✅ **% Gasto** - Percentual de despesas sobre entradas

**Barra Visual de Saldo:**
- ✅ Comparação visual Entradas vs Despesas
- ✅ Cores diferenciadas (verde/vermelho)
- ✅ Status do saldo (Positivo/Negativo)
- ✅ Valores exibidos na barra

#### 📈 Comparativo Mensal (NOVO!)

**Gráfico de Evolução - Últimos 6 Meses:**
- ✅ Linha de Entradas (verde)
- ✅ Linha de Despesas (vermelho)
- ✅ Valores exibidos em cada ponto
- ✅ Navegação interativa
- ✅ Hover com detalhes

**Gráfico de Saldo Mensal:**
- ✅ Barras de saldo por mês
- ✅ Cores dinâmicas:
  - Verde para saldo positivo
  - Vermelho para saldo negativo
- ✅ Linha de referência no zero
- ✅ Valores exibidos nas barras

**Análise Temporal:**
- ✅ Visualização de tendências
- ✅ Identificação de padrões de gastos
- ✅ Comparação entre períodos
- ✅ Histórico completo de 6 meses

### 🎨 Melhorias Visuais

- ✅ Layout mais organizado
- ✅ Seções bem definidas
- ✅ Cores consistentes (verde/vermelho para positivo/negativo)
- ✅ Gráficos interativos com Plotly
- ✅ Feedback visual de status

---

## 🔧 Melhorias Técnicas

### Dependências Atualizadas
- ✅ `python-dateutil` - Para cálculo de datas e meses

### Serviços
- ✅ Suporte a múltiplos lançamentos em série
- ✅ Cálculo de totais otimizado

### Dados de Exemplo
- ✅ Script atualizado com 6 meses de dados
- ✅ Variação mensal nos valores
- ✅ Orçamentos para 3 meses

---

## 📊 Como Usar as Novas Funcionalidades

### Criar Lançamento Parcelado

#### Entrada Recorrente (Ex: Salário mensal):
1. Vá em "💰 Nova Entrada"
2. Preencha os dados
3. Marque "💳 Lançamento Recorrente/Parcelado"
4. Escolha "12" meses
5. Selecione "Valor fixo por mês"
6. Clique em "Registrar Entrada"
7. ✅ 12 entradas serão criadas automaticamente!

#### Despesa Parcelada (Ex: Compra em 10x):
1. Vá em "💸 Nova Despesa"
2. Preencha valor total: R$ 1.000,00
3. Marque "💳 Despesa Recorrente/Parcelada"
4. Escolha "10" parcelas
5. Selecione "Valor total dividido"
6. Clique em "Registrar Despesa"
7. ✅ 10 despesas de R$ 100,00 cada serão criadas!

### Analisar Evolução Mensal

1. Acesse o Dashboard
2. Role até "📈 Evolução Mensal"
3. Visualize:
   - Gráfico de linhas (Entradas vs Despesas)
   - Gráfico de barras (Saldo mensal)
4. Passe o mouse sobre os pontos para ver detalhes
5. Analise tendências e padrões

### Verificar Saldo

1. Na parte superior do Dashboard
2. Veja o card "💵 Saldo do Mês"
3. Confira a barra visual
4. Status aparecerá à direita:
   - ✅ Verde: Saldo Positivo
   - ⚠️ Vermelho: Saldo Negativo

---

## 🎯 Casos de Uso

### Exemplo 1: Cartão de Crédito Parcelado
- Compra: R$ 2.400,00 em 12x
- Sistema cria: 12 despesas de R$ 200,00
- Uma por mês nos próximos 12 meses
- Descrição: "Notebook Dell (Parcela 1/12)", etc.

### Exemplo 2: Aluguel Anual
- Valor: R$ 1.200,00/mês
- Criar: 12 parcelas fixas
- Sistema: Lança automático para todo o ano

### Exemplo 3: Análise de Gastos
- Abrir Dashboard
- Ver evolução dos últimos 6 meses
- Identificar meses com maior gasto
- Ajustar planejamento futuro

---

## 📈 Benefícios

1. **Economia de Tempo**
   - Não precisa lançar manualmente cada mês
   - Criação em lote de parcelas

2. **Visão Completa**
   - Histórico de 6 meses sempre visível
   - Comparativos automáticos

3. **Melhor Planejamento**
   - Visualize tendências
   - Identifique padrões
   - Tome decisões informadas

4. **Organização**
   - Telas separadas por tipo
   - Interface mais limpa
   - Fluxo mais intuitivo

---

## ✅ Testado e Funcionando

Todas as funcionalidades foram testadas e estão operacionais:
- ✅ Parcelamento com divisão de valor
- ✅ Parcelamento com valor fixo
- ✅ Gráficos de evolução
- ✅ Cálculo de saldo
- ✅ Dados de exemplo com 6 meses

---

**Versão:** 1.2  
**Data:** 03/02/2026  
**Status:** Pronto para uso! 🚀
