from typing import List, Optional
from datetime import date, datetime
from models.lancamento import Lancamento, TipoLancamento
from models.categoria import Categoria, TipoCategoria
from database.connection import db_manager
from sqlalchemy import func, extract


class LancamentoService:
    """Serviço para gerenciamento de lançamentos financeiros."""
    
    @staticmethod
    def criar_lancamento(
        usuario_id: int,
        categoria_id: int,
        data: date,
        valor: float,
        descricao: str,
        tipo: TipoLancamento
    ) -> tuple[bool, str, Optional[Lancamento]]:
        """
        Cria um novo lançamento financeiro.
        
        Args:
            usuario_id: ID do usuário
            categoria_id: ID da categoria
            data: Data do lançamento
            valor: Valor do lançamento
            descricao: Descrição do lançamento
            tipo: Tipo do lançamento (FIXA ou VARIAVEL)
            
        Returns:
            Tupla (sucesso, mensagem, lancamento)
        """
        try:
            with db_manager.get_session() as session:
                # Verifica se a categoria pertence ao usuário
                categoria = session.query(Categoria).filter_by(
                    id=categoria_id,
                    usuario_id=usuario_id
                ).first()
                
                if not categoria:
                    return False, "Categoria não encontrada ou não pertence ao usuário!", None
                
                # Cria o lançamento
                lancamento = Lancamento(
                    usuario_id=usuario_id,
                    categoria_id=categoria_id,
                    data=data,
                    valor=abs(valor),  # Garante valor positivo
                    descricao=descricao,
                    tipo=tipo
                )
                
                session.add(lancamento)
                session.flush()
                session.expunge(lancamento)
                
                return True, "Lançamento criado com sucesso!", lancamento
        except Exception as e:
            return False, f"Erro ao criar lançamento: {str(e)}", None
    
    @staticmethod
    def listar_lancamentos(
        usuario_id: int,
        mes: Optional[int] = None,
        ano: Optional[int] = None,
        categoria_id: Optional[int] = None
    ) -> List[Lancamento]:
        """
        Lista lançamentos com filtros opcionais.
        
        Args:
            usuario_id: ID do usuário
            mes: Filtro por mês (1-12)
            ano: Filtro por ano
            categoria_id: Filtro por categoria
            
        Returns:
            Lista de lançamentos
        """
        try:
            with db_manager.get_session() as session:
                query = session.query(Lancamento).filter_by(usuario_id=usuario_id)
                
                if mes:
                    query = query.filter(extract('month', Lancamento.data) == mes)
                
                if ano:
                    query = query.filter(extract('year', Lancamento.data) == ano)
                
                if categoria_id:
                    query = query.filter_by(categoria_id=categoria_id)
                
                lancamentos = query.order_by(Lancamento.data.desc()).all()
                
                # Cria uma lista de dicionários com os dados necessários
                resultado = []
                for lanc in lancamentos:
                    resultado.append({
                        'id': lanc.id,
                        'data': lanc.data,
                        'valor': lanc.valor,
                        'descricao': lanc.descricao,
                        'tipo': lanc.tipo,
                        'categoria_id': lanc.categoria.id,
                        'categoria_nome': lanc.categoria.nome,
                        'categoria_tipo': lanc.categoria.tipo,
                        'categoria_cor': lanc.categoria.cor
                    })
                
                return resultado
        except Exception as e:
            print(f"Erro ao listar lançamentos: {e}")
            return []
    
    @staticmethod
    def atualizar_lancamento(
        lancamento_id: int,
        usuario_id: int,
        categoria_id: int,
        data: date,
        valor: float,
        descricao: str,
        tipo: TipoLancamento
    ) -> tuple[bool, str]:
        """
        Atualiza um lançamento existente.
        
        Args:
            lancamento_id: ID do lançamento
            usuario_id: ID do usuário (para validação)
            categoria_id: Nova categoria
            data: Nova data
            valor: Novo valor
            descricao: Nova descrição
            tipo: Novo tipo
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            with db_manager.get_session() as session:
                lancamento = session.query(Lancamento).filter_by(
                    id=lancamento_id,
                    usuario_id=usuario_id
                ).first()
                
                if not lancamento:
                    return False, "Lançamento não encontrado!"
                
                # Verifica se a categoria pertence ao usuário
                categoria = session.query(Categoria).filter_by(
                    id=categoria_id,
                    usuario_id=usuario_id
                ).first()
                
                if not categoria:
                    return False, "Categoria não encontrada!"
                
                lancamento.categoria_id = categoria_id
                lancamento.data = data
                lancamento.valor = abs(valor)
                lancamento.descricao = descricao
                lancamento.tipo = tipo
                
                return True, "Lançamento atualizado com sucesso!"
        except Exception as e:
            return False, f"Erro ao atualizar lançamento: {str(e)}"
    
    @staticmethod
    def excluir_lancamento(lancamento_id: int, usuario_id: int) -> tuple[bool, str]:
        """
        Exclui um lançamento.
        
        Args:
            lancamento_id: ID do lançamento
            usuario_id: ID do usuário (para validação)
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            with db_manager.get_session() as session:
                lancamento = session.query(Lancamento).filter_by(
                    id=lancamento_id,
                    usuario_id=usuario_id
                ).first()
                
                if not lancamento:
                    return False, "Lançamento não encontrado!"
                
                session.delete(lancamento)
                return True, "Lançamento excluído com sucesso!"
        except Exception as e:
            return False, f"Erro ao excluir lançamento: {str(e)}"
    
    @staticmethod
    def calcular_totais(usuario_id: int, mes: int, ano: int) -> dict:
        """
        Calcula totais de entradas, despesas e saldo.
        
        Args:
            usuario_id: ID do usuário
            mes: Mês (1-12)
            ano: Ano
            
        Returns:
            Dicionário com total_entradas, total_despesas, saldo
        """
        try:
            with db_manager.get_session() as session:
                # Total de entradas
                total_entradas = session.query(func.sum(Lancamento.valor)).join(
                    Categoria
                ).filter(
                    Lancamento.usuario_id == usuario_id,
                    Categoria.tipo == TipoCategoria.ENTRADA,
                    extract('month', Lancamento.data) == mes,
                    extract('year', Lancamento.data) == ano
                ).scalar() or 0.0
                
                # Total de despesas
                total_despesas = session.query(func.sum(Lancamento.valor)).join(
                    Categoria
                ).filter(
                    Lancamento.usuario_id == usuario_id,
                    Categoria.tipo == TipoCategoria.DESPESA,
                    extract('month', Lancamento.data) == mes,
                    extract('year', Lancamento.data) == ano
                ).scalar() or 0.0
                
                return {
                    'total_entradas': float(total_entradas),
                    'total_despesas': float(total_despesas),
                    'saldo': float(total_entradas - total_despesas)
                }
        except Exception as e:
            print(f"Erro ao calcular totais: {e}")
            return {'total_entradas': 0.0, 'total_despesas': 0.0, 'saldo': 0.0}
    
    @staticmethod
    def obter_lancamento(lancamento_id: int, usuario_id: int) -> Optional[dict]:
        """Obtém um lançamento específico."""
        try:
            with db_manager.get_session() as session:
                lancamento = session.query(Lancamento).filter_by(
                    id=lancamento_id,
                    usuario_id=usuario_id
                ).first()
                
                if lancamento:
                    return {
                        'id': lancamento.id,
                        'data': lancamento.data,
                        'valor': lancamento.valor,
                        'descricao': lancamento.descricao,
                        'tipo': lancamento.tipo,
                        'categoria_id': lancamento.categoria.id,
                        'categoria_nome': lancamento.categoria.nome,
                        'categoria_tipo': lancamento.categoria.tipo,
                        'categoria_cor': lancamento.categoria.cor
                    }
                
                return None
        except Exception:
            return None
