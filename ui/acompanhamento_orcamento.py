import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from services import OrcamentoService, LancamentoService, CategoriaService
from models.categoria import TipoCategoria
from utils.formatador import FormatadorBR


def mostrar_acompanhamento_orcamento():
    """Tela de acompanhamento de orçamento não utilizado."""
    
    usuario = st.session_state['usuario']
    formatador = FormatadorBR()
    
    st.title("💰 Acompanhamento de Orçamento")
    st.markdown("Visualize mês a mês o que foi planejado e quanto ainda resta disponível")
    
    # Seletor de ano
    ano_selecionado = st.selectbox(
        "Selecione o Ano",
        range(2020, 2031),
        index=range(2020, 2031).index(datetime.now().year),
        key="acomp_ano"
    )
    
    st.divider()
    
    # ===== RESUMO ANUAL =====
    st.subheader("📊 Resumo Anual do Orçamento")
    
    # Calcula dados de todos os meses
    dados_meses = []
    total_planejado_ano = 0
    total_utilizado_ano = 0
    total_disponivel_ano = 0
    
    for mes_num in range(1, 13):
        orcamentos_mes = OrcamentoService.listar_orcamentos(usuario.id, mes_num, ano_selecionado)
        
        total_planejado_mes = sum(orc['valor_planejado'] for orc in orcamentos_mes)
        total_utilizado_mes = sum(orc['valor_realizado'] for orc in orcamentos_mes)
        total_disponivel_mes = total_planejado_mes - total_utilizado_mes
        
        total_planejado_ano += total_planejado_mes
        total_utilizado_ano += total_utilizado_mes
        total_disponivel_ano += total_disponivel_mes
        
        dados_meses.append({
            'mes': mes_num,
            'mes_nome': formatador.mes_ano_formatado(mes_num, ano_selecionado).split(' de ')[0],
            'mes_abrev': formatador.mes_ano_formatado(mes_num, ano_selecionado).split(' de ')[0][:3],
            'planejado': total_planejado_mes,
            'utilizado': total_utilizado_mes,
            'disponivel': total_disponivel_mes,
            'percentual_utilizado': (total_utilizado_mes / total_planejado_mes * 100) if total_planejado_mes > 0 else 0,
            'tem_orcamento': len(orcamentos_mes) > 0
        })
    
    # KPIs do ano
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Total Planejado",
            formatador.formatar_moeda(total_planejado_ano)
        )
    
    with col2:
        st.metric(
            "💸 Total Utilizado",
            formatador.formatar_moeda(total_utilizado_ano)
        )
    
    with col3:
        cor_disponivel = "normal" if total_disponivel_ano >= 0 else "inverse"
        st.metric(
            "💵 Total Disponível",
            formatador.formatar_moeda(total_disponivel_ano),
            delta_color=cor_disponivel
        )
    
    with col4:
        percent_utilizado_ano = (total_utilizado_ano / total_planejado_ano * 100) if total_planejado_ano > 0 else 0
        st.metric(
            "📊 % Utilizado",
            f"{percent_utilizado_ano:.1f}%"
        )
    
    if total_planejado_ano == 0:
        st.warning("⚠️ Nenhum orçamento definido para este ano. Configure orçamentos na aba 'Planejamento'.")
        return
    
    st.divider()
    
    # ===== GRÁFICO: Disponível vs Utilizado por Mês =====
    st.subheader("📈 Orçamento Disponível Mês a Mês")
    
    df_meses = pd.DataFrame(dados_meses)
    
    # Gráfico de barras empilhadas
    fig_disponivel = go.Figure()
    
    fig_disponivel.add_trace(go.Bar(
        name='Utilizado',
        x=df_meses['mes_abrev'],
        y=df_meses['utilizado'],
        marker_color='#e74c3c',
        text=[formatador.formatar_moeda(v) for v in df_meses['utilizado']],
        textposition='inside',
        hovertemplate='<b>%{x}</b><br>Utilizado: R$ %{y:,.2f}<extra></extra>'
    ))
    
    fig_disponivel.add_trace(go.Bar(
        name='Disponível',
        x=df_meses['mes_abrev'],
        y=df_meses['disponivel'],
        marker_color='#27ae60',
        text=[formatador.formatar_moeda(v) for v in df_meses['disponivel']],
        textposition='inside',
        hovertemplate='<b>%{x}</b><br>Disponível: R$ %{y:,.2f}<extra></extra>'
    ))
    
    fig_disponivel.update_layout(
        barmode='stack',
        xaxis_title="Mês",
        yaxis_title="Valor (R$)",
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig_disponivel, use_container_width=True)
    
    # Análise rápida
    meses_com_saldo = len([d for d in dados_meses if d['disponivel'] > 0])
    meses_estourados = len([d for d in dados_meses if d['disponivel'] < 0])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if meses_com_saldo >= 6:
            st.success(f"✅ **{meses_com_saldo} meses** com orçamento disponível")
        else:
            st.info(f"💡 **{meses_com_saldo} meses** com orçamento disponível")
    
    with col2:
        if meses_estourados > 0:
            st.error(f"⚠️ **{meses_estourados} meses** estouraram o orçamento")
        else:
            st.success(f"✅ **{meses_estourados} meses** estouraram o orçamento")
    
    with col3:
        meses_sem_orcamento = len([d for d in dados_meses if not d['tem_orcamento']])
        if meses_sem_orcamento > 0:
            st.warning(f"⚠️ **{meses_sem_orcamento} meses** sem orçamento definido")
        else:
            st.success(f"✅ Todos os meses têm orçamento")
    
    st.divider()
    
    # ===== DETALHAMENTO MÊS A MÊS =====
    st.subheader("📋 Detalhamento Mês a Mês")
    
    # Tabs para cada mês
    tabs = st.tabs([d['mes_abrev'] for d in dados_meses])
    
    for idx, tab in enumerate(tabs):
        with tab:
            mes_dados = dados_meses[idx]
            mes_num = mes_dados['mes']
            
            if not mes_dados['tem_orcamento']:
                st.info(f"💡 Nenhum orçamento definido para {mes_dados['mes_nome']}. Configure na aba 'Planejamento'.")
                continue
            
            # KPIs do mês
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "💰 Planejado",
                    formatador.formatar_moeda(mes_dados['planejado'])
                )
            
            with col2:
                st.metric(
                    "💸 Utilizado",
                    formatador.formatar_moeda(mes_dados['utilizado']),
                    delta=f"{mes_dados['percentual_utilizado']:.1f}%"
                )
            
            with col3:
                cor = "normal" if mes_dados['disponivel'] >= 0 else "inverse"
                st.metric(
                    "💵 Disponível",
                    formatador.formatar_moeda(mes_dados['disponivel']),
                    delta_color=cor
                )
            
            # Barra de progresso
            progresso = min(mes_dados['percentual_utilizado'] / 100, 1.0)
            st.progress(progresso)
            
            st.markdown("---")
            
            # Detalhamento por categoria
            orcamentos_mes = OrcamentoService.listar_orcamentos(usuario.id, mes_num, ano_selecionado)
            
            if orcamentos_mes:
                st.markdown("#### 📊 Orçamento por Categoria")
                
                # Cria DataFrame
                df_cat = pd.DataFrame(orcamentos_mes)
                df_cat = df_cat.sort_values('diferenca', ascending=False)
                
                # Gráfico de barras horizontais
                fig_cat = go.Figure()
                
                # Barra do planejado (fundo)
                fig_cat.add_trace(go.Bar(
                    name='Planejado',
                    y=df_cat['categoria_nome'],
                    x=df_cat['valor_planejado'],
                    orientation='h',
                    marker_color='#3498db',
                    opacity=0.3,
                    hovertemplate='<b>%{y}</b><br>Planejado: R$ %{x:,.2f}<extra></extra>'
                ))
                
                # Barra do utilizado (frente)
                cores_utilizado = ['#e74c3c' if u > p else '#27ae60' 
                                   for u, p in zip(df_cat['valor_realizado'], df_cat['valor_planejado'])]
                
                fig_cat.add_trace(go.Bar(
                    name='Utilizado',
                    y=df_cat['categoria_nome'],
                    x=df_cat['valor_realizado'],
                    orientation='h',
                    marker_color=cores_utilizado,
                    text=[formatador.formatar_moeda(v) for v in df_cat['valor_realizado']],
                    textposition='inside',
                    hovertemplate='<b>%{y}</b><br>Utilizado: R$ %{x:,.2f}<extra></extra>'
                ))
                
                fig_cat.update_layout(
                    barmode='overlay',
                    xaxis_title="Valor (R$)",
                    height=max(300, len(df_cat) * 50),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig_cat, use_container_width=True)
                
                # Tabela detalhada
                st.markdown("#### 📋 Tabela Detalhada")
                
                tabela_display = pd.DataFrame({
                    'Categoria': df_cat['categoria_nome'],
                    'Planejado': [formatador.formatar_moeda(v) for v in df_cat['valor_planejado']],
                    'Utilizado': [formatador.formatar_moeda(v) for v in df_cat['valor_realizado']],
                    'Disponível': [formatador.formatar_moeda(v) for v in df_cat['diferenca']],
                    '% Usado': [f"{v:.1f}%" for v in df_cat['percentual_utilizado']],
                    'Status': ['🔴 Estourou' if d < 0 else '🟢 Disponível' if d > 0 else '⚖️ Exato' 
                              for d in df_cat['diferenca']]
                })
                
                st.dataframe(
                    tabela_display,
                    use_container_width=True,
                    hide_index=True,
                    height=min(400, (len(tabela_display) + 1) * 35 + 3)
                )
                
                # Alertas
                categorias_estouradas = df_cat[df_cat['diferenca'] < 0]
                categorias_disponiveis = df_cat[df_cat['diferenca'] > 0]
                
                if not categorias_estouradas.empty:
                    st.error(f"⚠️ **{len(categorias_estouradas)} categorias** estouraram o orçamento:")
                    for _, cat in categorias_estouradas.iterrows():
                        st.markdown(f"- **{cat['categoria_nome']}**: Estourou {formatador.formatar_moeda(abs(cat['diferenca']))}")
                
                if not categorias_disponiveis.empty:
                    total_disponivel_cat = categorias_disponiveis['diferenca'].sum()
                    st.success(f"✅ **{formatador.formatar_moeda(total_disponivel_cat)}** ainda disponível em {len(categorias_disponiveis)} categorias")
                    
                    # Top 3 com mais saldo
                    with st.expander("💰 Categorias com Maior Saldo Disponível"):
                        for _, cat in categorias_disponiveis.head(3).iterrows():
                            st.markdown(f"**{cat['categoria_nome']}**: {formatador.formatar_moeda(cat['diferenca'])} ({100 - cat['percentual_utilizado']:.1f}% não utilizado)")
    
    st.divider()
    
    # ===== ANÁLISE E INSIGHTS =====
    st.subheader("💡 Insights e Recomendações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Melhores Meses")
        
        # Meses com mais saldo disponível
        meses_ordenados = sorted([d for d in dados_meses if d['tem_orcamento']], 
                                 key=lambda x: x['disponivel'], reverse=True)[:3]
        
        for idx, mes in enumerate(meses_ordenados, 1):
            if mes['disponivel'] > 0:
                st.success(f"""
                **{idx}. {mes['mes_nome']}**
                - Disponível: {formatador.formatar_moeda(mes['disponivel'])}
                - Utilizado: {mes['percentual_utilizado']:.1f}%
                """)
    
    with col2:
        st.markdown("#### ⚠️ Meses de Atenção")
        
        # Meses que estouraram ou usaram quase tudo
        meses_atencao = sorted([d for d in dados_meses if d['tem_orcamento']], 
                               key=lambda x: x['disponivel'])[:3]
        
        for idx, mes in enumerate(meses_atencao, 1):
            if mes['disponivel'] < 0:
                st.error(f"""
                **{idx}. {mes['mes_nome']}**
                - Estourou: {formatador.formatar_moeda(abs(mes['disponivel']))}
                - Utilizado: {mes['percentual_utilizado']:.1f}%
                """)
            elif mes['percentual_utilizado'] > 95:
                st.warning(f"""
                **{idx}. {mes['mes_nome']}**
                - Disponível: {formatador.formatar_moeda(mes['disponivel'])}
                - Utilizado: {mes['percentual_utilizado']:.1f}%
                """)
    
    # Recomendações
    st.markdown("#### 📝 Recomendações")
    
    if total_disponivel_ano > 0:
        st.success(f"""
        ✅ **Situação Positiva**
        
        Você tem {formatador.formatar_moeda(total_disponivel_ano)} de orçamento disponível no ano.
        Isso representa {(total_disponivel_ano / total_planejado_ano * 100):.1f}% do orçamento total.
        
        **Sugestões:**
        - Considere investir o valor não utilizado
        - Ou ajuste o orçamento para ser mais realista
        - Mantenha uma reserva de emergência
        """)
    elif total_disponivel_ano < 0:
        st.error(f"""
        ⚠️ **Atenção Necessária**
        
        Você estourou o orçamento em {formatador.formatar_moeda(abs(total_disponivel_ano))} no ano.
        
        **Ações recomendadas:**
        - Revise as categorias que mais estouram
        - Ajuste o orçamento para valores realistas
        - Implemente controles mais rígidos
        - Identifique gastos desnecessários
        """)
    else:
        st.info(f"""
        ⚖️ **Equilíbrio Perfeito**
        
        Você utilizou exatamente o orçamento planejado!
        """)
