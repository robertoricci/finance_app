import streamlit as st
from services import CategoriaService
from models.categoria import TipoCategoria


def mostrar_categorias():
    """Tela de gerenciamento de categorias."""
    
    usuario = st.session_state['usuario']
    
    st.title("🏷️ Gerenciar Categorias")
    
    tab_listar, tab_criar = st.tabs(["Minhas Categorias", "Nova Categoria"])
    
    with tab_listar:
        st.subheader("Categorias Cadastradas")
        
        # Filtro por tipo
        filtro_tipo = st.radio(
            "Filtrar por tipo:",
            ["Todas", "Despesas", "Entradas"],
            horizontal=True
        )
        
        tipo_filtro = None
        if filtro_tipo == "Despesas":
            tipo_filtro = TipoCategoria.DESPESA
        elif filtro_tipo == "Entradas":
            tipo_filtro = TipoCategoria.ENTRADA
        
        categorias = CategoriaService.listar_categorias(usuario.id, tipo_filtro)
        
        if categorias:
            # Agrupa por tipo
            despesas = [c for c in categorias if c['tipo'] == TipoCategoria.DESPESA]
            entradas = [c for c in categorias if c['tipo'] == TipoCategoria.ENTRADA]
            
            if not tipo_filtro or tipo_filtro == TipoCategoria.DESPESA:
                if despesas:
                    st.markdown("### 💸 Categorias de Despesa")
                    
                    for cat in despesas:
                        col1, col2, col3, col4 = st.columns([0.1, 3, 1, 1])
                        
                        with col1:
                            st.markdown(f'<div style="background-color: {cat["cor"]}; width: 30px; height: 30px; border-radius: 5px;"></div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.write(f"**{cat['nome']}**")
                        
                        with col3:
                            if st.button("✏️ Editar", key=f"edit_desp_{cat['id']}"):
                                st.session_state['editar_categoria'] = cat['id']
                                st.rerun()
                        
                        with col4:
                            if st.button("🗑️ Excluir", key=f"del_desp_{cat['id']}"):
                                sucesso, mensagem = CategoriaService.excluir_categoria(cat['id'], usuario.id)
                                if sucesso:
                                    st.success(mensagem)
                                    st.rerun()
                                else:
                                    st.error(mensagem)
                    
                    st.divider()
            
            if not tipo_filtro or tipo_filtro == TipoCategoria.ENTRADA:
                if entradas:
                    st.markdown("### 💰 Categorias de Entrada")
                    
                    for cat in entradas:
                        col1, col2, col3, col4 = st.columns([0.1, 3, 1, 1])
                        
                        with col1:
                            st.markdown(f'<div style="background-color: {cat["cor"]}; width: 30px; height: 30px; border-radius: 5px;"></div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.write(f"**{cat['nome']}**")
                        
                        with col3:
                            if st.button("✏️ Editar", key=f"edit_ent_{cat['id']}"):
                                st.session_state['editar_categoria'] = cat['id']
                                st.rerun()
                        
                        with col4:
                            if st.button("🗑️ Excluir", key=f"del_ent_{cat['id']}"):
                                sucesso, mensagem = CategoriaService.excluir_categoria(cat['id'], usuario.id)
                                if sucesso:
                                    st.success(mensagem)
                                    st.rerun()
                                else:
                                    st.error(mensagem)
        else:
            st.info("Nenhuma categoria cadastrada.")
        
        # Modal de edição
        if 'editar_categoria' in st.session_state:
            categoria = CategoriaService.obter_categoria(
                st.session_state['editar_categoria'],
                usuario.id
            )
            
            if categoria:
                st.divider()
                st.subheader(f"Editar: {categoria['nome']}")
                
                with st.form("form_editar_categoria"):
                    novo_nome = st.text_input("Nome", value=categoria['nome'])
                    nova_cor = st.color_picker("Cor", value=categoria['cor'])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.form_submit_button("💾 Salvar", use_container_width=True):
                            sucesso, mensagem = CategoriaService.atualizar_categoria(
                                categoria['id'],
                                usuario.id,
                                novo_nome,
                                nova_cor
                            )
                            
                            if sucesso:
                                st.success(mensagem)
                                del st.session_state['editar_categoria']
                                st.rerun()
                            else:
                                st.error(mensagem)
                    
                    with col2:
                        if st.form_submit_button("❌ Cancelar", use_container_width=True):
                            del st.session_state['editar_categoria']
                            st.rerun()
    
    with tab_criar:
        st.subheader("Criar Nova Categoria")
        
        with st.form("form_nova_categoria"):
            nome = st.text_input("Nome da Categoria")
            tipo = st.selectbox(
                "Tipo",
                [TipoCategoria.DESPESA, TipoCategoria.ENTRADA],
                format_func=lambda x: x.value
            )
            cor = st.color_picker("Cor", value="#3498db")
            
            if st.form_submit_button("✅ Criar Categoria", use_container_width=True):
                if not nome:
                    st.error("Por favor, informe o nome da categoria!")
                else:
                    sucesso, mensagem, _ = CategoriaService.criar_categoria(
                        usuario.id,
                        nome,
                        tipo,
                        cor
                    )
                    
                    if sucesso:
                        st.success(mensagem)
                        st.rerun()
                    else:
                        st.error(mensagem)
