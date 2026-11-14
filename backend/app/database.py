from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Credenciales por defecto. 'db' es el nombre del contenedor en tu docker-compose.yml
SQLALCHEMY_DATABASE_URL = "postgresql://admin:password@db:5432/agridb"
# Crear el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear la sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para crear nuestros modelos (tablas)
Base = declarative_base()

# Función para obtener la base de datos en nuestros endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()