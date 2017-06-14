from flask import Flask, render_template
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app, 'twitter')
# an example of running a query
@app.route('/')
def index():
    users = mysql.query_db("SELECT * FROM users")
    print users
    return render_template("index.html", users = users) 
app.run(debug=True) 