from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from database.base import Base
import os


class DatabaseManager:
    """Gerenciador de conexão e sessões do banco de dados."""
    
    def __init__(self, db_path: str = 'finance_app.db'):
        """
        Inicializa o gerenciador de banco de dados.
        
        Args:
            db_path: Caminho para o arquivo do banco SQLite
        """
        self.db_path = db_path
        self.engine = create_engine(
            f'sqlite:///{db_path}',
            echo=False,
            connect_args={'check_same_thread': False}
        )
        self.Session = scoped_session(sessionmaker(bind=self.engine))
    
    def create_tables(self):
        """Cria todas as tabelas no banco de dados."""
        # Import necessário para registrar os modelos
        from models import Usuario, Categoria, Lancamento, OrcamentoMensal
        Base.metadata.create_all(self.engine)
    
    def drop_tables(self):
        """Remove todas as tabelas do banco de dados."""
        Base.metadata.drop_all(self.engine)
    
    @contextmanager
    def get_session(self):
        """
        Context manager para gerenciar sessões do banco.
        
        Uso:
            with db_manager.get_session() as session:
                # operações com o banco
                session.query(...)
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def init_database(self):
        """Inicializa o banco de dados criando as tabelas se não existirem."""
        if not os.path.exists(self.db_path):
            self.create_tables()
            return True
        return False


# Instância global do gerenciador de banco
db_manager = DatabaseManager()
