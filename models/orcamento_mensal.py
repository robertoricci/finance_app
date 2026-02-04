from sqlalchemy import Column, Integer, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database.base import Base


class OrcamentoMensal(Base):
    """Modelo de orçamento planejado por categoria e mês."""
    
    __tablename__ = 'orcamentos_mensais'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    mes_ano = Column(String(7), nullable=False)  # Formato: 'MM/YYYY'
    valor_planejado = Column(Float, nullable=False)
    
    # Relacionamentos
    usuario = relationship('Usuario', back_populates='orcamentos')
    categoria = relationship('Categoria', back_populates='orcamentos')
    
    # Constraint para evitar duplicação: um orçamento por categoria por mês por usuário
    __table_args__ = (
        UniqueConstraint('usuario_id', 'categoria_id', 'mes_ano', name='uq_orcamento_usuario_categoria_mes'),
    )
    
    def __repr__(self):
        return f"<OrcamentoMensal(id={self.id}, mes_ano='{self.mes_ano}', valor={self.valor_planejado})>"
