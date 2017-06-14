from flask import Flask,render_template,request,redirect,flash,session
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "Thisissecret"
mysql = MySQLConnector(app, 'friendsassign')
# connect and store the connection in "mysql" note that you pass the database name to the function
 
@app.route('/') 
def display_friends():
    querysel="SELECT * FROM friend"
    friends= mysql.query_db(querysel)
    print friends
    try:
        friend=friends[0]
    except:
        flash("There are no entries")
    return render_template('index.html',friends=friends)

@app.route('/friends', methods=['POST'])
def create():
    query = "INSERT INTO friend (first_name, last_name, age,friend_since) VALUES (:first_name, :last_name, :age, NOW())"
    data = {
            'first_name': request.form['first_name'],
            'last_name':  request.form['last_name'],
            'age': request.form['age']

           }
    mysql.query_db(query, data)
    return redirect('/')
app.run(debug=True)