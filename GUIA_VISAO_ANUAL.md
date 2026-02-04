# 📆 GUIA: VISÃO ANUAL DO DASHBOARD

## 🎯 Funcionalidade Principal

A **Visão Anual** oferece uma análise completa de todo o ano financeiro em uma única tela, com gráficos interativos, tabela detalhada e insights automáticos.

---

## 🚀 Como Acessar

1. Faça login no sistema
2. Clique em **📊 Dashboard** no menu lateral
3. Selecione a aba **"📆 Visão Anual"**
4. Escolha o ano que deseja analisar

---

## 📊 O Que Você Verá

### 1️⃣ KPIs Anuais (Topo da Página)

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ 💰 Total de     │ 💸 Total de     │ 💵 Saldo        │ 📊 Média        │
│    Entradas     │    Despesas     │    Anual        │    Mensal       │
│  R$ 60.000,00   │  R$ 45.000,00   │  R$ 15.000,00   │  R$ 1.250,00    │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

**Descrição:**
- **Total de Entradas**: Soma de todas as entradas do ano
- **Total de Despesas**: Soma de todas as despesas do ano
- **Saldo Anual**: Diferença entre entradas e despesas
- **Média Mensal**: Saldo médio por mês (Saldo Anual ÷ 12)

---

### 2️⃣ Gráfico: Fluxo de Caixa Mensal

**Tipo:** Gráfico de Área  
**Cores:** Verde (Entradas) e Vermelho (Despesas)

**O que mostra:**
- Evolução das entradas mês a mês
- Evolução das despesas mês a mês
- Área preenchida para melhor visualização
- Tendências ao longo do ano

**Como usar:**
- Passe o mouse sobre os pontos para ver valores exatos
- Identifique meses de pico de entrada/despesa
- Compare visualmente os dois fluxos

**Exemplo de análise:**
- "Em Dezembro as entradas aumentaram (13º salário)"
- "Em Janeiro as despesas foram maiores (férias/impostos)"

---

### 3️⃣ Gráfico: Saldo Mês a Mês

**Tipo:** Gráfico de Barras  
**Cores:** Verde (positivo) e Vermelho (negativo)

**O que mostra:**
- Saldo de cada mês do ano
- Cor verde: Você teve sobra (saldo positivo)
- Cor vermelha: Você gastou mais do que ganhou
- Linha tracejada no zero como referência

**Como usar:**
- Identifique rapidamente meses problemáticos (vermelho)
- Veja quais meses você conseguiu economizar (verde)
- Planeje ações corretivas para meses negativos

**Exemplo de análise:**
- "Janeiro e Fevereiro tive saldo negativo"
- "De Março a Junho consegui economizar"
- "Dezembro foi meu melhor mês"

---

### 4️⃣ Gráfico: Planejado vs Realizado

**Tipo:** Gráfico de Linhas  
**Cores:** Azul tracejado (Planejado) e Laranja sólido (Realizado)

**O que mostra:**
- Linha azul: Quanto você planejou gastar (orçamento)
- Linha laranja: Quanto você realmente gastou
- Comparação visual de aderência ao planejamento

**Como usar:**
- Veja se está seguindo seu orçamento
- Identifique meses que extrapolaram
- Ajuste planejamento futuro

**Exemplo de análise:**
- "Em Abril gastei R$ 500 a mais que o planejado"
- "Consegui ficar abaixo do orçamento em 8 meses"

**Observação:** Este gráfico só aparece se você tiver orçamentos cadastrados.

---

### 5️⃣ Gráfico: Percentual de Gastos

**Tipo:** Gráfico de Barras Coloridas  
**Cores:** Escala verde → amarelo → vermelho

**O que mostra:**
- Quanto % das suas entradas você gastou em cada mês
- 0-50%: Verde (Gastou pouco, economizou muito)
- 50-80%: Amarelo (Gastou moderadamente)
- 80-100%+: Vermelho (Gastou quase tudo ou mais)
- Linha de referência em 100%

**Como usar:**
- Meses verdes: Ótimo controle financeiro
- Meses amarelos: Atenção, mas ainda ok
- Meses vermelhos: Precisa de atenção/ajuste

**Exemplo de análise:**
- "Janeiro: gastei 120% (vermelho) - usei reservas"
- "Maio: gastei 45% (verde) - consegui economizar 55%"

---

### 6️⃣ Tabela Detalhada Mês a Mês

**Formato:** Tabela com scroll

**Colunas:**

| Mês | Entradas | Despesas | Saldo | Planejado | Dif. Planejado | % Gasto |
|-----|----------|----------|-------|-----------|----------------|---------|
| Janeiro | R$ 5.000,00 | R$ 4.200,00 | R$ 800,00 | R$ 4.000,00 | -R$ 200,00 | 84,0% |
| Fevereiro | R$ 5.000,00 | R$ 3.800,00 | R$ 1.200,00 | R$ 4.000,00 | R$ 200,00 | 76,0% |
| ... | ... | ... | ... | ... | ... | ... |
| **TOTAL** | **R$ 60.000,00** | **R$ 48.000,00** | **R$ 12.000,00** | **R$ 48.000,00** | **R$ 0,00** | **80,0%** |

