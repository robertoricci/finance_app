# 🚀 GUIA RÁPIDO DE INSTALAÇÃO

## Opção 1: Usando o Script Automático (Recomendado)

### Windows:
```bash
python setup.py
```

### Linux/Mac:
```bash
python3 setup.py
```

O script irá:
1. Verificar a versão do Python
2. Instalar todas as dependências
3. Iniciar a aplicação automaticamente

---

## Opção 2: Instalação Manual

### Passo 1: Verificar Python
```bash
python --version
```
Deve ser Python 3.10 ou superior.

### Passo 2: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 3: Executar a Aplicação
```bash
streamlit run app.py
```

---

## 📱 Acessando a Aplicação

Após executar, a aplicação abrirá automaticamente no navegador em:
- **URL Local:** http://localhost:8501
- **URL de Rede:** http://[seu-ip]:8501

---

## 🎯 Primeiro Uso

1. **Registrar-se:**
   - Clique na aba "Registrar-se"
   - Preencha: Nome, Email, Senha
   - Clique em "Registrar"

2. **Fazer Login:**
   - Use o email e senha cadastrados
   - Clique em "Entrar"

3. **Começar a usar:**
   - O sistema já vem com categorias padrão
   - Acesse "💳 Lançamentos" para registrar entradas/despesas
   - Acesse "📋 Planejamento" para definir orçamentos
   - Acesse "📊 Dashboard" para visualizar seus dados

---

## 🛠️ Solução de Problemas

### Erro: "streamlit: command not found"
```bash
pip install streamlit
```

### Erro: "No module named 'sqlalchemy'"
```bash
pip install -r requirements.txt
```

### Porta 8501 já está em uso
```bash
streamlit run app.py --server.port 8502
```

### Problemas de permissão (Linux/Mac)
```bash
chmod +x setup.py
```

---

## 📞 Dicas

- **Backup dos Dados:** O arquivo `finance_app.db` contém todos os seus dados
- **Resetar Banco:** Delete o arquivo `finance_app.db` e reinicie a aplicação
- **Várias Instâncias:** Cada cópia do app tem seu próprio banco de dados
- **Deploy:** O sistema pode ser facilmente deployado no Streamlit Cloud

---

## ✅ Checklist de Funcionalidades

- [x] Sistema multiusuário
- [x] Dashboard com gráficos
- [x] Gestão de categorias
- [x] Lançamentos financeiros
- [x] Planejamento e orçamentos
- [x] Relatórios em PDF
- [x] Formatação brasileira (R$)
- [x] Interface responsiva
- [x] Banco de dados SQLite

---

**Desenvolvido com Python + Streamlit**
Versão: 1.0.0
