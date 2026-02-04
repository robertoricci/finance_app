from typing import List, Optional
from models.categoria import Categoria, TipoCategoria
from database.connection import db_manager


class CategoriaService:
    """Serviço para gerenciamento de categorias."""
    
    @staticmethod
    def listar_categorias(usuario_id: int, tipo: Optional[TipoCategoria] = None) -> List[dict]:
        """
        Lista todas as categorias de um usuário.
        
        Args:
            usuario_id: ID do usuário
            tipo: Filtro opcional por tipo (DESPESA ou ENTRADA)
            
        Returns:
            Lista de categorias
        """
        try:
            with db_manager.get_session() as session:
                query = session.query(Categoria).filter_by(usuario_id=usuario_id)
                
                if tipo:
                    query = query.filter_by(tipo=tipo)
                
                categorias = query.order_by(Categoria.nome).all()
                
                # Converte para dicionários
                resultado = []
                for cat in categorias:
                    resultado.append({
                        'id': cat.id,
                        'nome': cat.nome,
                        'tipo': cat.tipo,
                        'cor': cat.cor
                    })
                
                return resultado
        except Exception as e:
            print(f"Erro ao listar categorias: {e}")
            return []
    
    @staticmethod
    def criar_categoria(usuario_id: int, nome: str, tipo: TipoCategoria, cor: str = '#3498db') -> tuple[bool, str, Optional[Categoria]]:
        """
        Cria uma nova categoria.
        
        Args:
            usuario_id: ID do usuário
            nome: Nome da categoria
            tipo: Tipo da categoria (DESPESA ou ENTRADA)
            cor: Cor em hexadecimal
            
        Returns:
            Tupla (sucesso, mensagem, categoria)
        """
        try:
            with db_manager.get_session() as session:
                # Verifica se já existe categoria com mesmo nome
                existe = session.query(Categoria).filter_by(
                    usuario_id=usuario_id,
                    nome=nome
                ).first()
                
                if existe:
                    return False, "Já existe uma categoria com este nome!", None
                
                categoria = Categoria(
                    usuario_id=usuario_id,
                    nome=nome,
                    tipo=tipo,
                    cor=cor
                )
                session.add(categoria)
                session.flush()
                session.expunge(categoria)
                
                return True, "Categoria criada com sucesso!", categoria
        except Exception as e:
            return False, f"Erro ao criar categoria: {str(e)}", None
    
    @staticmethod
    def atualizar_categoria(categoria_id: int, usuario_id: int, nome: str, cor: str) -> tuple[bool, str]:
        """
        Atualiza uma categoria existente.
        
        Args:
            categoria_id: ID da categoria
            usuario_id: ID do usuário (para validação)
            nome: Novo nome
            cor: Nova cor
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            with db_manager.get_session() as session:
                categoria = session.query(Categoria).filter_by(
                    id=categoria_id,
                    usuario_id=usuario_id
                ).first()
                
                if not categoria:
                    return False, "Categoria não encontrada!"
                
                # Verifica se o novo nome já existe em outra categoria
                existe = session.query(Categoria).filter(
                    Categoria.usuario_id == usuario_id,
                    Categoria.nome == nome,
                    Categoria.id != categoria_id
                ).first()
                
                if existe:
                    return False, "Já existe outra categoria com este nome!"
                
                categoria.nome = nome
                categoria.cor = cor
                
                return True, "Categoria atualizada com sucesso!"
        except Exception as e:
            return False, f"Erro ao atualizar categoria: {str(e)}"
    
    @staticmethod
    def excluir_categoria(categoria_id: int, usuario_id: int) -> tuple[bool, str]:
        """
        Exclui uma categoria.
        
        Args:
            categoria_id: ID da categoria
            usuario_id: ID do usuário (para validação)
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            with db_manager.get_session() as session:
                categoria = session.query(Categoria).filter_by(
                    id=categoria_id,
                    usuario_id=usuario_id
                ).first()
                
                if not categoria:
                    return False, "Categoria não encontrada!"
                
                # Verifica se há lançamentos associados
                if categoria.lancamentos:
                    return False, "Não é possível excluir categoria com lançamentos associados!"
                
                session.delete(categoria)
                return True, "Categoria excluída com sucesso!"
        except Exception as e:
            return False, f"Erro ao excluir categoria: {str(e)}"
    
    @staticmethod
    def obter_categoria(categoria_id: int, usuario_id: int) -> Optional[dict]:
        """Obtém uma categoria específica."""
        try:
            with db_manager.get_session() as session:
                categoria = session.query(Categoria).filter_by(
                    id=categoria_id,
                    usuario_id=usuario_id
                ).first()
                
                if categoria:
                    return {
                        'id': categoria.id,
                        'nome': categoria.nome,
                        'tipo': categoria.tipo,
                        'cor': categoria.cor
                    }
                
                return None
        except Exception:
            return None
