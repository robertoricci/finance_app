import streamlit as st
from services import AuthService


def mostrar_tela_autenticacao():
    """Tela de login e registro de usuários."""
    
    st.title("🏦 Sistema de Finanças Pessoais")
    
    tab_login, tab_registro = st.tabs(["Login", "Registrar-se"])
    
    with tab_login:
        st.subheader("Entrar no Sistema")
        
        with st.form("form_login"):
            email = st.text_input("Email", key="login_email")
            senha = st.text_input("Senha", type="password", key="login_senha")
            
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                if not email or not senha:
                    st.error("Por favor, preencha todos os campos!")
                else:
                    sucesso, mensagem, usuario = AuthService.autenticar_usuario(email, senha)
                    
                    if sucesso:
                        st.session_state['usuario'] = usuario
                        st.success(mensagem)
                        st.rerun()
                    else:
                        st.error(mensagem)
    
    with tab_registro:
        st.subheader("Criar Nova Conta")
        
        with st.form("form_registro"):
            nome = st.text_input("Nome Completo", key="reg_nome")
            email = st.text_input("Email", key="reg_email")
            senha = st.text_input("Senha", type="password", key="reg_senha")
            senha_conf = st.text_input("Confirmar Senha", type="password", key="reg_senha_conf")
            
            submit = st.form_submit_button("Registrar", use_container_width=True)
            
            if submit:
                if not nome or not email or not senha or not senha_conf:
                    st.error("Por favor, preencha todos os campos!")
                elif senha != senha_conf:
                    st.error("As senhas não coincidem!")
                elif len(senha) < 6:
                    st.error("A senha deve ter pelo menos 6 caracteres!")
                else:
                    sucesso, mensagem, usuario = AuthService.registrar_usuario(nome, email, senha)
                    
                    if sucesso:
                        st.success(mensagem + " Faça login para continuar.")
                    else:
                        st.error(mensagem)
