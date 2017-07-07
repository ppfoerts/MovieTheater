from flask import Blueprint, render_template, request
import mysql.connector
#by Peter Pfoertsch,250741344
#for CS3319 Assignment 3
customer_api = Blueprint('customer_api',__name__)

#Customer View 
#customer index page, will show a table of all customers
@customer_api.route("/customer")
def customer():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
        
    query = ("select idCustomer,LastName,FirstName,EmailAddress,cast(Sex as char(1)) from Customer order by LastName")
    cursor.execute(query)
    
    returnString = []
    for i in cursor:
        print(i)
        returnString.append(i)
        
    cursor.close()
    cnx.close()
    return render_template('customerIndex.html' , data=returnString , type="Customer") 

#Here is the menu for an individual customer
@customer_api.route("/customerInfo")   
def customerInfo():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    #get the profile info of the customer
    id = str(request.args.get('id'))
    query = ("select idCustomer,FirstName,LastName,EmailAddress,cast(Sex as char(1)) from Customer where idCustomer=%s" % id)
    cursor.execute(query)
        
    returnString = []
    for i in cursor:
        print(i)
        returnString.append(i)
    #get Movies seen    
    query = ("select idMovie, MovieName, idShowing, date_format(ShowingDateTime,'%m-%e-%Y %H:%i:%S'), Rating from Attend "
        "join Customer on Customer_idCustomer=idCustomer "
        "join Showing on Showing_idShowing=idShowing "
        "join Movie on Movie_idMovie=idMovie "
        "where idCustomer={0}".format(id))
        
    cursor.execute(query)
    
    movies = []
    for i in cursor:
        print(i)
        movies.append(i)
        
    #get all dates for showing date time dropdowns
    query = ("select * from Showing order by ShowingDateTime")
    cursor.execute(query)
    showings = []
    for i in cursor:
        print(i)
        showings.append(i)
        
    #get all genres to add in the dropdown    
    query = ("select Genre from Genre group by Genre")
    cursor.execute(query)
    genres = []
    for i in cursor:
        print(i)
        genres.append(i)
        
    
    cursor.close()
    cnx.close()
    
    return render_template('customerInfo.html', data=returnString, movies=movies, showings=showings, genres=genres, id=id)  

#command to update ratings for the movies seen
@customer_api.route("/customerUpdateRating", methods=["POST"])  
def customerUpdateRating():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    data = (request.form['value'],request.form['idShowing'])
    modify_stmt = ("update Attend set Rating='%s' where Showing_idShowing='%s'" % data)
    
    print(modify_stmt)
    cursor.execute(modify_stmt)
   
    cnx.commit()
    cursor.close()
    cnx.close()
    return "Success"

#command to search for showing
@customer_api.route("/searchForShowing", methods=["POST"])  
def searchForShowing():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    #long query to get all necessary info
    query = ("select idShowing,date_format(ShowingDateTime,'%m-%e-%Y %H:%i:%S'),Showing.Movie_idMovie,MovieName,TheatreRoom_RoomNumber,TicketPrice,Capacity,count(*),Rating " 
    "from Showing join Genre on Genre.Movie_idMovie=Showing.Movie_idMovie join TheatreRoom on TheatreRoom_RoomNumber=RoomNumber "
    "left join Attend on Showing_idShowing=idShowing "
    "join Movie on Showing.Movie_idMovie=idMovie "
    "where ShowingDateTime >= \"{0}\" and ShowingDateTime <= \"{1}\" ").format(request.form['startDate'], request.form['endDate']) #ask for date time here
    #if the user has selected a genre, add it as a requirement
    if request.form.get('genre') != "any":
        query = query + "and Genre='%s' " % request.form.get('genre')
    #if the user specified a movie name, add that condition here
    if request.form.get('MovieName') != "":
        query = query + " and MovieName='%s'" % request.form.get('MovieName')
    #group it by idshowing (because did left join earlier so that you know how many people are attending a showing)
    query = query + " group by idShowing"
    #if the user wants to know what seats are available, add the having condition here to show it. 
    #having is clause that is where after you group the tuples
    if request.form.get('seatsAvailable'):
        query = query + " having count(*) < TheatreRoom.Capacity"
    cursor.execute(query)
    returnString = []
    for i in cursor:
        print(i)
        returnString.append(i)
    
    id = str(request.args.get('id'))
    
    cursor.close()
    cnx.close()
    return render_template('showings.html', data=returnString , type="Showing", id=id)

#add an attending
@customer_api.route("/addAttend", methods=["POST"]) 
def addAttend():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    #first check if this person has already attended this showing
    id = str(request.args.get('id'))
    showing = request.form.get('idShowing')
    query = ("select Showing_idShowing from Attend "
    "join Customer on Customer_idCustomer=idCustomer "
    "where idCustomer='%s'" % id)
    cursor.execute(query)
    
    returnString = []
    for i in cursor:
        print(i)
        returnString.append(i)
    
    #search through sttendings and see if you already joined it
    for attended in returnString:
        if str(attended[0]) == showing:
            return render_template('error.html', error="You have already attended this showing")
         
    #then add showing
    rating = request.form.get('rating')
    insert_query = ("insert into Attend(Customer_idCustomer,Showing_idShowing,rating) values(%s,%s,%s)" % (id, showing, rating))
    cursor.execute(insert_query)
    
    cnx.commit()
    cursor.close()
    cnx.close()
    return "Have fun at " + showing