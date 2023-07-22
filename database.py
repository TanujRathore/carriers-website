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


'''def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query=text("insert into applications (job_id,full_name,email,linkedin_url,education,work_experience,resume_url) values(:full_name,:email,:linkedin_url,:education,:work_experience,:resume_url)")
    
    conn.execute(query,
                 full_name=data['full_name'],
                 email=data['email'],
                 linkedin_url=data['linkedin_url'],
                 education=data['education'],
                 work_experience=data['work_experience'],
                 resume_url=data['resume_url'])'''


def add_application_to_db(id , data):
    with engine.connect() as conn:

        stmt = text("INSERT INTO `applications` ( `job_id`, `full_name`, `email`, `linkedin_url`, `education`, `work_experience`, `resume_url`) VALUES ( :job_id, :full_name, :email, :linkedin_url, :education ,  :work_experience,:resume_url)")
       


        stmt = stmt.bindparams(job_id=id)
        stmt = stmt.bindparams( full_name = data['full_name'])
        stmt = stmt.bindparams( email = data['email'])
        stmt = stmt.bindparams( linkedin_url = data['linkedin_url'])
        stmt = stmt.bindparams( education = data['education'])
        stmt = stmt.bindparams( work_experience = data['work_experience'])
        stmt = stmt.bindparams( resume_url = data['resume_url'])
        conn.execute(stmt)

                 


    
    

  