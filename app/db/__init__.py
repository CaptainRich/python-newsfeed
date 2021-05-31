from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Connect to the database using the env variable (from the root directory ".env" file).
engine  = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)  #manages overall DB connection
Session = sessionmaker(bind=engine)                                                 #generates temporary connections
Base    = declarative_base()                                                    #helps map models to the real MySQL tables