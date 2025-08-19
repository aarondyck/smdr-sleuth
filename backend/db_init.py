from sqlalchemy import create_engine
from models import Base

DB_FILENAME = 'smdr.db'
DB_URL = f'sqlite:///{DB_FILENAME}'

def init_db():
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    print(f"Database initialized at {DB_FILENAME}")

if __name__ == "__main__":
    init_db()
