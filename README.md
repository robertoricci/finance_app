# 💰 Sistema de Finanças Pessoais

Sistema completo e profissional para gerenciamento de finanças pessoais desenvolvido com Python e Streamlit.

## 🎯 Funcionalidades

### ✅ Sistema Multiusuário
- Cadastro e autenticação de usuários
- Cada usuário tem seus próprios dados isolados
- Sistema de hash de senhas para segurança

### 📊 Dashboard Interativo
- Indicadores financeiros (KPIs)
- Gráficos de pizza (despesas por categoria)
- Gráficos de barras (entrada vs despesa)
- Comparativo orçamento vs realizado
- Filtros por mês e ano

### 🏷️ Gestão de Categorias
- CRUD completo de categorias
- Separação entre Despesas e Entradas
- Personalização de cores
- Categorias padrão criadas automaticamente

### 💳 Lançamentos Financeiros
- Cadastro de despesas e entradas
- Campos: data, valor, categoria, descrição, tipo (fixa/variável)
- Edição e exclusão de lançamentos
- Filtros avançados (mês, ano, categoria)
- Totalizadores automáticos

### 📋 Planejamento Financeiro
- Definição de orçamento por categoria
- Comparação planejado vs realizado
- Indicadores de percentual utilizado
- Alertas de orçamento excedido
- Dicas de planejamento financeiro

### 📄 Relatórios em PDF
- Geração automática de relatórios mensais
- Resumo financeiro completo
- Lista detalhada de lançamentos
- Comparativo de orçamento
- Download direto do PDF

## 🏗️ Arquitetura

```
finance_app/
├── models/              # Modelos de dados (SQLAlchemy)
│   ├── usuario.py
│   ├── categoria.py
│   ├── lancamento.py
│   └── orcamento_mensal.py
├── database/            # Camada de banco de dados
│   ├── base.py
│   └── connection.py
├── services/            # Lógica de negócio
│   ├── auth_service.py
│   ├── categoria_service.py
│   ├── lancamento_service.py
│   └── orcamento_service.py
├── ui/                  # Interface do usuário (Streamlit)
│   ├── autenticacao.py
│   ├── dashboard.py
│   ├── categorias.py
│   ├── lancamentos.py
│   ├── planejamento.py
│   └── relatorios.py
├── reports/             # Geração de relatórios
│   └── pdf_generator.py
├── utils/               # Utilitários
│   └── formatador.py
├── app.py              # Aplicação principal
└── requirements.txt    # Dependências
```

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 2: Executar a Aplicação

```bash
streamlit run app.py
```

O sistema será aberto automaticamente no navegador em `http://localhost:8501`

## 📖 Como Usar

### 1. Primeiro Acesso
1. Clique na aba "Registrar-se"
2. Preencha seus dados (nome, email, senha)
3. Após o registro, faça login com suas credenciais

### 2. Configuração Inicial
1. O sistema já cria categorias padrão automaticamente
2. Você pode adicionar mais categorias em "🏷️ Categorias"
3. Personalize cores e nomes conforme sua preferência

### 3. Registrando Lançamentos
1. Acesse "💳 Lançamentos"
2. Clique em "Novo Lançamento"
3. Escolha o tipo (Entrada ou Despesa)
4. Preencha os dados e salve

### 4. Planejamento
1. Acesse "📋 Planejamento"
2. Selecione mês e ano
3. Defina valores de orçamento para cada categoria
4. Acompanhe o percentual utilizado

### 5. Dashboard
1. Acesse "📊 Dashboard"
2. Visualize seus indicadores financeiros
3. Analise gráficos de gastos
4. Compare orçamento vs realizado

### 6. Relatórios
1. Acesse "📄 Relatórios"
2. Selecione o período desejado
3. Clique em "Gerar Relatório PDF"
4. Baixe o arquivo gerado

## 💾 Banco de Dados

- **Tipo:** SQLite
- **Arquivo:** `finance_app.db` (criado automaticamente)
- **ORM:** SQLAlchemy
- **Tabelas:**
  - `usuarios` - Dados dos usuários
  - `categorias` - Categorias financeiras
  - `lancamentos` - Lançamentos financeiros
  - `orcamentos_mensais` - Orçamentos planejados

## 🎨 Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit** - Framework web para interface
- **SQLAlchemy** - ORM para banco de dados
- **Pandas** - Manipulação de dados
- **Plotly** - Gráficos interativos
- **ReportLab** - Geração de PDFs

## 🔒 Segurança

- Senhas armazenadas com hash SHA-256
- Isolamento de dados por usuário
- Validações em todas as operações
- Tratamento de erros robusto

## ✨ Diferenciais

- ✅ Código modular e organizado
- ✅ Arquitetura em camadas (MVC)
- ✅ Comentários em português
- ✅ Formatação monetária brasileira (R$)
- ✅ Interface intuitiva e responsiva
- ✅ Gráficos interativos e profissionais
- ✅ Sistema multiusuário completo
- ✅ Relatórios profissionais em PDF

## 🛠️ Manutenção e Extensões

### Adicionar Novas Funcionalidades
1. Criar serviço em `services/`
2. Criar interface em `ui/`
3. Adicionar rota em `app.py`

### Modificar Modelos
1. Editar modelo em `models/`
2. Deletar arquivo `finance_app.db`
3. Reiniciar aplicação (banco será recriado)

### Personalizar Visual
- Editar componentes em `ui/`
- Modificar cores em `models/categoria.py`
- Ajustar layout em cada arquivo de UI

## 📝 Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências estão instaladas
2. Certifique-se de estar usando Python 3.10+
3. Verifique se a porta 8501 está disponível

## 📄 Licença

Este projeto é de código aberto e está disponível para uso pessoal e educacional.

---

Desenvolvido com ❤️ usando Python e Streamlit
