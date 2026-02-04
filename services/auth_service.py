from typing import Optional
from sqlalchemy.orm import Session
from models.usuario import Usuario
from database.connection import db_manager


class AuthService:
    """Serviço de autenticação e gerenciamento de usuários."""
    
    @staticmethod
    def registrar_usuario(nome: str, email: str, senha: str) -> tuple[bool, str, Optional[Usuario]]:
        """
        Registra um novo usuário no sistema.
        
        Args:
            nome: Nome do usuário
            email: Email do usuário (único)
            senha: Senha em texto plano
            
        Returns:
            Tupla (sucesso, mensagem, usuario)
        """
        try:
            with db_manager.get_session() as session:
                # Verifica se o email já existe
                usuario_existente = session.query(Usuario).filter_by(email=email).first()
                if usuario_existente:
                    return False, "Este email já está cadastrado!", None
                
                # Cria novo usuário
                novo_usuario = Usuario(
                    nome=nome,
                    email=email,
                    senha_hash=Usuario.hash_senha(senha)
                )
                session.add(novo_usuario)
                session.flush()
                
                # Criar categorias padrão para o novo usuário
                AuthService._criar_categorias_padrao(session, novo_usuario.id)
                
                return True, "Usuário registrado com sucesso!", novo_usuario
        except Exception as e:
            return False, f"Erro ao registrar usuário: {str(e)}", None
    
    @staticmethod
    def _criar_categorias_padrao(session: Session, usuario_id: int):
        """Cria categorias padrão para um novo usuário."""
        from models.categoria import Categoria, TipoCategoria
        
        categorias_padrao = [
            # Despesas
            {'nome': 'Moradia', 'tipo': TipoCategoria.DESPESA, 'cor': '#e74c3c'},
            {'nome': 'Alimentação', 'tipo': TipoCategoria.DESPESA, 'cor': '#e67e22'},
            {'nome': 'Transporte', 'tipo': TipoCategoria.DESPESA, 'cor': '#f39c12'},
            {'nome': 'Saúde', 'tipo': TipoCategoria.DESPESA, 'cor': '#16a085'},
            {'nome': 'Educação', 'tipo': TipoCategoria.DESPESA, 'cor': '#2980b9'},
            {'nome': 'Lazer', 'tipo': TipoCategoria.DESPESA, 'cor': '#8e44ad'},
            {'nome': 'Outros', 'tipo': TipoCategoria.DESPESA, 'cor': '#95a5a6'},
            # Entradas
            {'nome': 'Salário', 'tipo': TipoCategoria.ENTRADA, 'cor': '#27ae60'},
            {'nome': 'Investimentos', 'tipo': TipoCategoria.ENTRADA, 'cor': '#2ecc71'},
            {'nome': 'Outros Rendimentos', 'tipo': TipoCategoria.ENTRADA, 'cor': '#1abc9c'},
        ]
        
        for cat_data in categorias_padrao:
            categoria = Categoria(usuario_id=usuario_id, **cat_data)
            session.add(categoria)
    
    @staticmethod
    def autenticar_usuario(email: str, senha: str) -> tuple[bool, str, Optional[Usuario]]:
        """
        Autentica um usuário no sistema.
        
        Args:
            email: Email do usuário
            senha: Senha em texto plano
            
        Returns:
            Tupla (sucesso, mensagem, usuario)
        """
        try:
            with db_manager.get_session() as session:
                usuario = session.query(Usuario).filter_by(email=email).first()
                
                if not usuario:
                    return False, "Email não encontrado!", None
                
                if not usuario.verificar_senha(senha):
                    return False, "Senha incorreta!", None
                
                # Retorna uma instância desacoplada da sessão
                session.expunge(usuario)
                return True, "Login realizado com sucesso!", usuario
        except Exception as e:
            return False, f"Erro ao autenticar: {str(e)}", None
    
    @staticmethod
    def obter_usuario_por_id(usuario_id: int) -> Optional[Usuario]:
        """Obtém um usuário pelo ID."""
        try:
            with db_manager.get_session() as session:
                usuario = session.query(Usuario).filter_by(id=usuario_id).first()
                if usuario:
                    session.expunge(usuario)
                return usuario
        except Exception:
            return None
