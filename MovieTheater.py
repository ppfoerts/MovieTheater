from flask import Flask, render_template, request
import mysql.connector
import os
from customer import customer_api
from staff import staff_api
app = Flask(__name__)

#by Peter Pfoertsch,250741344
#for CS3319 Assignment 3

#register the front and back ends
app.register_blueprint(customer_api)
app.register_blueprint(staff_api)

#index page here
@app.route("/")
def index():
    return render_template('index.html')

#sql Injection example
#uses the add movie, exactly the same except it does the sql injection error
@app.route('/sqlInjection')
def sqlInjection():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    type = 'Movie'
    query = ("show columns from %s" % type)
    cursor.execute(query)
  
    returnString = []
    for i in cursor:
        print(i)
        returnString.append(i)
        
    cursor.close()
    cnx.close()
    
    return render_template('edit.html', name=type,command="/add%s" % type, data=returnString) 

@app.route('/submitSqlInjection', methods=["POST"])
def sqlInjectionResult():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = (
        "INSERT INTO Movie(idMovie, MovieName, MovieYear) "
        "VALUES "
    )
    data = (request.form['idMovie'], request.form['MovieName'], request.form['MovieYear'])
    insert_stmt += data
    cursor.execute(insert_stmt)
   
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template('success.html', type="Movie")

 
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)