from flask import Blueprint, render_template, request
import mysql.connector

staff_api = Blueprint('staff_api',__name__)

#by Peter Pfoertsch,250741344
#for CS3319 Assignment 3

#Staff View
@staff_api.route("/staff")
def staff():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query = ("show tables")
    cursor.execute(query)
    returnString = []
    for i in cursor:
        print(i)
        returnString.append(i)
        
    cursor.close()
    cnx.close()
    
    return render_template('staffIndex.html', data=returnString) 
 
#intermediate pages that set up the site to execute the right sql statement

#edit is the add, it was originally going to be update, but I switched it over
# for sake of consistency, I kept it edit, I know it's not good coding practice, but I had little time 
#it is not specified wether you should not allow someone to change primary key attributes, so I allowed them to change it
@staff_api.route("/edit")
def edit():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    #get all columns to show all categories
    type = str(request.args.get('type'))
    query = ("show columns from %s" % type)
    cursor.execute(query)
        
    returnString = []
    for i in cursor:
        print(i)
        returnString.append(i)
        
    cursor.close()
    cnx.close()
    
    #return template that gives input box for each condition and it's submit is the relevent add
    return render_template('edit.html', name=type,command="/add%s" % type, data=returnString)   

#update is the page that sets up the update
#you can only change one attribute at a time for a single tuple    
@staff_api.route("/update")
def update():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    type = str(request.args.get('type'))
    key = str(request.args.get('key'))
    query = ("show columns from %s" % type)
    cursor.execute(query)
        
    returnString = []
    for i in cursor:
        print(i)
        returnString.append(i)
        
    cursor.close()
    cnx.close()
    
    return render_template('update.html', name=type,command="/modify%s" % type, data=returnString,key=key)

    
#I couldn't figure out how to make one show, add, delete and modify method for all tables, so I made each one seperately
#they all have the same structure, with me first defining the basic structure and then adding in the relevant details from the sources
#I sometimes get the data from the url, just to keep track of things better
#movies methods
@staff_api.route("/showMovie")
def showMovie():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
        
    query = ("select idMovie,MovieName,MovieYear from Movie order by MovieName")
    cursor.execute(query) 
        
    returnString = []    
    for i in cursor:
        print(i)
        returnString.append(i)
    
    #add the columns you need
    query = ("show columns from Movie")
    cursor.execute(query)
        
    columns = []
    for i in cursor:
        print(i)
        columns.append(i)
        
    cursor.close()
    cnx.close()
    return render_template('table.html', type="Movie", data=returnString, columns=columns)

    #add
@staff_api.route("/addMovie", methods=["POST"])
def addMovie():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = (
        "INSERT INTO Movie(idMovie, MovieName, MovieYear) "
        "VALUES (%s,%s,%s)"
    )
    data = (request.form['idMovie'], request.form['MovieName'], request.form['MovieYear'])
    print(data)
    cursor.execute(insert_stmt, data)
   
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template('success.html', type="Movie")

    #delete
@staff_api.route("/deleteMovie", methods=["POST"])
def deleteMovie():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    data = str(request.form['idMovie'])
    delete_stmt = ("delete from Movie where idMovie=%s" % data)
    
    #added try catch here because of the foreign key error
    try: 
        cursor.execute(delete_stmt)
    except mysql.connector.errors.IntegrityError as e:
        print(e)
        return render_template('error.html', error=e)
        
    cnx.commit()
    cursor.close()
    cnx.close()
    
    return render_template('success.html', type="Movie")
    
    #modify
@staff_api.route("/modifyMovie", methods=["POST"])
def modifyMovie():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    modify_stmt = (
        "update Movie set %s='%s' where idMovie='%s'"
    ) % (request.form['attribute'], request.form['value'],request.form['idMovie'])
    print(modify_stmt)
    cursor.execute(modify_stmt)
    
    cnx.commit()
    cursor.close()
    cnx.close()
    
    return render_template('success.html', type="Movie")