**Descrição das colunas:**
- **Mês**: Nome do mês
- **Entradas**: Total de entradas do mês
- **Despesas**: Total de despesas do mês
- **Saldo**: Diferença (Entradas - Despesas)
- **Planejado**: Orçamento planejado
- **Dif. Planejado**: Quanto economizou/extrapolou vs planejado
- **% Gasto**: Percentual das entradas que foi gasto

**Linha TOTAL:**
- Última linha em negrito
- Soma/média de todos os meses
- Visão consolidada do ano

**Recursos:**
- ✅ Altura fixa com scroll (500px)
- ✅ Valores formatados em R$
- ✅ Fácil leitura
- ✅ Botão de download

---

### 7️⃣ Botão de Download

**Localização:** Logo abaixo da tabela

```
┌──────────────────────────┐
│ 📥 Baixar Tabela em CSV  │
└──────────────────────────┘
```

**Como usar:**
1. Clique no botão
2. Arquivo será baixado: `relatorio_anual_2024.csv`
3. Abra no Excel, Google Sheets ou qualquer editor CSV

**Utilidades:**
- Análise offline
- Compartilhar com contador
- Criar gráficos personalizados
- Arquivar histórico

---

### 8️⃣ Insights Automáticos

**Localização:** Final da página

Três cards coloridos com insights automáticos:

#### ✅ Melhor Mês (Card Verde)
```
✅ Melhor Mês

Agosto

Saldo: R$ 2.500,00
```
- Mês com maior saldo positivo
- Indica quando você teve melhor desempenho

#### ⚠️ Pior Mês (Card Vermelho)
```
⚠️ Pior Mês

Janeiro

Saldo: -R$ 500,00
```
- Mês com menor saldo (ou maior negativo)
- Alerta para meses problemáticos

#### 💰 Mais Econômico (Card Azul)
```
💰 Mais Econômico

Junho

Economizou: R$ 800,00
```
- Mês que mais economizou vs orçamento planejado
- Mostra quando você teve melhor controle

---

## 💡 Dicas de Uso

### Para Análise Mensal
1. Olhe a tabela completa
2. Identifique padrões sazonais
3. Compare meses similares

### Para Planejamento
1. Veja os insights
2. Identifique meses problemáticos
3. Ajuste orçamento do próximo ano

### Para Apresentação
1. Use os gráficos como evidência
2. Baixe a tabela CSV
3. Prepare relatório para stakeholders

### Para Comparação Anual
1. Alterne entre anos no seletor
2. Compare totais anuais
3. Analise evolução

---

## 🎯 Casos de Uso Práticos

### Caso 1: Planejamento de Fim de Ano
**Situação:** É Dezembro, você quer planejar 2025

**Passos:**
1. Selecione 2024 na visão anual
2. Veja o total anual gasto
3. Identifique categorias que extrapolaram
4. Ajuste orçamento de 2025 baseado nos dados

### Caso 2: Análise de Desempenho
**Situação:** Você quer saber se está melhorando

**Passos:**
1. Compare 2023 vs 2024
2. Veja se saldo anual aumentou
3. Veja se % gasto diminuiu
4. Identifique progressos

### Caso 3: Reunião com Contador
**Situação:** Precisa mostrar dados para contador

**Passos:**
1. Acesse visão anual do ano fiscal
2. Baixe CSV
3. Compartilhe ou imprima gráficos
4. Use insights para discussão

---

## ✅ Checklist de Análise Completa

Use este checklist ao analisar o ano:

- [ ] Verifiquei o saldo anual total
- [ ] Identifiquei melhor e pior mês
- [ ] Analisei tendência de gastos (gráfico de área)
- [ ] Verifiquei quantos meses tive saldo positivo
- [ ] Comparei planejado vs realizado
- [ ] Identifiquei meses com % gasto alto
- [ ] Baixei a tabela para arquivo
- [ ] Anotei insights para próximo ano

---

## 🚨 Alertas Importantes

### ⚠️ Quando Ver Muitos Meses Vermelhos
- **Problema:** Saldo negativo em vários meses
- **Ação:** Revisar gastos, aumentar entradas ou reduzir despesas

### ⚠️ Quando % Gasto > 100%
- **Problema:** Gastando mais do que ganha
- **Ação:** Urgente revisar orçamento e cortar gastos

### ⚠️ Quando Planejado vs Realizado Diverge Muito
- **Problema:** Orçamento irreal ou falta de controle
- **Ação:** Revisar categorias, ajustar orçamento ou melhorar disciplina

---

## 🎓 Aprenda a Interpretar

### Padrões Saudáveis
- ✅ Maioria dos meses em verde (saldo positivo)
- ✅ % gasto entre 60-80%
- ✅ Realizado próximo do planejado
- ✅ Tendência de melhora ao longo do ano

### Padrões de Atenção
- ⚠️ Vários meses em vermelho
- ⚠️ % gasto > 90%
- ⚠️ Realizado muito acima do planejado
- ⚠️ Tendência de piora

---

**Com a Visão Anual, você tem controle total das suas finanças! 📊✨**
