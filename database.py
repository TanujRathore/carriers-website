import sqlalchemy
from sqlalchemy import create_engine, text
import os
my_secret = os.environ['DB_CONNECTION_STRING']

db_connection_string=my_secret

engine = create_engine(db_connection_string, connect_args={
  "ssl": {
    "ssl_ca": "/etc/ssl/cert.pem"
  }
})

def load_jobs_from_db():
  with engine.connect() as conn:
    result=conn.execute(text("select * from jobs"))
  column_names=result.keys()

  result_dicts=[]
  for row in result.all():
    result_dicts.append(dict(zip(column_names,row)))
  return result_dicts

'''
def load_job_from_db(id):
  with engine.connect() as conn:
    result= conn.execute(text(f"SELECT * FROM jobs WHERE id ={id}"))
    rows = []
    for row in result.all():
      rows.append(row._mapping)
      
      if len(rows)==0:
        return None
      else:
        return row

'''
def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(
       text("SELECT * FROM jobs WHERE id=:val"),{'val':id})
    row=result.fetchone()
    return row._asdict()
    
    

  