#Genres methods
@staff_api.route("/showGenre")
def showGenre():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query = ("select Movie_idMovie, MovieName,Genre from Genre join Movie on Genre.Movie_idMovie=Movie.idMovie")
    cursor.execute(query)
    
    returnString = []
    for i in cursor:
        print(i)
        returnString.append(i)
    query = ("show columns from Genre")
    cursor.execute(query)
    
    #get the columns for the table header
    columns = []
    for i in cursor:
        print(i)
        columns.append(i)
        
    cursor.close()
    cnx.close()
    return render_template('genreTable.html', type="Genre",data=returnString, columns=columns)
 
    #add
@staff_api.route("/addGenre", methods=["POST"])
def addGenre():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = (
        "INSERT INTO Genre(Genre, Movie_idMovie) "
        "VALUES (%s,%s)"
    )
    data = (request.form['Genre'], request.form['Movie_idMovie'])
    print(data)
    cursor.execute(insert_stmt, data)
   
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template('success.html', type="Genre")

    #delete
@staff_api.route("/deleteGenre", methods=["POST"])
def deleteGenre():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    data = str(request.form['idGenre'])
    delete_stmt = ("delete from Genre where Movie_idMovie='%s'" % data)

    cursor.execute(delete_stmt)
    cnx.commit()
    cursor.close()
    cnx.close()
    
    return render_template('success.html', type="Genre")
    
#Rooms methods
@staff_api.route("/showTheatreRoom")
def showTheatreRoom():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
        
    query = ("select roomNumber,Capacity from TheatreRoom")
    cursor.execute(query)
    
    returnString = []
    for i in cursor:
        print(i)
        returnString.append(i)
    
    query = ("show columns from TheatreRoom")
    cursor.execute(query)
    #get the columns for the table header 
    columns = []
    for i in cursor:
        print(i)
        columns.append(i)
        
    cursor.close()
    cnx.close()
    return render_template('table.html', data=returnString, type="TheatreRoom", columns=columns)
    
    #add
@staff_api.route("/addTheatreRoom", methods=["POST"])
def addTheatreRoom():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = (
        "INSERT INTO TheatreRoom(RoomNumber, Capacity) "
        "VALUES (%s,%s)"
    )
    data = (request.form['RoomNumber'], request.form['Capacity'])
    print(insert_stmt, data)
    
    cursor.execute(insert_stmt,data)
    cnx.commit()
    cursor.close()
    cnx.close()
    
    return render_template('success.html', type="TheatreRoom")

    #delete
@staff_api.route("/deleteTheatreRoom", methods=["POST"])
def deleteTheatreRoom():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    data = (request.form['idTheatreRoom'])
    delete_stmt = ("delete from TheatreRoom where RoomNumber=%s" % data)
    print(delete_stmt, data)
    cursor.execute(delete_stmt)
    
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template('success.html', type="TheatreRoom")
    
    #modify
@staff_api.route("/modifyTheatreRoom", methods=["POST"])
def modifyTheatreRoom():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    data = (request.form['attribute'], request.form['value'],request.form['idTheatreRoom'])
    modify_stmt = ("update TheatreRoom set %s=%s where RoomNumber=%s" % data)
    cursor.execute(modify_stmt)
    
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template('success.html', type="TheatreRoom")
    
#Showings methods
@staff_api.route("/showShowing")
def showShowing():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query = ("select idShowing,date_format(ShowingDateTime,'%m-%e-%Y %H:%i:%S'),Movie_idMovie,TheatreRoom_RoomNumber,TicketPrice " 
    "from Showing order by ShowingDateTime")
    cursor.execute(query)
    
    returnString = []
    for i in cursor:
        print(i)
        returnString.append(i)
    
    query = ("show columns from Showing")
    cursor.execute(query)
       #get the columns for the table header 
    columns = []
    for i in cursor:
        print(i)
        columns.append(i)  
        
    cursor.close()
    cnx.close()
    return render_template('table.html', data=returnString , type="Showing", columns=columns)
    
    #add
