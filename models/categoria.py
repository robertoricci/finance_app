from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
import enum


class TipoCategoria(enum.Enum):
    """Tipos de categoria financeira."""
    DESPESA = "Despesa"
    ENTRADA = "Entrada"


class Categoria(Base):
    """Modelo de categoria financeira."""
    
    __tablename__ = 'categorias'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    nome = Column(String(100), nullable=False)
    tipo = Column(Enum(TipoCategoria), nullable=False)
    cor = Column(String(7), default='#3498db')  # Cor em hexadecimal
    
    # Relacionamentos
    usuario = relationship('Usuario', back_populates='categorias')
    lancamentos = relationship('Lancamento', back_populates='categoria')
    orcamentos = relationship('OrcamentoMensal', back_populates='categoria')
    
    def __repr__(self):
        return f"<Categoria(id={self.id}, nome='{self.nome}', tipo={self.tipo.value})>"
