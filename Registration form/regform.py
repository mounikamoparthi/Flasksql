from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, redirect,flash,session
from mysqlconnection import MySQLConnector
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key="secret"
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_REGEX = re.compile(r'^[a-zA-Z]+$')
mysql = MySQLConnector(app, 'registrations')
@app.route('/')
def index():
  return render_template("FORM.html")

@app.route('/result', methods=['POST'])
def create_user():
   print "Got Post Info"
   print request.form 

   firstname = request.form['firstname']
   lastname = request.form['lastname']
   emailid = request.form['emailid']
   password = request.form['password']
   pw_confirm = request.form['pw_confirm']

   print  name_REGEX.match(firstname) 
   print "regex displayed above"
   
   if len(firstname) < 3:
    flash("Please enter atleast two characters for First name")
   if (name_REGEX.match(firstname) == None):
    flash("Please enter only alpabets for First name")
   if len(lastname) < 3:
    flash("Please enter atleast two characters for Last name")
   if (name_REGEX.match(lastname) == None):
    flash("Please enter only alpabets for last name")
   if len(request.form['emailid']) < 1:
    flash("Email cannot be blank!")
   elif not EMAIL_REGEX.match(request.form['emailid']):
    flash("Invalid Email Address!")
   if len(password) <= 8:
    flash("Atleast 8 characters needed")
   elif password!=pw_confirm:
    flash("Password doesnot match")
   if '_flashes' in session:
    return redirect('/')
   else:
      encrypted_password = bcrypt.generate_password_hash(password)
      query = "INSERT INTO regusers (first_name, last_name, emailid, password) VALUES (:first_name, :last_name, :emailid, :password)"
      data = {
              'first_name': request.form['firstname'],
              'last_name':request.form['lastname'],
              'emailid':request.form['emailid'],
              'password': encrypted_password
              }
      mysql.query_db(query, data)
      
   return render_template("result.html", name=firstname + " " + lastname)
@app.route('/loginpage', methods=['POST'])
def login_user():
  return render_template("loginpage.html")
@app.route('/logincheck', methods = ['POST'])
def login_check():
  print request.form
  
  data = {
          'emailid': request.form['emailid'],
          
         }
  query = "SELECT * FROM regusers WHERE emailid=:emailid"
  existinguser = mysql.query_db(query, data)
  try:
    dbpassword=existinguser[0]['password']
  except:
    flash("Please Register")
    return render_template('FORM.html')
  a = bcrypt.check_password_hash(existinguser[0]['password'], request.form['password'])
  if a==True:
    return render_template("loggedin.html")
  else:
    return render_template("FORM.html")
app.run(debug=True) 