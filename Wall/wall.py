from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, redirect,flash,session
from mysqlconnection import MySQLConnector
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key="secret"
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_REGEX = re.compile(r'^[a-zA-Z]+$')
mysql = MySQLConnector(app, 'walldb')
@app.route('/')
def index():
  return render_template("FORM.html")

@app.route('/result', methods=['POST'])
def create_user():
   #print "Got Post Info"
   #print request.form 

   firstname = request.form['firstname']
   lastname = request.form['lastname']
   emailid = request.form['emailid']
   password = request.form['password']
   pw_confirm = request.form['pw_confirm']


   
   if len(firstname) < 3:
    flash("Please enter atleast two characters for First name") 
   if (name_REGEX.match(firstname) == None):                        #if not first_name.isalpha()
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
      query = "INSERT INTO users (first_name, last_name, emailid, password,created_at,updated_at) VALUES (:first_name, :last_name, :emailid, :password, NOW(), NOW())"
      data = {
              'first_name': request.form['firstname'],
              'last_name':request.form['lastname'],
              'emailid':request.form['emailid'],
              'password': encrypted_password
              }
      mysql.query_db(query, data)
      
   return redirect('/loginpage')


@app.route('/loginpage')
def login_user():
  return render_template("loginpage.html")

@app.route('/logincheck', methods = ['POST'])
def login_check():
  
    print request.form
    password = request.form['password']
    emailid = request.form['emailid']

    if len(request.form['emailid']) < 1:
        flash("Email cannot be blank!")
    elif not EMAIL_REGEX.match(request.form['emailid']):
        flash("Invalid Email Address!")

    if len(password) <= 8:
        flash("Atleast 8 characters needed")
    if '_flashes' in session:
        return redirect('/loginpage')
    
    data = {
            'emailid': request.form['emailid']
            }
    query = "SELECT * FROM users WHERE emailid=:emailid"
    existinguser = mysql.query_db(query, data)

    try:
        dbpassword=existinguser[0]['password']
        session["firstname"] = existinguser[0]['first_name']
    except:
        flash("Please Register")
        return render_template('FORM.html')

    a = bcrypt.check_password_hash(existinguser[0]['password'], request.form['password'])
    if a==True:
        session["idusers"] = existinguser[0]['idusers']
        return redirect('/wall')
    else:
        return render_template("FORM.html")

@app.route('/wall', methods=['GET'])                #since we have two apps with same rote specify the method
def wall3():
    
    query1 = "SELECT * FROM messages JOIN users ON idusers = user_iduser ORDER BY messages.created_at DESC"
    data1 = {
            'as': session['idusers']
            }
    usermsgs = mysql.query_db(query1, data1)
    
    
    query = "SELECT * FROM comments JOIN messages on idmessages = comments.message_idmessage ORDER BY comments.created_at DESC "

    usercomments = mysql.query_db(query)
   
    return render_template("loggedin.html", usercomments = usercomments,usermsgs = usermsgs)


@app.route('/wall', methods = ['POST'])
def wall2():
    print request.form
    if request.form['action'] == 'postmsg':
        print "IN POST MSGS"
        comment = request.form['comment']
        query = "INSERT INTO messages (message, created_at, updated_at, user_iduser) VALUES (:message, NOW(), NOW(), :user_id)"
        data = {
                'message': request.form['comment'],
                'user_id': session['idusers']
                }
        mysql.query_db(query, data)
        return redirect('/wall')
    elif request.form['action'] == 'postcmt':
        #print "IN COMMENTS"
        comment_for_post = request.form['commenting']
        msgid = request.form ['msgid']
        #print "THIS IS MSGID"
        #print msgid
        print request.form
        query  = "INSERT INTO comments (comment, created_at, updated_at, message_idmessage,user_iduser) VALUES (:comments, NOW(), NOW(),:message_id, :user_id)"
        data = {
                'comments': request.form['commenting'],
                'message_id': request.form['msgid'],
                'user_id': session['idusers']
                }
        mysql.query_db(query, data)
        return redirect('/wall')
        
    
app.run(debug=True) 