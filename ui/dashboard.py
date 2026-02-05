import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from services import LancamentoService, OrcamentoService, CategoriaService
from models.categoria import TipoCategoria
from utils.formatador import FormatadorBR


def mostrar_dashboard():
    """Dashboard principal com indicadores financeiros."""
    
    usuario = st.session_state['usuario']
    formatador = FormatadorBR()
    
    st.title(f"📊 Dashboard - {usuario.nome}")
    
    # Abas para visão mensal e anual
    tab_mensal, tab_anual = st.tabs(["📅 Visão Mensal", "📆 Visão Anual"])
    
    # ========== VISÃO MENSAL ==========
    with tab_mensal:
        mostrar_visao_mensal(usuario, formatador)
    
    # ========== VISÃO ANUAL ==========
    with tab_anual:
        mostrar_visao_anual(usuario, formatador)


def mostrar_visao_mensal(usuario, formatador):
    """Exibe a visão mensal do dashboard."""
    
    # Seletor de período
    col1, col2 = st.columns(2)
    
    with col1:
        mes = st.selectbox(
            "Mês",
            range(1, 13),
            index=datetime.now().month - 1,
            format_func=lambda x: formatador.mes_ano_formatado(x, 2024).split(' de ')[0],
            key="mensal_mes"
        )
    
    with col2:
        ano = st.selectbox(
            "Ano",
            range(2020, 2031),
            index=range(2020, 2031).index(datetime.now().year),
            key="mensal_ano"
        )
    
    st.divider()
    
    # Calcula totais do mês atual
    totais = LancamentoService.calcular_totais(usuario.id, mes, ano)
    
    # ===== SEÇÃO DE KPIs PRINCIPAIS =====
    st.subheader("💰 Resumo Financeiro do Mês")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💵 Total de Entradas",
            value=formatador.formatar_moeda(totais['total_entradas']),
            delta=None
        )
    
    with col2:
        st.metric(
            label="💸 Total de Despesas",
            value=formatador.formatar_moeda(totais['total_despesas']),
            delta=None
        )
    
    with col3:
        saldo = totais['saldo']
        st.metric(
            label="💵 Saldo do Mês",
            value=formatador.formatar_moeda(saldo),
            delta=None,
            delta_color="normal" if saldo >= 0 else "inverse"
        )
    
    with col4:
        # Percentual gasto vs entrada
        if totais['total_entradas'] > 0:
            percentual_gasto = (totais['total_despesas'] / totais['total_entradas']) * 100
        else:
            percentual_gasto = 0
        
        st.metric(
            label="📊 % Gasto",
            value=f"{percentual_gasto:.1f}%",
            delta=None
        )
    
    # Barra visual de saldo
    if totais['total_entradas'] > 0:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Cria barra de progresso customizada
            fig_barra = go.Figure()
            
            fig_barra.add_trace(go.Bar(
                x=[totais['total_entradas']],
                y=[''],
                orientation='h',
                name='Entrada',
                marker_color='#27ae60',
                text=[formatador.formatar_moeda(totais['total_entradas'])],
                textposition='inside',
                hoverinfo='text',
                hovertext=f"Entradas: {formatador.formatar_moeda(totais['total_entradas'])}"
            ))
            
            fig_barra.add_trace(go.Bar(
                x=[totais['total_despesas']],
                y=[''],
                orientation='h',
                name='Despesa',
                marker_color='#e74c3c',
                text=[formatador.formatar_moeda(totais['total_despesas'])],
                textposition='inside',
                hoverinfo='text',
                hovertext=f"Despesas: {formatador.formatar_moeda(totais['total_despesas'])}"
            ))
            
            fig_barra.update_layout(
                barmode='overlay',
                showlegend=True,
                height=120,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(showticklabels=False, showgrid=False),
                yaxis=dict(showticklabels=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_barra, use_container_width=True)
        
        with col2:
            # Status do saldo
            if saldo >= 0:
                st.success(f"✅ Saldo Positivo\n\n{formatador.formatar_moeda(saldo)}")
            else:
                st.error(f"⚠️ Saldo Negativo\n\n{formatador.formatar_moeda(saldo)}")
    
    st.divider()
    
    # ===== COMPARATIVO MENSAL (ÚLTIMOS 6 MESES) =====
    st.subheader("📈 Evolução Mensal - Últimos 6 Meses")
    
    # Calcula dados dos últimos 6 meses
    meses_dados = []
    data_atual = date(ano, mes, 1)
    
    for i in range(5, -1, -1):
        data_mes = data_atual - relativedelta(months=i)
        mes_num = data_mes.month
        ano_num = data_mes.year
        
        totais_mes = LancamentoService.calcular_totais(usuario.id, mes_num, ano_num)
        
        meses_dados.append({
            'mes': formatador.mes_ano_formatado(mes_num, ano_num).split(' de ')[0][:3],
            'mes_ano': f"{mes_num:02d}/{ano_num}",
            'entradas': totais_mes['total_entradas'],
            'despesas': totais_mes['total_despesas'],
            'saldo': totais_mes['saldo']
        })
    
    if meses_dados:
        df_meses = pd.DataFrame(meses_dados)
        
        # Gráfico de linhas - Entradas vs Despesas
        fig_evolucao = go.Figure()
        
        fig_evolucao.add_trace(go.Scatter(
            x=df_meses['mes'],
            y=df_meses['entradas'],
            mode='lines+markers+text',
            name='Entradas',
            line=dict(color='#27ae60', width=3),
            marker=dict(size=10),
            text=[formatador.formatar_moeda(v) for v in df_meses['entradas']],
            textposition='top center',
            textfont=dict(size=10)
        ))
        
        fig_evolucao.add_trace(go.Scatter(
            x=df_meses['mes'],
            y=df_meses['despesas'],
            mode='lines+markers+text',
            name='Despesas',
            line=dict(color='#e74c3c', width=3),
            marker=dict(size=10),
            text=[formatador.formatar_moeda(v) for v in df_meses['despesas']],
            textposition='bottom center',
            textfont=dict(size=10)
        ))
        
        fig_evolucao.update_layout(
            xaxis_title="Mês",
            yaxis_title="Valor (R$)",
            height=400,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_evolucao, use_container_width=True)
        
        # Gráfico de barras - Saldo mensal
        st.markdown("#### 💵 Saldo por Mês")
        
        fig_saldo = go.Figure()
        
        # Define cores baseadas no saldo (positivo/negativo)
        cores = ['#27ae60' if s >= 0 else '#e74c3c' for s in df_meses['saldo']]
        
        fig_saldo.add_trace(go.Bar(
            x=df_meses['mes'],
            y=df_meses['saldo'],
            marker_color=cores,
            text=[formatador.formatar_moeda(v) for v in df_meses['saldo']],
            textposition='outside',
            hoverinfo='text',
            hovertext=[f"{m}: {formatador.formatar_moeda(s)}" for m, s in zip(df_meses['mes'], df_meses['saldo'])]
        ))
        
        fig_saldo.update_layout(
            xaxis_title="Mês",
            yaxis_title="Saldo (R$)",
            height=350,
            showlegend=False
        )
        
        # Adiciona linha zero
        fig_saldo.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        st.plotly_chart(fig_saldo, use_container_width=True)
    
    st.divider()
    
    # ===== KPIs PROFISSIONAIS =====
    st.subheader("📊 Indicadores Financeiros Profissionais")
    
    # Obtém lançamentos do mês para cálculos
    lancamentos = LancamentoService.listar_lancamentos(usuario.id, mes, ano)
    
    if lancamentos:
        # Prepara dados
        entradas_mes = [l for l in lancamentos if l['categoria_tipo'] == TipoCategoria.ENTRADA]
        despesas_mes = [l for l in lancamentos if l['categoria_tipo'] == TipoCategoria.DESPESA]
        
        total_entradas_mes = sum(l['valor'] for l in entradas_mes)
        total_despesas_mes = sum(l['valor'] for l in despesas_mes)
        
        # ===== KPI 1: Distribuição de Despesas por Categoria =====
        st.markdown("#### 🎯 KPI 1: Distribuição de Despesas por Categoria")
        
        if despesas_mes:
            # Agrupa despesas por categoria
            despesas_por_categoria = {}
            for lanc in despesas_mes:
                cat = lanc['categoria_nome']
                if cat not in despesas_por_categoria:
                    despesas_por_categoria[cat] = {'valor': 0, 'cor': lanc['categoria_cor']}
                despesas_por_categoria[cat]['valor'] += lanc['valor']
            
            # Calcula percentuais
            df_dist = pd.DataFrame([
                {
                    'categoria': cat,
                    'valor': dados['valor'],
                    'percentual': (dados['valor'] / total_despesas_mes * 100),
                    'cor': dados['cor']
                }
                for cat, dados in despesas_por_categoria.items()
            ]).sort_values('valor', ascending=False)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Gráfico de Donut
                fig_donut = go.Figure(data=[go.Pie(
                    labels=df_dist['categoria'],
                    values=df_dist['valor'],
                    hole=0.5,
                    marker=dict(colors=df_dist['cor']),
                    texttemplate='%{label}<br>%{percent}',
                    hovertemplate='<b>%{label}</b><br>Valor: R$ %{value:,.2f}<br>Percentual: %{percent}<extra></extra>'
                )])
                
                fig_donut.update_layout(
                    title="Distribuição Percentual",
                    height=400,
                    annotations=[dict(
                        text=formatador.formatar_moeda(total_despesas_mes),
                        x=0.5, y=0.5,
                        font_size=16,
                        showarrow=False
                    )]
                )
                
                st.plotly_chart(fig_donut, use_container_width=True)
            
            with col2:
                st.markdown("**Interpretação:**")
                
                # Mostra top 3 categorias
                for idx, row in df_dist.head(3).iterrows():
                    st.markdown(f"""
                    **{idx+1}. {row['categoria']}**
                    - Valor: {formatador.formatar_moeda(row['valor'])}
                    - {row['percentual']:.1f}% do total
                    """)
                
                # Alerta se alguma categoria > 40%
                cat_alta = df_dist[df_dist['percentual'] > 40]
                if not cat_alta.empty:
                    st.warning(f"⚠️ **{cat_alta.iloc[0]['categoria']}** representa mais de 40% dos gastos!")
        else:
            st.info("Nenhuma despesa registrada neste período.")
        
        st.divider()
        
        # ===== KPI 2: Evolução Mensal de Gastos (Últimos 6 meses) =====
        st.markdown("#### 📈 KPI 2: Evolução Mensal de Gastos")
        
        # Calcula gastos dos últimos 6 meses
        evolucao_gastos = []
        data_atual = date(ano, mes, 1)
        
        for i in range(5, -1, -1):
            data_mes = data_atual - relativedelta(months=i)
            mes_num = data_mes.month
            ano_num = data_mes.year
            
            totais_mes = LancamentoService.calcular_totais(usuario.id, mes_num, ano_num)
            
            evolucao_gastos.append({
                'mes': formatador.mes_ano_formatado(mes_num, ano_num).split(' de ')[0][:3],
                'mes_completo': formatador.mes_ano_formatado(mes_num, ano_num),
                'gastos': totais_mes['total_despesas']
            })
        
        df_evolucao = pd.DataFrame(evolucao_gastos)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de Linha
            fig_evolucao_gastos = go.Figure()
            
            fig_evolucao_gastos.add_trace(go.Scatter(
                x=df_evolucao['mes'],
                y=df_evolucao['gastos'],
                mode='lines+markers',
                line=dict(color='#e74c3c', width=3),
                marker=dict(size=10, color='#c0392b'),
                fill='tozeroy',
                fillcolor='rgba(231, 76, 60, 0.1)',
                text=[formatador.formatar_moeda(v) for v in df_evolucao['gastos']],
                textposition='top center',
                hovertemplate='<b>%{x}</b><br>Gastos: R$ %{y:,.2f}<extra></extra>'
            ))
            
            fig_evolucao_gastos.update_layout(
                title="Tendência de Gastos",
                xaxis_title="Mês",
                yaxis_title="Gastos (R$)",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig_evolucao_gastos, use_container_width=True)
        
        with col2:
            st.markdown("**Interpretação:**")
            
            # Calcula tendência
            if len(df_evolucao) >= 2:
                variacao = df_evolucao['gastos'].iloc[-1] - df_evolucao['gastos'].iloc[0]
                variacao_percent = (variacao / df_evolucao['gastos'].iloc[0] * 100) if df_evolucao['gastos'].iloc[0] > 0 else 0
                
                if variacao > 0:
                    st.error(f"""
                    📈 **Tendência de Alta**
                    
                    Aumento de {formatador.formatar_moeda(variacao)} ({variacao_percent:+.1f}%)
                    
                    ⚠️ Atenção ao crescimento
                    """)
                elif variacao < 0:
                    st.success(f"""
                    📉 **Tendência de Queda**
                    
                    Redução de {formatador.formatar_moeda(abs(variacao))} ({variacao_percent:.1f}%)
                    
                    ✅ Controle melhorando
                    """)
                else:
                    st.info("📊 **Gastos Estáveis**")
                
                # Média
                media_gastos = df_evolucao['gastos'].mean()
                st.metric("Média dos 6 meses", formatador.formatar_moeda(media_gastos))
        
        st.divider()
        
        # ===== KPI 3: Fluxo de Caixa Mensal =====
        st.markdown("#### 💰 KPI 3: Fluxo de Caixa Mensal")
        
        fluxo_caixa = total_entradas_mes - total_despesas_mes
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de Barras Comparativo
            fig_fluxo = go.Figure()
            
            fig_fluxo.add_trace(go.Bar(
                name='Entradas',
                x=['Fluxo de Caixa'],
                y=[total_entradas_mes],
                marker_color='#27ae60',
                text=[formatador.formatar_moeda(total_entradas_mes)],
                textposition='inside',
                hovertemplate='Entradas: R$ %{y:,.2f}<extra></extra>'
            ))
            
            fig_fluxo.add_trace(go.Bar(
                name='Saídas',
                x=['Fluxo de Caixa'],
                y=[total_despesas_mes],
                marker_color='#e74c3c',
                text=[formatador.formatar_moeda(total_despesas_mes)],
                textposition='inside',
                hovertemplate='Saídas: R$ %{y:,.2f}<extra></extra>'
            ))
            
            # Adiciona linha do saldo
            fig_fluxo.add_trace(go.Scatter(
                name=f'Saldo: {formatador.formatar_moeda(fluxo_caixa)}',
                x=['Fluxo de Caixa'],
                y=[fluxo_caixa],
                mode='markers+text',
                marker=dict(
                    size=20,
                    color='#3498db',
                    symbol='diamond'
                ),
                text=[formatador.formatar_moeda(fluxo_caixa)],
                textposition='top center',
                hovertemplate='Saldo: R$ %{y:,.2f}<extra></extra>'
            ))
            
            fig_fluxo.update_layout(
                title="Entradas vs Saídas",
                yaxis_title="Valor (R$)",
                height=400,
                barmode='group'
            )
            
            st.plotly_chart(fig_fluxo, use_container_width=True)
        
        with col2:
            st.markdown("**Interpretação:**")
            
            if fluxo_caixa > 0:
                st.success(f"""
                ✅ **SUPERÁVIT**
                
                {formatador.formatar_moeda(fluxo_caixa)}
                
                Você gastou menos que recebeu!
                """)
            elif fluxo_caixa < 0:
                st.error(f"""
                ⚠️ **DÉFICIT**
                
                {formatador.formatar_moeda(fluxo_caixa)}
                
                Você gastou mais que recebeu!
                """)
            else:
                st.info("⚖️ **EQUILÍBRIO**\n\nEntradas = Saídas")
            
            # Taxa de economia
            if total_entradas_mes > 0:
                taxa_economia = (fluxo_caixa / total_entradas_mes * 100)
                st.metric("Taxa de Economia", f"{taxa_economia:.1f}%")
        
        st.divider()
        
        # ===== KPI 4: Percentual de Comprometimento da Renda =====
        st.markdown("#### ⚠️ KPI 4: Comprometimento da Renda")
        
        if total_entradas_mes > 0:
            comprometimento = (total_despesas_mes / total_entradas_mes * 100)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Gauge (Velocímetro)
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=comprometimento,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Comprometimento (%)"},
                    delta={'reference': 50, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
                    gauge={
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "darkblue"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 50], 'color': '#27ae60'},
                            {'range': [50, 70], 'color': '#f39c12'},
                            {'range': [70, 100], 'color': '#e74c3c'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                
                fig_gauge.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with col2:
                st.markdown("**Interpretação:**")
                
                if comprometimento <= 50:
                    st.success(f"""
                    ✅ **SAUDÁVEL**
                    
                    {comprometimento:.1f}% da renda comprometida
                    
                    Excelente controle financeiro!
                    """)
                elif comprometimento <= 70:
                    st.warning(f"""
                    ⚠️ **ATENÇÃO**
                    
                    {comprometimento:.1f}% da renda comprometida
                    
                    Monitore seus gastos.
                    """)
                else:
                    st.error(f"""
                    🔴 **RISCO ALTO**
                    
                    {comprometimento:.1f}% da renda comprometida
                    
                    Reduza despesas urgente!
                    """)
                
                st.markdown(f"""
                **Referências:**
                - 0-50%: Saudável 🟢
                - 50-70%: Atenção 🟡
                - 70-100%: Risco 🔴
                """)
        else:
            st.info("⚠️ Sem entradas registradas neste período.")
        
        st.divider()
        
        # ===== KPI 5: Saldo Acumulado (Últimos 6 meses) =====
        st.markdown("#### 📊 KPI 5: Saldo Acumulado")
        
        # Calcula saldo acumulado dos últimos 6 meses
        saldos_acumulados = []
        saldo_acumulado = 0
        data_atual = date(ano, mes, 1)
        
        for i in range(5, -1, -1):
            data_mes = data_atual - relativedelta(months=i)
            mes_num = data_mes.month
            ano_num = data_mes.year
            
            totais_mes = LancamentoService.calcular_totais(usuario.id, mes_num, ano_num)
            saldo_acumulado += totais_mes['saldo']
            
            saldos_acumulados.append({
                'mes': formatador.mes_ano_formatado(mes_num, ano_num).split(' de ')[0][:3],
                'saldo_mensal': totais_mes['saldo'],
                'saldo_acumulado': saldo_acumulado
            })
        
        df_acumulado = pd.DataFrame(saldos_acumulados)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de Área
            fig_acumulado = go.Figure()
            
            fig_acumulado.add_trace(go.Scatter(
                x=df_acumulado['mes'],
                y=df_acumulado['saldo_acumulado'],
                mode='lines+markers',
                line=dict(color='#3498db', width=3),
                marker=dict(size=10),
                fill='tozeroy',
                fillcolor='rgba(52, 152, 219, 0.2)',
                text=[formatador.formatar_moeda(v) for v in df_acumulado['saldo_acumulado']],
                textposition='top center',
                hovertemplate='<b>%{x}</b><br>Saldo Acumulado: R$ %{y:,.2f}<extra></extra>'
            ))
            
            fig_acumulado.update_layout(
                title="Evolução do Capital",
                xaxis_title="Mês",
                yaxis_title="Saldo Acumulado (R$)",
                height=400,
                showlegend=False
            )
            
            # Linha zero
            fig_acumulado.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
            
            st.plotly_chart(fig_acumulado, use_container_width=True)
        
        with col2:
            st.markdown("**Interpretação:**")
            
            saldo_inicial = df_acumulado['saldo_acumulado'].iloc[0]
            saldo_final = df_acumulado['saldo_acumulado'].iloc[-1]
            variacao_capital = saldo_final - saldo_inicial
            
            if variacao_capital > 0:
                st.success(f"""
                📈 **CRESCIMENTO**
                
                +{formatador.formatar_moeda(variacao_capital)}
                
                Capacidade de poupança!
                """)
            elif variacao_capital < 0:
                st.error(f"""
                📉 **QUEDA**
                
                {formatador.formatar_moeda(variacao_capital)}
                
                Consumo excessivo!
                """)
            else:
                st.info("⚖️ **ESTÁVEL**")
            
            st.metric(
                "Saldo Atual (6 meses)",
                formatador.formatar_moeda(saldo_final)
            )
            
            # Taxa de crescimento
            if saldo_inicial != 0:
                taxa_crescimento = (variacao_capital / abs(saldo_inicial) * 100)
                st.metric("Crescimento", f"{taxa_crescimento:+.1f}%")
    else:
        st.info("📭 Nenhum lançamento registrado neste período. Cadastre entradas e despesas para visualizar os KPIs.")
    
    st.divider()
    
    # ===== GRÁFICOS DO MÊS ATUAL =====
    st.subheader(f"📊 Detalhamento de {formatador.mes_ano_formatado(mes, ano)}")
    
    # Obtém dados para gráficos
    lancamentos = LancamentoService.listar_lancamentos(usuario.id, mes, ano)
    
    if lancamentos:
        # Gráficos em duas colunas
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Despesas por Categoria")
            
            # Filtra apenas despesas
            despesas = [l for l in lancamentos if l['categoria_tipo'] == TipoCategoria.DESPESA]
            
            if despesas:
                # Agrupa por categoria
                df_despesas = pd.DataFrame([
                    {
                        'categoria': l['categoria_nome'],
                        'valor': l['valor'],
                        'cor': l['categoria_cor']
                    }
                    for l in despesas
                ])
                
                df_group = df_despesas.groupby('categoria').agg({
                    'valor': 'sum',
                    'cor': 'first'
                }).reset_index()
                
                # Gráfico de pizza
                fig = px.pie(
                    df_group,
                    values='valor',
                    names='categoria',
                    color='categoria',
                    color_discrete_map={row['categoria']: row['cor'] for _, row in df_group.iterrows()}
                )
                
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(showlegend=False, height=400)
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhuma despesa registrada neste período.")
        
        with col2:
            st.subheader("Comparativo Entrada vs Despesa")
            
            # Gráfico de barras
            df_comparativo = pd.DataFrame({
                'Tipo': ['Entradas', 'Despesas'],
                'Valor': [totais['total_entradas'], totais['total_despesas']],
                'Cor': ['#27ae60', '#e74c3c']
            })
            
            fig = go.Figure(data=[
                go.Bar(
                    x=df_comparativo['Tipo'],
                    y=df_comparativo['Valor'],
                    marker_color=df_comparativo['Cor'],
                    text=[formatador.formatar_moeda(v) for v in df_comparativo['Valor']],
                    textposition='outside'
                )
            ])
            
            fig.update_layout(
                yaxis_title="Valor (R$)",
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📭 Nenhum lançamento registrado neste período.")
    
    st.divider()
    
    # Orçamento vs Realizado
    orcamentos = OrcamentoService.listar_orcamentos(usuario.id, mes, ano)
    
    if orcamentos:
        st.subheader("📋 Orçamento vs Realizado")
        
        df_orcamento = pd.DataFrame(orcamentos)
        
        # Gráfico de barras agrupadas
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Planejado',
            x=df_orcamento['categoria_nome'],
            y=df_orcamento['valor_planejado'],
            marker_color='#3498db',
            text=[formatador.formatar_moeda(v) for v in df_orcamento['valor_planejado']],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='Realizado',
            x=df_orcamento['categoria_nome'],
            y=df_orcamento['valor_realizado'],
            marker_color='#e67e22',
            text=[formatador.formatar_moeda(v) for v in df_orcamento['valor_realizado']],
            textposition='outside'
        ))
        
        fig.update_layout(
            barmode='group',
            yaxis_title="Valor (R$)",
            xaxis_title="Categoria",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela detalhada
        st.dataframe(
            df_orcamento[[
                'categoria_nome',
                'valor_planejado',
                'valor_realizado',
                'percentual_utilizado',
                'diferenca'
            ]].rename(columns={
                'categoria_nome': 'Categoria',
                'valor_planejado': 'Planejado',
                'valor_realizado': 'Realizado',
                'percentual_utilizado': '% Utilizado',
                'diferenca': 'Diferença'
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("💡 Configure seu orçamento mensal na aba 'Planejamento' para acompanhar suas metas!")


def mostrar_visao_anual(usuario, formatador):
    """Exibe a visão anual com análise mês a mês."""
    
    # Seletor de ano
    ano_selecionado = st.selectbox(
        "Selecione o Ano",
        range(2020, 2031),
        index=range(2020, 2031).index(datetime.now().year),
        key="anual_ano"
    )
    
    st.divider()
    
    # Calcula dados de todos os meses do ano
    dados_ano = []
    total_anual_entradas = 0
    total_anual_despesas = 0
    total_anual_planejado = 0
    
    for mes_num in range(1, 13):
        # Totais do mês
        totais_mes = LancamentoService.calcular_totais(usuario.id, mes_num, ano_selecionado)
        
        # Orçamento do mês
        orcamentos_mes = OrcamentoService.listar_orcamentos(usuario.id, mes_num, ano_selecionado)
        planejado_mes = sum(orc['valor_planejado'] for orc in orcamentos_mes)
        
        # Calcula diferença do planejado
        diferenca_planejado = planejado_mes - totais_mes['total_despesas']
        
        dados_ano.append({
            'mes': mes_num,
            'mes_nome': formatador.mes_ano_formatado(mes_num, ano_selecionado).split(' de ')[0],
            'mes_abrev': formatador.mes_ano_formatado(mes_num, ano_selecionado).split(' de ')[0][:3],
            'entradas': totais_mes['total_entradas'],
            'despesas': totais_mes['total_despesas'],
            'saldo': totais_mes['saldo'],
            'planejado': planejado_mes,
            'diferenca_planejado': diferenca_planejado,
            'percentual_gasto': (totais_mes['total_despesas'] / totais_mes['total_entradas'] * 100) if totais_mes['total_entradas'] > 0 else 0
        })
        
        total_anual_entradas += totais_mes['total_entradas']
        total_anual_despesas += totais_mes['total_despesas']
        total_anual_planejado += planejado_mes
    
    df_ano = pd.DataFrame(dados_ano)
    
    # ===== KPIs ANUAIS =====
    st.subheader(f"📊 Resumo Anual de {ano_selecionado}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total de Entradas",
            value=formatador.formatar_moeda(total_anual_entradas)
        )
    
    with col2:
        st.metric(
            label="💸 Total de Despesas",
            value=formatador.formatar_moeda(total_anual_despesas)
        )
    
    with col3:
        saldo_anual = total_anual_entradas - total_anual_despesas
        st.metric(
            label="💵 Saldo Anual",
            value=formatador.formatar_moeda(saldo_anual),
            delta_color="normal" if saldo_anual >= 0 else "inverse"
        )
    
    with col4:
        media_mensal = saldo_anual / 12
        st.metric(
            label="📊 Média Mensal",
            value=formatador.formatar_moeda(media_mensal)
        )
    
    st.divider()
    
    # ===== GRÁFICOS ANUAIS =====
    st.subheader("📈 Análise Gráfica do Ano")
    
    # Gráfico 1: Entradas vs Despesas (Área)
    st.markdown("#### 💰 Fluxo de Caixa Mensal")
    
    fig_area = go.Figure()
    
    fig_area.add_trace(go.Scatter(
        x=df_ano['mes_abrev'],
        y=df_ano['entradas'],
        mode='lines+markers',
        name='Entradas',
        fill='tozeroy',
        line=dict(color='#27ae60', width=2),
        marker=dict(size=8),
        hovertemplate='%{x}<br>Entradas: R$ %{y:,.2f}<extra></extra>'
    ))
    
    fig_area.add_trace(go.Scatter(
        x=df_ano['mes_abrev'],
        y=df_ano['despesas'],
        mode='lines+markers',
        name='Despesas',
        fill='tozeroy',
        line=dict(color='#e74c3c', width=2),
        marker=dict(size=8),
        hovertemplate='%{x}<br>Despesas: R$ %{y:,.2f}<extra></extra>'
    ))
    
    fig_area.update_layout(
        xaxis_title="Mês",
        yaxis_title="Valor (R$)",
        height=400,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_area, use_container_width=True)
    
    # Gráfico 2: Saldo Mensal (Barras)
    st.markdown("#### 💵 Saldo Mês a Mês")
    
    fig_saldo = go.Figure()
    
    cores_saldo = ['#27ae60' if s >= 0 else '#e74c3c' for s in df_ano['saldo']]
    
    fig_saldo.add_trace(go.Bar(
        x=df_ano['mes_abrev'],
        y=df_ano['saldo'],
        marker_color=cores_saldo,
        text=[formatador.formatar_moeda(v) for v in df_ano['saldo']],
        textposition='outside',
        hovertemplate='%{x}<br>Saldo: R$ %{y:,.2f}<extra></extra>'
    ))
    
    fig_saldo.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig_saldo.update_layout(
        xaxis_title="Mês",
        yaxis_title="Saldo (R$)",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_saldo, use_container_width=True)
    
    # Gráfico 3: Planejado vs Realizado
    if total_anual_planejado > 0:
        st.markdown("#### 📋 Orçamento Planejado vs Realizado")
        
        fig_planejado = go.Figure()
        
        fig_planejado.add_trace(go.Scatter(
            x=df_ano['mes_abrev'],
            y=df_ano['planejado'],
            mode='lines+markers',
            name='Planejado',
            line=dict(color='#3498db', width=2, dash='dash'),
            marker=dict(size=8),
            hovertemplate='%{x}<br>Planejado: R$ %{y:,.2f}<extra></extra>'
        ))
        
        fig_planejado.add_trace(go.Scatter(
            x=df_ano['mes_abrev'],
            y=df_ano['despesas'],
            mode='lines+markers',
            name='Realizado',
            line=dict(color='#e67e22', width=2),
            marker=dict(size=8),
            hovertemplate='%{x}<br>Realizado: R$ %{y:,.2f}<extra></extra>'
        ))
        
        fig_planejado.update_layout(
            xaxis_title="Mês",
            yaxis_title="Valor (R$)",
            height=400,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_planejado, use_container_width=True)
    
    # Gráfico 4: % Gasto por Mês (Gauge)
    st.markdown("#### 📊 Percentual de Gastos Mensal")
    
    fig_percent = go.Figure()
    
    fig_percent.add_trace(go.Bar(
        x=df_ano['mes_abrev'],
        y=df_ano['percentual_gasto'],
        marker=dict(
            color=df_ano['percentual_gasto'],
            colorscale=[[0, '#27ae60'], [0.5, '#f39c12'], [1, '#e74c3c']],
            showscale=True,
            colorbar=dict(title="% Gasto")
        ),
        text=[f"{v:.1f}%" for v in df_ano['percentual_gasto']],
        textposition='outside',
        hovertemplate='%{x}<br>% Gasto: %{y:.1f}%<extra></extra>'
    ))
    
    fig_percent.add_hline(y=100, line_dash="dash", line_color="red", opacity=0.5, 
                          annotation_text="100% (Gastou tudo)")
    
    fig_percent.update_layout(
        xaxis_title="Mês",
        yaxis_title="% Gasto",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_percent, use_container_width=True)
    
    # Gráfico 5: Controle Orçamentário (Barras Empilhadas)
    st.markdown("#### 🎯 Controle Orçamentário Mensal")
    
    fig_controle = go.Figure()
    
    # Para cada mês, mostra 3 barras: Entrada, Despesa Realizada, Despesa Planejada
    meses_labels = df_ano['mes_abrev'].tolist()
    
    # Barra 1: Entradas (base)
    fig_controle.add_trace(go.Bar(
        name='Entradas',
        x=meses_labels,
        y=df_ano['entradas'],
        marker_color='#27ae60',
        text=[formatador.formatar_moeda(v) for v in df_ano['entradas']],
        textposition='inside',
        hovertemplate='Entradas: R$ %{y:,.2f}<extra></extra>'
    ))
    
    # Barra 2: Despesas Realizadas
    fig_controle.add_trace(go.Bar(
        name='Despesas Realizadas',
        x=meses_labels,
        y=df_ano['despesas'],
        marker_color='#e74c3c',
        text=[formatador.formatar_moeda(v) for v in df_ano['despesas']],
        textposition='inside',
        hovertemplate='Despesas: R$ %{y:,.2f}<extra></extra>'
    ))
    
    # Barra 3: Orçamento Planejado (se houver)
    if total_anual_planejado > 0:
        fig_controle.add_trace(go.Bar(
            name='Orçamento Planejado',
            x=meses_labels,
            y=df_ano['planejado'],
            marker_color='#3498db',
            marker_pattern_shape="/",
            text=[formatador.formatar_moeda(v) for v in df_ano['planejado']],
            textposition='inside',
            hovertemplate='Planejado: R$ %{y:,.2f}<extra></extra>'
        ))
    
    fig_controle.update_layout(
        barmode='group',
        xaxis_title="Mês",
        yaxis_title="Valor (R$)",
        height=450,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_controle, use_container_width=True)
    
    # Indicadores de alerta
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Quantos meses gastou mais que recebeu
        meses_negativo = len([s for s in df_ano['saldo'] if s < 0])
        if meses_negativo > 0:
            st.warning(f"⚠️ **{meses_negativo} meses** gastando mais que recebendo")
        else:
            st.success(f"✅ **0 meses** gastando mais que recebendo")
    
    with col2:
        # Quantos meses estourou orçamento
        if total_anual_planejado > 0:
            meses_estouro = len([d for d in df_ano['diferenca_planejado'] if d < 0])
            if meses_estouro > 0:
                st.warning(f"⚠️ **{meses_estouro} meses** acima do orçamento")
            else:
                st.success(f"✅ **0 meses** acima do orçamento")
        else:
            st.info("💡 Configure orçamentos para ver análise")
    
    with col3:
        # Média de % gasto
        media_percent = df_ano['percentual_gasto'].mean()
        if media_percent > 90:
            st.error(f"⚠️ Média de **{media_percent:.1f}%** gasto")
        elif media_percent > 75:
            st.warning(f"⚠️ Média de **{media_percent:.1f}%** gasto")
        else:
            st.success(f"✅ Média de **{media_percent:.1f}%** gasto")
    
    st.divider()
    
    # Gráfico 6: Análise de Desvios (se houver orçamento)
    if total_anual_planejado > 0:
        st.markdown("#### 📉 Análise de Desvios do Orçamento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de Waterfall - Desvios mensais
            fig_desvios = go.Figure()
            
            # Calcula desvios (positivo = economizou, negativo = estourou)
            desvios = df_ano['diferenca_planejado'].tolist()
            cores_desvios = ['#27ae60' if d >= 0 else '#e74c3c' for d in desvios]
            
            fig_desvios.add_trace(go.Bar(
                x=df_ano['mes_abrev'],
                y=desvios,
                marker_color=cores_desvios,
                text=[formatador.formatar_moeda(v) for v in desvios],
                textposition='outside',
                hovertemplate='%{x}<br>Desvio: R$ %{y:,.2f}<extra></extra>',
                showlegend=False
            ))
            
            fig_desvios.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Adiciona anotações
            fig_desvios.add_annotation(
                x=0.5, y=1.15,
                xref="paper", yref="paper",
                text="🟢 Acima da linha = Economizou | 🔴 Abaixo = Estourou",
                showarrow=False,
                font=dict(size=10)
            )
            
            fig_desvios.update_layout(
                xaxis_title="Mês",
                yaxis_title="Desvio (R$)",
                height=400
            )
            
            st.plotly_chart(fig_desvios, use_container_width=True)
        
        with col2:
            # Gráfico de Pizza - Distribuição de controle
            meses_sob_controle = len([d for d in desvios if d >= 0])
            meses_fora_controle = len([d for d in desvios if d < 0])
            
            fig_pizza_controle = go.Figure(data=[go.Pie(
                labels=['✅ Dentro do Orçamento', '⚠️ Acima do Orçamento'],
                values=[meses_sob_controle, meses_fora_controle],
                marker_colors=['#27ae60', '#e74c3c'],
                hole=0.4,
                textinfo='label+percent+value',
                texttemplate='%{label}<br>%{value} meses<br>(%{percent})',
                hovertemplate='%{label}<br>%{value} meses<br>%{percent}<extra></extra>'
            )])
            
            fig_pizza_controle.update_layout(
                title_text="Controle Orçamentário do Ano",
                height=400,
                annotations=[dict(
                    text=f'{meses_sob_controle}/12',
                    x=0.5, y=0.5,
                    font_size=24,
                    showarrow=False
                )]
            )
            
            st.plotly_chart(fig_pizza_controle, use_container_width=True)
        
        # Estatísticas de desvio
        st.markdown("##### 📊 Estatísticas de Desvio")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_desvio = sum(desvios)
        maior_economia = max(desvios)
        maior_estouro = min(desvios)
        desvio_medio = sum(desvios) / len(desvios)
        
        with col1:
            if total_desvio >= 0:
                st.success(f"**Desvio Total**\n\n{formatador.formatar_moeda(total_desvio)}\n\n✅ Economia geral")
            else:
                st.error(f"**Desvio Total**\n\n{formatador.formatar_moeda(total_desvio)}\n\n⚠️ Estouro geral")
        
        with col2:
            mes_maior_economia = df_ano.loc[df_ano['diferenca_planejado'].idxmax(), 'mes_nome']
            st.info(f"**Maior Economia**\n\n{formatador.formatar_moeda(maior_economia)}\n\n📅 {mes_maior_economia}")
        
        with col3:
            mes_maior_estouro = df_ano.loc[df_ano['diferenca_planejado'].idxmin(), 'mes_nome']
            if maior_estouro < 0:
                st.warning(f"**Maior Estouro**\n\n{formatador.formatar_moeda(maior_estouro)}\n\n📅 {mes_maior_estouro}")
            else:
                st.success(f"**Maior Estouro**\n\n{formatador.formatar_moeda(maior_estouro)}\n\n✅ Sem estouros")
        
        with col4:
            if desvio_medio >= 0:
                st.success(f"**Desvio Médio**\n\n{formatador.formatar_moeda(desvio_medio)}\n\n✅ Positivo")
            else:
                st.error(f"**Desvio Médio**\n\n{formatador.formatar_moeda(desvio_medio)}\n\n⚠️ Negativo")
    
    st.divider()
    
    # Gráfico 7: Gasto vs Renda (Semáforo)
    st.markdown("#### 🚦 Semáforo Financeiro - Gasto vs Renda")
    
    fig_semaforo = go.Figure()
    
    # Para cada mês, calcula a diferença entre despesa e entrada
    diferencas = [entrada - despesa for entrada, despesa in zip(df_ano['entradas'], df_ano['despesas'])]
    
    # Define cores baseadas na diferença
    cores_semaforo = []
    for diff, entrada in zip(diferencas, df_ano['entradas']):
        if diff < 0:  # Gastou mais que recebeu
            cores_semaforo.append('#e74c3c')  # Vermelho
        elif diff < entrada * 0.10:  # Economizou menos de 10%
            cores_semaforo.append('#f39c12')  # Amarelo
        else:  # Economizou 10% ou mais
            cores_semaforo.append('#27ae60')  # Verde
    
    fig_semaforo.add_trace(go.Bar(
        x=df_ano['mes_abrev'],
        y=diferencas,
        marker_color=cores_semaforo,
        text=[formatador.formatar_moeda(v) for v in diferencas],
        textposition='outside',
        hovertemplate='%{x}<br>Diferença: R$ %{y:,.2f}<extra></extra>',
        showlegend=False
    ))
    
    fig_semaforo.add_hline(y=0, line_dash="solid", line_color="black", line_width=2)
    
    # Adiciona legendas
    fig_semaforo.add_annotation(
        x=0.15, y=1.12,
        xref="paper", yref="paper",
        text="🔴 Negativo = Gastou mais | 🟡 0-10% sobra | 🟢 +10% sobra",
        showarrow=False,
        font=dict(size=11)
    )
    
    fig_semaforo.update_layout(
        xaxis_title="Mês",
        yaxis_title="Diferença Renda - Gasto (R$)",
        height=400
    )
    
    st.plotly_chart(fig_semaforo, use_container_width=True)
    
    # Análise do semáforo
    meses_vermelho = len([c for c in cores_semaforo if c == '#e74c3c'])
    meses_amarelo = len([c for c in cores_semaforo if c == '#f39c12'])
    meses_verde = len([c for c in cores_semaforo if c == '#27ae60'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if meses_vermelho > 0:
            st.error(f"""
            **🔴 Vermelho: {meses_vermelho} meses**
            
            Gastando mais que recebe
            
            ⚠️ Atenção urgente necessária!
            """)
        else:
            st.success(f"""
            **🔴 Vermelho: {meses_vermelho} meses**
            
            Parabéns! Nenhum mês no vermelho
            """)
    
    with col2:
        if meses_amarelo > 0:
            st.warning(f"""
            **🟡 Amarelo: {meses_amarelo} meses**
            
            Economizando pouco (menos de 10%)
            
            💡 Pode melhorar
            """)
        else:
            st.success(f"""
            **🟡 Amarelo: {meses_amarelo} meses**
            
            Sem meses em alerta
            """)
    
    with col3:
        if meses_verde >= 6:
            st.success(f"""
            **🟢 Verde: {meses_verde} meses**
            
            Ótimo controle! Economizando +10%
            
            ✅ Continue assim!
            """)
        elif meses_verde > 0:
            st.info(f"""
            **🟢 Verde: {meses_verde} meses**
            
            Economizando +10%
            
            💪 Bom trabalho!
            """)
        else:
            st.error(f"""
            **🟢 Verde: {meses_verde} meses**
            
            Nenhum mês economizando bem
            
            ⚠️ Precisa melhorar
            """)
    
    st.divider()
    
    # ===== TABELA DETALHADA =====
    st.subheader("📋 Tabela Detalhada Mês a Mês")
    
    # Prepara dados para a tabela
    tabela_dados = df_ano.copy()
    
    # Formata valores
    tabela_display = pd.DataFrame({
        'Mês': tabela_dados['mes_nome'],
        'Entradas': [formatador.formatar_moeda(v) for v in tabela_dados['entradas']],
        'Despesas': [formatador.formatar_moeda(v) for v in tabela_dados['despesas']],
        'Saldo': [formatador.formatar_moeda(v) for v in tabela_dados['saldo']],
        'Planejado': [formatador.formatar_moeda(v) for v in tabela_dados['planejado']],
        'Dif. Planejado': [formatador.formatar_moeda(v) for v in tabela_dados['diferenca_planejado']],
        '% Gasto': [f"{v:.1f}%" for v in tabela_dados['percentual_gasto']]
    })
    
    # Adiciona linha de totais
    totais_row = pd.DataFrame({
        'Mês': ['TOTAL'],
        'Entradas': [formatador.formatar_moeda(total_anual_entradas)],
        'Despesas': [formatador.formatar_moeda(total_anual_despesas)],
        'Saldo': [formatador.formatar_moeda(saldo_anual)],
        'Planejado': [formatador.formatar_moeda(total_anual_planejado)],
        'Dif. Planejado': [formatador.formatar_moeda(total_anual_planejado - total_anual_despesas)],
        '% Gasto': [f"{(total_anual_despesas / total_anual_entradas * 100):.1f}%" if total_anual_entradas > 0 else "0%"]
    })
    
    tabela_completa = pd.concat([tabela_display, totais_row], ignore_index=True)
    
    # Exibe a tabela com estilo
    st.dataframe(
        tabela_completa,
        use_container_width=True,
        hide_index=True,
        height=500
    )
    
    # Download da tabela
    csv = tabela_completa.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Tabela em CSV",
        data=csv,
        file_name=f"relatorio_anual_{ano_selecionado}.csv",
        mime="text/csv",
    )
    
    st.divider()
    
    # ===== INSIGHTS =====
    st.subheader("💡 Insights do Ano")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Melhor mês
        melhor_mes = df_ano.loc[df_ano['saldo'].idxmax()]
        st.success(f"""
        **✅ Melhor Mês**
        
        {melhor_mes['mes_nome']}
        
        Saldo: {formatador.formatar_moeda(melhor_mes['saldo'])}
        """)
    
    with col2:
        # Pior mês
        pior_mes = df_ano.loc[df_ano['saldo'].idxmin()]
        st.error(f"""
        **⚠️ Pior Mês**
        
        {pior_mes['mes_nome']}
        
        Saldo: {formatador.formatar_moeda(pior_mes['saldo'])}
        """)
    
    with col3:
        # Mês mais econômico
        if total_anual_planejado > 0:
            mais_economico = df_ano.loc[df_ano['diferenca_planejado'].idxmax()]
            st.info(f"""
            **💰 Mais Econômico**
            
            {mais_economico['mes_nome']}
            
            Economizou: {formatador.formatar_moeda(mais_economico['diferenca_planejado'])}
            """)
        else:
            st.info("💡 Configure orçamentos para ver análise de economia")
