from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.base import Base
import hashlib


class Usuario(Base):
    """Modelo de usuário do sistema."""
    
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    senha_hash = Column(String(256), nullable=False)
    data_criacao = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    categorias = relationship('Categoria', back_populates='usuario', cascade='all, delete-orphan')
    lancamentos = relationship('Lancamento', back_populates='usuario', cascade='all, delete-orphan')
    orcamentos = relationship('OrcamentoMensal', back_populates='usuario', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Usuario(id={self.id}, nome='{self.nome}', email='{self.email}')>"
    
    @staticmethod
    def hash_senha(senha: str) -> str:
        """Gera hash SHA256 da senha."""
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def verificar_senha(self, senha: str) -> bool:
        """Verifica se a senha corresponde ao hash armazenado."""
        return self.senha_hash == self.hash_senha(senha)
