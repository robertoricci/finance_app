import streamlit as st
from datetime import datetime
from services import LancamentoService, OrcamentoService
from reports import RelatorioFinanceiro
from utils.formatador import FormatadorBR


def mostrar_relatorios():
    """Tela de geração de relatórios."""
    
    usuario = st.session_state['usuario']
    formatador = FormatadorBR()
    
    st.title("📄 Relatórios")
    
    st.markdown("""
    Gere relatórios financeiros completos em PDF com resumo do mês, 
    detalhamento de lançamentos e gráficos.
    """)
    
    st.divider()
    
    # Seletor de período
    col1, col2 = st.columns(2)
    
    with col1:
        mes = st.selectbox(
            "Mês do Relatório",
            range(1, 13),
            index=datetime.now().month - 1,
            format_func=lambda x: formatador.mes_ano_formatado(x, 2024).split(' de ')[0],
            key="relatorio_mes"
        )
    
    with col2:
        ano = st.selectbox(
            "Ano do Relatório",
            range(2020, 2031),
            index=range(2020, 2031).index(datetime.now().year),
            key="relatorio_ano"
        )
    
    st.divider()
    
    # Preview dos dados
    st.subheader("📊 Preview do Relatório")
    
    totais = LancamentoService.calcular_totais(usuario.id, mes, ano)
    lancamentos = LancamentoService.listar_lancamentos(usuario.id, mes, ano)
    orcamentos = OrcamentoService.listar_orcamentos(usuario.id, mes, ano)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💰 Entradas", formatador.formatar_moeda(totais['total_entradas']))
    
    with col2:
        st.metric("💸 Despesas", formatador.formatar_moeda(totais['total_despesas']))
    
    with col3:
        st.metric("💵 Saldo", formatador.formatar_moeda(totais['saldo']))
    
    st.markdown(f"""
    - **Total de Lançamentos:** {len(lancamentos)}
    - **Orçamentos Definidos:** {len(orcamentos)}
    - **Período:** {formatador.mes_ano_formatado(mes, ano)}
    """)
    
    st.divider()
    
    # Botão de geração
    if st.button("📥 Gerar Relatório PDF", type="primary", use_container_width=True):
        if not lancamentos:
            st.warning("⚠️ Não há lançamentos registrados neste período para gerar relatório.")
        else:
            with st.spinner("Gerando relatório PDF..."):
                try:
                    # Gera o relatório
                    gerador = RelatorioFinanceiro()
                    pdf_buffer = gerador.gerar_relatorio_mensal(
                        usuario.nome,
                        mes,
                        ano,
                        totais,
                        lancamentos,
                        orcamentos
                    )
                    
                    # Oferece para download
                    nome_arquivo = f"relatorio_financeiro_{mes:02d}_{ano}.pdf"
                    
                    st.success("✅ Relatório gerado com sucesso!")
                    
                    st.download_button(
                        label="📥 Baixar Relatório PDF",
                        data=pdf_buffer,
                        file_name=nome_arquivo,
                        mime="application/pdf",
                        use_container_width=True
                    )
                
                except Exception as e:
                    st.error(f"❌ Erro ao gerar relatório: {str(e)}")
    
    st.divider()
    
    # Informações sobre o relatório
    with st.expander("ℹ️ O que está incluído no relatório?"):
        st.markdown("""
        ### Conteúdo do Relatório PDF:
        
        1. **Cabeçalho**
           - Nome do usuário
           - Período do relatório
           - Data de geração
        
        2. **Resumo Financeiro**
           - Total de entradas
           - Total de despesas
           - Saldo do mês
        
        3. **Orçamento vs Realizado** (se houver orçamentos definidos)
           - Comparativo por categoria
           - Percentual utilizado
           - Valores planejados vs realizados
        
        4. **Lançamentos Detalhados**
           - Todas as entradas do período
           - Todas as despesas do período
           - Organizados por data
           - Com categoria e descrição
        
        ### Dicas:
        - Gere relatórios mensais para acompanhar sua evolução
        - Use os relatórios para análise de padrões de consumo
        - Arquive os PDFs para histórico financeiro
        - Compartilhe com seu contador ou planejador financeiro
        """)
