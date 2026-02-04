from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database.base import Base
from datetime import date
import enum


class TipoLancamento(enum.Enum):
    """Tipos de lançamento financeiro."""
    FIXA = "Fixa"
    VARIAVEL = "Variável"


class Lancamento(Base):
    """Modelo de lançamento financeiro (entrada ou despesa)."""
    
    __tablename__ = 'lancamentos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    data = Column(Date, nullable=False, default=date.today)
    valor = Column(Float, nullable=False)
    descricao = Column(String(255))
    tipo = Column(Enum(TipoLancamento), nullable=False, default=TipoLancamento.VARIAVEL)
    
    # Relacionamentos
    usuario = relationship('Usuario', back_populates='lancamentos')
    categoria = relationship('Categoria', back_populates='lancamentos')
    
    def __repr__(self):
        return f"<Lancamento(id={self.id}, data={self.data}, valor={self.valor}, descricao='{self.descricao}')>"
    
    @property
    def mes_ano(self) -> str:
        """Retorna o mês/ano do lançamento no formato 'MM/YYYY'."""
        return self.data.strftime('%m/%Y')
