import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from typing import Generator

Base = declarative_base()

class DatabaseManager:
    """Singleton para gestionar la conexión a la base de datos"""
    _instance = None
    _engine = None
    _session_factory = None
    _tables_created = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._engine is None:
            self._initialize_database()

    def _initialize_database(self):
        database_url = os.getenv(
            "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/tracking")
        
        # Configuración optimizada del pool de conexiones
        self._engine = create_engine(
            database_url,
            pool_size=20,          # Número de conexiones en el pool
            max_overflow=30,       # Conexiones adicionales permitidas
            pool_timeout=30,       # Tiempo de espera para obtener conexión (segundos)
            pool_recycle=3600,     # Reciclar conexiones cada hora
            pool_pre_ping=True,    # Verificar conexiones antes de usar
            echo=False             # No mostrar SQL en logs (cambiar a True para debug)
        )
        
        # Crear la fábrica de sesiones
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine
        )

    def _ensure_tables_created(self):
        """Crear las tablas si no han sido creadas aún"""
        if not self._tables_created:
            Base.metadata.create_all(bind=self._engine)
            self._tables_created = True

    @property
    def engine(self):
        return self._engine

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Context manager para obtener una sesión de base de datos"""
        # Asegurar que las tablas estén creadas antes de usar la sesión
        self._ensure_tables_created()
        
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_session(self) -> Session:
        """Crear una nueva sesión (úsala solo si no puedes usar el context manager)"""
        self._ensure_tables_created()
        return self._session_factory()

# Instancia global del gestor de base de datos
db_manager = DatabaseManager()