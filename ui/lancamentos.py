import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from services import LancamentoService, CategoriaService
from models.lancamento import TipoLancamento
from models.categoria import TipoCategoria
from utils.formatador import FormatadorBR


def mostrar_lancamentos():
    """Tela de gerenciamento de lançamentos financeiros."""
    
    usuario = st.session_state['usuario']
    formatador = FormatadorBR()
    
    st.title("💳 Lançamentos Financeiros")
    
    tab_listar, tab_entrada, tab_despesa = st.tabs(["📋 Meus Lançamentos", "💰 Nova Entrada", "💸 Nova Despesa"])
    
    with tab_listar:
        st.subheader("Lançamentos Registrados")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            mes_filtro = st.selectbox(
                "Mês",
                ['Todos'] + list(range(1, 13)),
                format_func=lambda x: 'Todos' if x == 'Todos' else formatador.mes_ano_formatado(x, 2024).split(' de ')[0]
            )
        
        with col2:
            ano_filtro = st.selectbox(
                "Ano",
                ['Todos'] + list(range(2020, 2031)),
                index=range(2020, 2031).index(datetime.now().year) + 1
            )
        
        with col3:
            categorias = CategoriaService.listar_categorias(usuario.id)
            cat_opcoes = ['Todas'] + [c['nome'] for c in categorias]
            cat_filtro = st.selectbox("Categoria", cat_opcoes)
        
        # Aplica filtros
        mes = None if mes_filtro == 'Todos' else mes_filtro
        ano = None if ano_filtro == 'Todos' else ano_filtro
        categoria_id = None
        
        if cat_filtro != 'Todas':
            categoria_selecionada = next((c for c in categorias if c['nome'] == cat_filtro), None)
            if categoria_selecionada:
                categoria_id = categoria_selecionada['id']
        
        lancamentos = LancamentoService.listar_lancamentos(usuario.id, mes, ano, categoria_id)
        
        if lancamentos:
            # Separa por tipo
            entradas = [l for l in lancamentos if l['categoria_tipo'] == TipoCategoria.ENTRADA]
            despesas = [l for l in lancamentos if l['categoria_tipo'] == TipoCategoria.DESPESA]
            
            # Exibe totais
            total_entradas = sum(l['valor'] for l in entradas)
            total_despesas = sum(l['valor'] for l in despesas)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("💰 Entradas", formatador.formatar_moeda(total_entradas))
            
            with col2:
                st.metric("💸 Despesas", formatador.formatar_moeda(total_despesas))
            
            with col3:
                st.metric("💵 Saldo", formatador.formatar_moeda(total_entradas - total_despesas))
            
            st.divider()
            
            # Lista entradas
            if entradas:
                st.markdown("### 💰 Entradas")
                
                for lanc in entradas:
                    with st.container():
                        col1, col2, col3, col4, col5 = st.columns([1.5, 1, 2, 1.5, 1])
                        
                        with col1:
                            st.write(f"📅 {formatador.formatar_data(lanc['data'])}")
                        
                        with col2:
                            st.markdown(f'<span style="background-color: {lanc["categoria_cor"]}; padding: 2px 8px; border-radius: 4px; color: white;">{lanc["categoria_nome"]}</span>', unsafe_allow_html=True)
                        
                        with col3:
                            st.write(f"**{lanc['descricao']}**")
                        
                        with col4:
                            st.write(f"**{formatador.formatar_moeda(lanc['valor'])}**")
                        
                        with col5:
                            if st.button("🗑️", key=f"del_ent_{lanc['id']}"):
                                sucesso, mensagem = LancamentoService.excluir_lancamento(lanc['id'], usuario.id)
                                if sucesso:
                                    st.success(mensagem)
                                    st.rerun()
                                else:
                                    st.error(mensagem)
                
                st.divider()
            
            # Lista despesas
            if despesas:
                st.markdown("### 💸 Despesas")
                
                for lanc in despesas:
                    with st.container():
                        col1, col2, col3, col4, col5 = st.columns([1.5, 1, 2, 1.5, 1])
                        
                        with col1:
                            st.write(f"📅 {formatador.formatar_data(lanc['data'])}")
                        
                        with col2:
                            st.markdown(f'<span style="background-color: {lanc["categoria_cor"]}; padding: 2px 8px; border-radius: 4px; color: white;">{lanc["categoria_nome"]}</span>', unsafe_allow_html=True)
                        
                        with col3:
                            st.write(f"**{lanc['descricao']}**")
                        
                        with col4:
                            st.write(f"**{formatador.formatar_moeda(lanc['valor'])}**")
                        
                        with col5:
                            if st.button("🗑️", key=f"del_desp_{lanc['id']}"):
                                sucesso, mensagem = LancamentoService.excluir_lancamento(lanc['id'], usuario.id)
                                if sucesso:
                                    st.success(mensagem)
                                    st.rerun()
                                else:
                                    st.error(mensagem)
        else:
            st.info("📭 Nenhum lançamento encontrado com os filtros selecionados.")
    
    with tab_entrada:
        st.subheader("💰 Registrar Nova Entrada")
        
        # Busca categorias de entrada
        categorias_entrada = CategoriaService.listar_categorias(usuario.id, TipoCategoria.ENTRADA)
        
        if not categorias_entrada:
            st.warning("⚠️ Você precisa criar categorias de entrada primeiro!")
            st.info("💡 Vá em **Categorias** e crie categorias como: Salário, Freelance, Investimentos, etc.")
        else:
            with st.form("form_nova_entrada"):
                st.markdown("#### 📝 Informações da Entrada")
                
                categoria = st.selectbox(
                    "Categoria",
                    categorias_entrada,
                    format_func=lambda x: x['nome'],
                    key="entrada_categoria"
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    data_entrada = st.date_input(
                        "Data",
                        value=date.today(),
                        max_value=date.today() + timedelta(days=365),
                        key="entrada_data"
                    )
                
                with col2:
                    valor = st.number_input(
                        "Valor (R$)",
                        min_value=0.01,
                        value=1000.0,
                        step=0.01,
                        format="%.2f",
                        key="entrada_valor"
                    )
                
                descricao = st.text_input(
                    "Descrição",
                    placeholder="Ex: Salário de Janeiro, Freelance projeto X...",
                    key="entrada_descricao"
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    tipo = st.selectbox(
                        "Tipo",
                        [TipoLancamento.FIXA, TipoLancamento.VARIAVEL],
                        format_func=lambda x: x.value,
                        key="entrada_tipo"
                    )
                
                with col2:
                    parcelado = st.checkbox("💳 Lançamento Recorrente/Parcelado", key="entrada_parcelado")
                
                # Se for parcelado
                num_parcelas = 1
                if parcelado:
                    st.markdown("---")
                    st.markdown("#### 🔄 Configuração de Parcelas")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        num_parcelas = st.number_input(
                            "Número de meses",
                            min_value=2,
                            max_value=60,
                            value=12,
                            step=1,
                            help="Número de meses que esta entrada se repetirá",
                            key="entrada_num_parcelas"
                        )
                    
                    with col2:
                        tipo_parcelamento = st.radio(
                            "Tipo",
                            ["Valor total dividido", "Valor fixo por mês"],
                            help="Dividir o valor total pelas parcelas ou repetir o valor em cada mês",
                            key="entrada_tipo_parcelamento"
                        )
                    
                    # Preview das parcelas
                    if tipo_parcelamento == "Valor total dividido":
                        valor_parcela = valor / num_parcelas
                        st.info(f"💡 Serão criadas {num_parcelas} entradas de {formatador.formatar_moeda(valor_parcela)} cada")
                    else:
                        st.info(f"💡 Serão criadas {num_parcelas} entradas de {formatador.formatar_moeda(valor)} cada")
                
                st.markdown("---")
                
                if st.form_submit_button("✅ Registrar Entrada", use_container_width=True, type="primary"):
                    if not descricao:
                        st.error("Por favor, informe uma descrição!")
                    else:
                        sucesso_total = True
                        mensagens_erro = []
                        
                        # Calcula valor da parcela se for parcelado
                        if parcelado and tipo_parcelamento == "Valor total dividido":
                            valor_a_lancar = valor / num_parcelas
                        else:
                            valor_a_lancar = valor
                        
                        # Cria os lançamentos
                        for i in range(num_parcelas):
                            # Calcula a data do lançamento
                            if i == 0:
                                data_lanc = data_entrada
                            else:
                                data_lanc = data_entrada + relativedelta(months=i)
                            
                            # Cria descrição da parcela
                            if num_parcelas > 1:
                                desc_parcela = f"{descricao} ({i+1}/{num_parcelas})"
                            else:
                                desc_parcela = descricao
                            
                            sucesso, mensagem, _ = LancamentoService.criar_lancamento(
                                usuario.id,
                                categoria['id'],
                                data_lanc,
                                valor_a_lancar,
                                desc_parcela,
                                tipo
                            )
                            
                            if not sucesso:
                                sucesso_total = False
                                mensagens_erro.append(f"Parcela {i+1}: {mensagem}")
                        
                        if sucesso_total:
                            if num_parcelas > 1:
                                st.success(f"✅ {num_parcelas} entradas criadas com sucesso!")
                            else:
                                st.success("✅ Entrada registrada com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Alguns lançamentos falharam:")
                            for msg in mensagens_erro:
                                st.error(msg)
    
    with tab_despesa:
        st.subheader("💸 Registrar Nova Despesa")
        
        # Busca categorias de despesa
        categorias_despesa = CategoriaService.listar_categorias(usuario.id, TipoCategoria.DESPESA)
        
        if not categorias_despesa:
            st.warning("⚠️ Você precisa criar categorias de despesa primeiro!")
            st.info("💡 Vá em **Categorias** e crie categorias como: Moradia, Alimentação, Transporte, etc.")
        else:
            with st.form("form_nova_despesa"):
                st.markdown("#### 📝 Informações da Despesa")
                
                categoria = st.selectbox(
                    "Categoria",
                    categorias_despesa,
                    format_func=lambda x: x['nome'],
                    key="despesa_categoria"
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    data_despesa = st.date_input(
                        "Data",
                        value=date.today(),
                        max_value=date.today() + timedelta(days=365),
                        key="despesa_data"
                    )
                
                with col2:
                    valor = st.number_input(
                        "Valor (R$)",
                        min_value=0.01,
                        value=100.0,
                        step=0.01,
                        format="%.2f",
                        key="despesa_valor"
                    )
                
                descricao = st.text_input(
                    "Descrição",
                    placeholder="Ex: Aluguel, Supermercado, Conta de luz...",
                    key="despesa_descricao"
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    tipo = st.selectbox(
                        "Tipo",
                        [TipoLancamento.FIXA, TipoLancamento.VARIAVEL],
                        format_func=lambda x: x.value,
                        key="despesa_tipo"
                    )
                
                with col2:
                    parcelado = st.checkbox("💳 Despesa Recorrente/Parcelada", key="despesa_parcelado")
                
                # Se for parcelado
                num_parcelas = 1
                if parcelado:
                    st.markdown("---")
                    st.markdown("#### 🔄 Configuração de Parcelas")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        num_parcelas = st.number_input(
                            "Número de parcelas",
                            min_value=2,
                            max_value=60,
                            value=12,
                            step=1,
                            help="Número de meses que esta despesa se repetirá",
                            key="despesa_num_parcelas"
                        )
                    
                    with col2:
                        tipo_parcelamento = st.radio(
                            "Tipo",
                            ["Valor total dividido", "Valor fixo por mês"],
                            help="Dividir o valor total pelas parcelas ou repetir o valor em cada mês",
                            key="despesa_tipo_parcelamento"
                        )
                    
                    # Preview das parcelas
                    if tipo_parcelamento == "Valor total dividido":
                        valor_parcela = valor / num_parcelas
                        st.info(f"💡 Serão criadas {num_parcelas} despesas de {formatador.formatar_moeda(valor_parcela)} cada")
                    else:
                        st.info(f"💡 Serão criadas {num_parcelas} despesas de {formatador.formatar_moeda(valor)} cada")
                
                st.markdown("---")
                
                if st.form_submit_button("✅ Registrar Despesa", use_container_width=True, type="primary"):
                    if not descricao:
                        st.error("Por favor, informe uma descrição!")
                    else:
                        sucesso_total = True
                        mensagens_erro = []
                        
                        # Calcula valor da parcela se for parcelado
                        if parcelado and tipo_parcelamento == "Valor total dividido":
                            valor_a_lancar = valor / num_parcelas
                        else:
                            valor_a_lancar = valor
                        
                        # Cria os lançamentos
                        for i in range(num_parcelas):
                            # Calcula a data do lançamento
                            if i == 0:
                                data_lanc = data_despesa
                            else:
                                data_lanc = data_despesa + relativedelta(months=i)
                            
                            # Cria descrição da parcela
                            if num_parcelas > 1:
                                desc_parcela = f"{descricao} (Parcela {i+1}/{num_parcelas})"
                            else:
                                desc_parcela = descricao
                            
                            sucesso, mensagem, _ = LancamentoService.criar_lancamento(
                                usuario.id,
                                categoria['id'],
                                data_lanc,
                                valor_a_lancar,
                                desc_parcela,
                                tipo
                            )
                            
                            if not sucesso:
                                sucesso_total = False
                                mensagens_erro.append(f"Parcela {i+1}: {mensagem}")
                        
                        if sucesso_total:
                            if num_parcelas > 1:
                                st.success(f"✅ {num_parcelas} despesas criadas com sucesso!")
                            else:
                                st.success("✅ Despesa registrada com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Alguns lançamentos falharam:")
                            for msg in mensagens_erro:
                                st.error(msg)
