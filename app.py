import streamlit as st
from database import db_manager
from ui import (
    mostrar_tela_autenticacao,
    mostrar_dashboard,
    mostrar_categorias,
    mostrar_lancamentos,
    mostrar_planejamento,
    mostrar_relatorios
)


def configurar_pagina():
    """Configura as propriedades da página."""
    st.set_page_config(
        page_title="Ricci - Sistema de Finanças Pessoais",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def inicializar_banco():
    """Inicializa o banco de dados se necessário."""
    if db_manager.init_database():
        st.toast("✅ Banco de dados inicializado!", icon="✅")


def inicializar_sessao():
    """Inicializa variáveis de sessão."""
    if 'usuario' not in st.session_state:
        st.session_state['usuario'] = None


def criar_sidebar():
    """Cria a sidebar com menu de navegação."""
    usuario = st.session_state['usuario']
    
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/3498db/ffffff?text=Finanças", use_container_width=True)
        
        st.markdown(f"### Olá, {usuario.nome.split()[0]}! 👋")
        st.markdown(f"📧 {usuario.email}")
        
        st.divider()
        
        # Menu de navegação
        menu_opcoes = {
            "📊 Dashboard": "dashboard",
            "🏷️ Categorias": "categorias",
            "💳 Lançamentos": "lancamentos",
            "📋 Planejamento": "planejamento",
            "📄 Relatórios": "relatorios"
        }
        
        for label, key in menu_opcoes.items():
            if st.button(label, key=f"menu_{key}", use_container_width=True):
                st.session_state['pagina_atual'] = key
                st.rerun()
        
        st.divider()
        
        # Botão de logout
        if st.button("🚪 Sair", use_container_width=True, type="secondary"):
            st.session_state['usuario'] = None
            if 'pagina_atual' in st.session_state:
                del st.session_state['pagina_atual']
            st.rerun()
        
        st.divider()
        
        # Informações adicionais
        with st.expander("ℹ️ Sobre o Sistema"):
            st.markdown("""
            **Sistema de Finanças Pessoais**
            
            Versão: 1.0.0
            
            Desenvolvido para ajudar no controle e 
            planejamento de suas finanças pessoais.
            
            ### Funcionalidades:
            - ✅ Dashboard com indicadores
            - ✅ Gestão de categorias
            - ✅ Lançamentos financeiros
            - ✅ Planejamento e orçamentos
            - ✅ Relatórios em PDF
            - ✅ Sistema multiusuário
            """)


def main():
    """Função principal da aplicação."""
    configurar_pagina()
    inicializar_banco()
    inicializar_sessao()
    
    # Verifica autenticação
    if st.session_state['usuario'] is None:
        mostrar_tela_autenticacao()
    else:
        # Usuário autenticado
        criar_sidebar()
        
        # Define página inicial se não estiver definida
        if 'pagina_atual' not in st.session_state:
            st.session_state['pagina_atual'] = 'dashboard'
        
        # Roteamento de páginas
        pagina_atual = st.session_state['pagina_atual']
        
        if pagina_atual == 'dashboard':
            mostrar_dashboard()
        elif pagina_atual == 'categorias':
            mostrar_categorias()
        elif pagina_atual == 'lancamentos':
            mostrar_lancamentos()
        elif pagina_atual == 'planejamento':
            mostrar_planejamento()
        elif pagina_atual == 'relatorios':
            mostrar_relatorios()


if __name__ == "__main__":
    main()
