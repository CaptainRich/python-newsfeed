from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g

load_dotenv()

# Connect to the database using the env variable (from the root directory ".env" file).
engine  = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)  #manages overall DB connection
Session = sessionmaker(bind=engine)                                                 #generates temporary connections
Base    = declarative_base()                                                   #helps map models to the real MySQL tables

def init_db(app):
  Base.metadata.create_all(engine)

  app.teardown_appcontext(close_db)   #run "close_db" with the teardown function

def get_db():
  #Avoid createing a new Session instance with each call to this function
  if 'db' not in g:
    # store db connection in app context
    g.db = Session()

  return g.db

def close_db(e=None):
  db = g.pop('db', None)   #find and remove "dg" from "g"

  if db is not None:
    db.close()