from flask import Flask,render_template,request,redirect
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, 'test')
# connect and store the connection in "mysql" note that you pass the database name to the function
 
@app.route('/') 
def display_friends():
    querysel="SELECT * FROM friend"
    friends= mysql.query_db(querysel)
    return render_template('index.html',friends=friends)
# an example of running a query

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
# an example of running a query
app.run(debug=True)