from flask import Flask, request,render_template, jsonify, session,redirect, url_for
from flask_mail import Mail, Message
import os
from database import load_jobs_from_db,load_job_from_db, add_application_to_db
from flask_session import Session
from sqlalchemy import create_engine, text
from database import engine

app=Flask(__name__)

# Connect to database

#configure session
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)




app.config["MAIL_DEFAULT_SENDER"]=os.environ["MAIL_DEFAULT_SENDER"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_PORT"]=587
app.config["MAIL_SERVER"]="smtp.gmail.com"
app.config["MAIL_USE_TLS"]=True
app.config["MAIL_USERNAME"]=os.environ["MAIL_USERNAME"]
mail=Mail(app)


@app.route("/")
def hello_world():
  jobs = load_jobs_from_db()
  return render_template('home.html',jobs=jobs)

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)


@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  if not job:
    return "Not Found",404
  return render_template('jobpage.html', job=job)


@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
  data=request.form
  job=load_job_from_db(id)

  add_application_to_db(id,data)
  msg = Message(
                'Hello',
                #sender ='yourId@gmail.com',
                recipients = [data['email']]
               )
  msg.body = 'Hello Flask message sent from Flask-Mail'
  mail.send(msg)
  
  return render_template('application_submitted.html',application=data,job=job)


@app.route("/login", methods=["POST"])
def login():
  if request.method=="POST":
    session["name"]=request.form.get("name")
    username=request.form.get("name")
    password=request.form.get("password")

    result=engine.connect().execute(text("select email from applications where email='username'"))
    result=result.fetchone()
    if username == result:
      return  redirect('home.html')
    else:
      return render_template('singup.html')
  return render_template('home.html')
    #return jsonify(result)
    #return jsonify(result)


@app.route("/logout")
def logout():
  session["name"]= None
  return redirect("/")



@app.route("/singup", methods=["POST"])
def singup():
  if request.method=="POST":
    username=request.form.get("name")
    pass_word=request.form.get("pass_word")
    with engine.connect() as conn:
      
      stmt =text("INSERT INTO 'login_information'('username','pass_word') VALUES (:username,:pass_word)")
      stmt = stmt.bindparams(username=username)
      stmt = stmt.bindparams( pass_word=pass_word)

      #stmt = stmt.params(username=username, pass_word=pass_word)
    
      conn.execute(stmt)

  return redirect('/login')


if __name__=='__main__':
  app.run(host='0.0.0.0',debug=True)