@staff_api.route("/addShowing", methods=["POST"])
def addShowing():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = (
        "INSERT INTO Showing(idShowing,ShowingDateTime,Movie_idMovie,TheatreRoom_RoomNumber,TicketPrice) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    data = (request.form['idShowing'], request.form['ShowingDateTime'], 
    request.form['Movie_idMovie'], request.form['TheatreRoom_RoomNumber'],
    request.form['TicketPrice'])
    cursor.execute(insert_stmt, data)
    
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template('success.html', type="Showing")
    
    #delete
@staff_api.route("/deleteShowing", methods=["POST"])
def deleteShowing():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    data = (request.form['idShowing'])
    delete_stmt = ("delete from Showing where idShowing=%s" % data)
    #added try catch here because of the foreign key error
    try: 
        cursor.execute(delete_stmt)
    except mysql.connector.errors.IntegrityError as e:
        print(e)
        return render_template('error.html', error=e)
    
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template('success.html', type="Showing")
    
    #modify
@staff_api.route("/modifyShowing", methods=["POST"])
def modifyShowing():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    data = (request.form['attribute'], request.form['value'],request.form['idShowing'])
    modify_stmt = ("update Showing set %s='%s' where idShowing='%s'" % data)
    
    cursor.execute(modify_stmt)
    
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template('success.html', type="Showing")
    
#Customers methods
@staff_api.route("/showCustomer")
def showCustomer():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
        
    query = ("select idCustomer,LastName,FirstName,EmailAddress,cast(Sex as char(1)) from Customer order by LastName")
    cursor.execute(query)
    
    returnString = []
    for i in cursor:
        print(i)
        returnString.append(i)
    
    query = ("show columns from Customer")
    cursor.execute(query)
    #get the columns for the table header    
    columns = []
    for i in cursor:
        print(i)
        columns.append(i)
        
    cursor.close()
    cnx.close()
    return render_template('table.html', data=returnString , type="Customer", columns=columns)
    
    #add
@staff_api.route("/addCustomer", methods=["POST"])
def addCustomer():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre' )
    cursor = cnx.cursor()
    insert_stmt = (
        "INSERT INTO Customer(idCustomer,FirstName,LastName,EmailAddress,Sex) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    data = (request.form['idCustomer'], request.form['FirstName'], request.form['LastName'], request.form['EmailAddress'], request.form['Sex'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template('success.html', type="Customer")

    #delete
@staff_api.route("/deleteCustomer", methods=["POST"])
def deleteCustomer():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    delete_stmt = ("delete from Customer where idCustomer=(%s)")
    data = (request.form['idCustomer'],)
    cursor.execute(delete_stmt, data)
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template('success.html', type="Customer")
    
    #modify
@staff_api.route("/modifyCustomer", methods=["POST"])
def modifyCustomer():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    data = (request.form['attribute'], request.form['value'],request.form['idCustomer'])
    modify_stmt = ("update Customer set %s='%s' where idCustomer='%s'" % data)
    
    cursor.execute(modify_stmt)
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template('success.html', type="Customer")
    
#show Attendings
@staff_api.route("/showAttend")
def showAttend():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
        
    query = ("select idShowing,Rating,FirstName,LastName, date_format(ShowingDateTime,'%m-%e-%Y %H:%i:%S'), idMovie, MovieName from Attend "
        "join Customer on Customer_idCustomer=idCustomer "
        "join Showing on Showing_idShowing=idShowing "
        "join Movie on Movie_idMovie=idMovie "
        "order by Rating")
    cursor.execute(query)
    
    returnString = []
    for i in cursor:
        print(i)
        returnString.append(i)
        
    cursor.close()
    cnx.close()
    return render_template('staticTable.html', data=returnString , type="Attend")