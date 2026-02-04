from typing import List, Optional, Dict
from models.orcamento_mensal import OrcamentoMensal
from models.categoria import Categoria, TipoCategoria
from models.lancamento import Lancamento
from database.connection import db_manager
from sqlalchemy import func, extract


class OrcamentoService:
    """Serviço para gerenciamento de orçamentos mensais."""
    
    @staticmethod
    def definir_orcamento(
        usuario_id: int,
        categoria_id: int,
        mes: int,
        ano: int,
        valor_planejado: float
    ) -> tuple[bool, str]:
        """
        Define ou atualiza o orçamento para uma categoria em um mês específico.
        
        Args:
            usuario_id: ID do usuário
            categoria_id: ID da categoria
            mes: Mês (1-12)
            ano: Ano
            valor_planejado: Valor planejado para a categoria
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            with db_manager.get_session() as session:
                # Verifica se a categoria pertence ao usuário
                categoria = session.query(Categoria).filter_by(
                    id=categoria_id,
                    usuario_id=usuario_id
                ).first()
                
                if not categoria:
                    return False, "Categoria não encontrada!"
                
                # Só permite orçamento para despesas
                if categoria.tipo != TipoCategoria.DESPESA:
                    return False, "Orçamento só pode ser definido para categorias de despesa!"
                
                mes_ano = f"{mes:02d}/{ano}"
                
                # Verifica se já existe orçamento para esta categoria neste mês
                orcamento = session.query(OrcamentoMensal).filter_by(
                    usuario_id=usuario_id,
                    categoria_id=categoria_id,
                    mes_ano=mes_ano
                ).first()
                
                if orcamento:
                    # Atualiza orçamento existente
                    orcamento.valor_planejado = abs(valor_planejado)
                    mensagem = "Orçamento atualizado com sucesso!"
                else:
                    # Cria novo orçamento
                    orcamento = OrcamentoMensal(
                        usuario_id=usuario_id,
                        categoria_id=categoria_id,
                        mes_ano=mes_ano,
                        valor_planejado=abs(valor_planejado)
                    )
                    session.add(orcamento)
                    mensagem = "Orçamento criado com sucesso!"
                
                return True, mensagem
        except Exception as e:
            return False, f"Erro ao definir orçamento: {str(e)}"
    
    @staticmethod
    def listar_orcamentos(usuario_id: int, mes: int, ano: int) -> List[Dict]:
        """
        Lista orçamentos de um mês com comparação de valores planejados vs realizados.
        
        Args:
            usuario_id: ID do usuário
            mes: Mês (1-12)
            ano: Ano
            
        Returns:
            Lista de dicionários com informações de orçamento
        """
        try:
            with db_manager.get_session() as session:
                mes_ano = f"{mes:02d}/{ano}"
                
                orcamentos = session.query(OrcamentoMensal).filter_by(
                    usuario_id=usuario_id,
                    mes_ano=mes_ano
                ).all()
                
                resultado = []
                
                for orcamento in orcamentos:
                    # Calcula o valor realizado
                    valor_realizado = session.query(func.sum(Lancamento.valor)).filter(
                        Lancamento.usuario_id == usuario_id,
                        Lancamento.categoria_id == orcamento.categoria_id,
                        extract('month', Lancamento.data) == mes,
                        extract('year', Lancamento.data) == ano
                    ).scalar() or 0.0
                    
                    categoria = orcamento.categoria
                    
                    resultado.append({
                        'id': orcamento.id,
                        'categoria_id': categoria.id,
                        'categoria_nome': categoria.nome,
                        'categoria_cor': categoria.cor,
                        'valor_planejado': orcamento.valor_planejado,
                        'valor_realizado': float(valor_realizado),
                        'percentual_utilizado': (float(valor_realizado) / orcamento.valor_planejado * 100) if orcamento.valor_planejado > 0 else 0,
                        'diferenca': orcamento.valor_planejado - float(valor_realizado)
                    })
                
                return resultado
        except Exception as e:
            print(f"Erro ao listar orçamentos: {e}")
            return []
    
    @staticmethod
    def excluir_orcamento(orcamento_id: int, usuario_id: int) -> tuple[bool, str]:
        """
        Exclui um orçamento.
        
        Args:
            orcamento_id: ID do orçamento
            usuario_id: ID do usuário (para validação)
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            with db_manager.get_session() as session:
                orcamento = session.query(OrcamentoMensal).filter_by(
                    id=orcamento_id,
                    usuario_id=usuario_id
                ).first()
                
                if not orcamento:
                    return False, "Orçamento não encontrado!"
                
                session.delete(orcamento)
                return True, "Orçamento excluído com sucesso!"
        except Exception as e:
            return False, f"Erro ao excluir orçamento: {str(e)}"
    
    @staticmethod
    def obter_resumo_orcamento(usuario_id: int, mes: int, ano: int) -> Dict:
        """
        Obtém resumo do orçamento total do mês.
        
        Args:
            usuario_id: ID do usuário
            mes: Mês (1-12)
            ano: Ano
            
        Returns:
            Dicionário com total planejado, realizado e percentual
        """
        try:
            orcamentos = OrcamentoService.listar_orcamentos(usuario_id, mes, ano)
            
            total_planejado = sum(o['valor_planejado'] for o in orcamentos)
            total_realizado = sum(o['valor_realizado'] for o in orcamentos)
            
            percentual = (total_realizado / total_planejado * 100) if total_planejado > 0 else 0
            
            return {
                'total_planejado': total_planejado,
                'total_realizado': total_realizado,
                'diferenca': total_planejado - total_realizado,
                'percentual_utilizado': percentual
            }
        except Exception as e:
            print(f"Erro ao obter resumo: {e}")
            return {
                'total_planejado': 0.0,
                'total_realizado': 0.0,
                'diferenca': 0.0,
                'percentual_utilizado': 0.0
            }
