from src.db.models import Base
from src.db.connection import engine

Base.metadata.create_all(bind=engine)

print("Tables created successfully")