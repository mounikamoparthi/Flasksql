from flask import Flask, render_template, request,redirect,flash,session
# import the Connector function
from mysqlconnection import MySQLConnector
import re
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app, 'email')
# an example of running a query
@app.route('/')
def index():
    return render_template("index.html") 
@app.route('/email_display', methods = ['POST'])
def display():
    if len(request.form['emailid']) < 1:
        flash("Email cannot be blank!")
    elif not EMAIL_REGEX.match(request.form['emailid']):
        flash("Invalid Email Address!")
        return redirect('/')
    else:
        flash("Success!")
        emailid = mysql.query_db("SELECT * FROM email_valid")
        query = "INSERT INTO email_valid (emailid) VALUES (:emailid)"
        data = {
                'emailid': request.form['emailid']
                }
        mysql.query_db(query, data)
    return render_template('result.html', emailid = emailid)
app.run(debug=True) 