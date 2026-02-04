import streamlit as st
from datetime import datetime
from services import OrcamentoService, CategoriaService
from models.categoria import TipoCategoria
from utils.formatador import FormatadorBR


def mostrar_planejamento():
    """Tela de planejamento financeiro e orçamentos."""
    
    usuario = st.session_state['usuario']
    formatador = FormatadorBR()
    
    st.title("📋 Planejamento Financeiro")
    
    # Seletor de período
    col1, col2 = st.columns(2)
    
    with col1:
        mes = st.selectbox(
            "Mês",
            range(1, 13),
            index=datetime.now().month - 1,
            format_func=lambda x: formatador.mes_ano_formatado(x, 2024).split(' de ')[0],
            key="planejamento_mes"
        )
    
    with col2:
        ano = st.selectbox(
            "Ano",
            range(2020, 2031),
            index=range(2020, 2031).index(datetime.now().year),
            key="planejamento_ano"
        )
    
    st.divider()
    
    # Resumo do orçamento
    resumo = OrcamentoService.obter_resumo_orcamento(usuario.id, mes, ano)
    
    if resumo['total_planejado'] > 0:
        st.subheader("📊 Resumo do Orçamento")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Orçamento Total",
                formatador.formatar_moeda(resumo['total_planejado'])
            )
        
        with col2:
            st.metric(
                "Total Realizado",
                formatador.formatar_moeda(resumo['total_realizado'])
            )
        
        with col3:
            st.metric(
                "Diferença",
                formatador.formatar_moeda(resumo['diferenca']),
                delta=None
            )
        
        with col4:
            st.metric(
                "% Utilizado",
                formatador.formatar_percentual(resumo['percentual_utilizado'])
            )
        
        # Barra de progresso
        progresso = min(resumo['percentual_utilizado'] / 100, 1.0)
        cor_progresso = "normal" if progresso <= 0.8 else "inverse"
        
        st.progress(progresso)
        
        st.divider()
    
    # Tabs
    tab_orcamentos, tab_definir = st.tabs(["Orçamentos do Mês", "Definir Orçamento"])
    
    with tab_orcamentos:
        st.subheader("Orçamentos por Categoria")
        
        orcamentos = OrcamentoService.listar_orcamentos(usuario.id, mes, ano)
        
        if orcamentos:
            for orc in orcamentos:
                with st.expander(f"**{orc['categoria_nome']}** - {formatador.formatar_moeda(orc['valor_planejado'])}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Planejado",
                            formatador.formatar_moeda(orc['valor_planejado'])
                        )
                    
                    with col2:
                        st.metric(
                            "Realizado",
                            formatador.formatar_moeda(orc['valor_realizado'])
                        )
                    
                    with col3:
                        st.metric(
                            "% Utilizado",
                            formatador.formatar_percentual(orc['percentual_utilizado'])
                        )
                    
                    # Barra de progresso individual
                    progresso_cat = min(orc['percentual_utilizado'] / 100, 1.0)
                    st.progress(progresso_cat)
                    
                    # Diferença
                    if orc['diferenca'] > 0:
                        st.success(f"✅ Saldo disponível: {formatador.formatar_moeda(orc['diferenca'])}")
                    elif orc['diferenca'] < 0:
                        st.error(f"⚠️ Orçamento excedido em: {formatador.formatar_moeda(abs(orc['diferenca']))}")
                    else:
                        st.info("🎯 Orçamento totalmente utilizado!")
                    
                    # Botão para excluir
                    if st.button("🗑️ Excluir Orçamento", key=f"del_orc_{orc['id']}"):
                        sucesso, mensagem = OrcamentoService.excluir_orcamento(orc['id'], usuario.id)
                        if sucesso:
                            st.success(mensagem)
                            st.rerun()
                        else:
                            st.error(mensagem)
        else:
            st.info("💡 Nenhum orçamento definido para este período. Use a aba 'Definir Orçamento' para começar!")
    
    with tab_definir:
        st.subheader("Definir Orçamento para Categoria")
        
        # Apenas categorias de despesa
        categorias_despesa = CategoriaService.listar_categorias(usuario.id, TipoCategoria.DESPESA)
        
        if not categorias_despesa:
            st.warning("⚠️ Você precisa criar categorias de despesa primeiro!")
        else:
            with st.form("form_definir_orcamento"):
                categoria_selecionada = st.selectbox(
                    "Categoria",
                    categorias_despesa,
                    format_func=lambda x: x['nome']
                )
                
                valor_planejado = st.number_input(
                    "Valor Planejado (R$)",
                    min_value=0.01,
                    value=500.0,
                    step=0.01,
                    format="%.2f"
                )
                
                st.info(f"📅 Orçamento será definido para: **{formatador.mes_ano_formatado(mes, ano)}**")
                
                if st.form_submit_button("💾 Definir Orçamento", use_container_width=True):
                    sucesso, mensagem = OrcamentoService.definir_orcamento(
                        usuario.id,
                        categoria_selecionada['id'],
                        mes,
                        ano,
                        valor_planejado
                    )
                    
                    if sucesso:
                        st.success(mensagem)
                        st.rerun()
                    else:
                        st.error(mensagem)
            
            st.divider()
            
            # Dicas de planejamento
            with st.expander("💡 Dicas de Planejamento Financeiro"):
                st.markdown("""
                ### Como planejar seu orçamento:
                
                1. **Analise seus gastos anteriores** - Use o histórico para entender seus padrões de consumo
                2. **Priorize necessidades** - Garanta primeiro os gastos essenciais (moradia, alimentação, saúde)
                3. **Reserve uma margem** - Deixe 10-20% de folga para imprevistos
                4. **Defina metas realistas** - Comece com valores alcançáveis e ajuste conforme necessário
                5. **Acompanhe regularmente** - Verifique seu orçamento semanalmente
                6. **Seja flexível** - Ajuste seu planejamento conforme as circunstâncias mudarem
                
                ### Regra 50-30-20:
                - **50%** para necessidades (moradia, alimentação, transporte)
                - **30%** para desejos (lazer, entretenimento)
                - **20%** para poupança e investimentos
                """)
