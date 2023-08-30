#Python program to build an ISS application

#~~Pseudo Code~~
#1) Create a Window
#2) Create a Menu
#3) Function to get the names of astronauts in the ISS
    # Get the data from the webservice
    # Extract the names from the data
    # Display the data
    # Connect the window to main menu
#4) Function to get the passtimes of the ISS over a location
    # Input latitude and longitude from the user
    # Get the data from the web service
    # Plot the position on the position
    # Display the data
#5) Function to find the current location of the ISS
    # Get the current location from the webservice
    # Extract the latitude and longitude
    # Get the name of the country
    # Display the data on the map
    # (Store the data in the data base)
#6) Create a database and related funtionalities
    # Insert data
    # Get the data
    # Delete data
#7) Function to track the live movement of the ISS
    # Fetch the data from the database
    # Plot it on the map
#8) Create the exit window

import time
import random
import turtle
import requests
from datetime import datetime#importing particular data(datetime) from datetimelibrary
import sqlite3
#StructuredQueryLanguage 

conn=sqlite3.connect('ISSdata.db')#creates/connects to database
c=conn.cursor()#(2D )data structure
c.execute('create table if not exists TrackData(Time text,Latitude float,Longitude float,Place text)')#to create a table

color_names=['orange red','yellow','lime','royal blue','dark violet','green','white','pink','brown','maroon','peach','silver'] 

def insert_data(time,latitude,longitude,place):
    with conn:#exception handling-prevents data being corrupted
        c.execute('insert into TrackData values(?,?,?,?)',(time,latitude,longitude,place))

def delete_data():#Function to delete the data
    with conn:
        c.execute('delete from TrackData')
        Track_ISS()
def get_data():
    c.execute('select * from TrackData')
    #function to fetch the data from the database
    return c.fetchall()
def exit_window():
    window.clearscreen()
    window.bgpic('Space2.gif')
    window.title('Exit')
    Display=turtle.Turtle()
    q=random.randint(0,5)
    Display.penup()
    Display.hideturtle()
    Display.color(color_names[q])
    Display.write('ThankYou!',align='center',font=('Freestyle Script',20,'bold'))
    
    time.sleep(3)
    window.bye()
    
def Track_ISS():#function to track the movement of the ISS
    window.clearscreen()
    window.bgpic('Map.gif')
    window.title('ISS Tracker')

    ISS=turtle.Turtle()    
    ISS.penup()
    ISS.hideturtle()
    ISS.color('white')
    ISS.right(90)
    ISS.goto(0,80)
    data=get_data()
    k=0
    if len(data)==0:#if the datab ase is empty
        ISS.write('Database empty!',align='center',font=('Freestyle Script',15,'bold'))
    else:
        for i in data:
            time=i[0]
            latitude=i[1]
            longitude=i[2]
            place=i[3]
            ISS.color(color_names[k])
            
            ISS.goto(longitude,latitude)
            ISS.dot(6)
            #ISS.forward(10)
            ISS.color('white')
            ISS.write('{} {}'.format(time,place),align='center',font=('Freestyle Script',12,'bold'))
            ISS.pendown()
            if k==4:
                k=-1
            k=k+1;
            
        ISS.penup()
        ISS.goto(0,80)
        ISS.write("Press'r'to delete data",align='center',font=('Freestyle Script',12,'bold'))
    display_message()
    window.listen()
    window.onkey(delete_data,'r')
    window.onkey(delete_data,'R')
    window.onkey(exit_window,'e')
    window.onkey(exit_window,'E')
    window.onkey(main_menu,'m')
    window.onkey(main_menu,'M') 
#[1,2,3]list
#(1,2,3)tuple - contents cannot be changed nor added nor deleted

def display_message():
    display=turtle.Turtle();
    display.penup()
    display.hideturtle();
    display.color('white')
    display.goto(0,-85)
    display.write('Press "M" for menu',align='center',font=('Freestyle Script',15,'bold'))
def astronauts_in_ISS():
    window.clearscreen()#clear the previous contents of the screen
    window.bgpic('Space2.gif')
    window.title('Astronauts in ISS')
    url='http://api.open-notify.org/astros.json'
    response=requests.get(url)# receive the response code from the specified url  
    data=response.json()
    # Response codes
    #200:Ok
    #404:Not found
    #400:Bad request
    astronaut_names=[]#list to store the names
    
    for i in data['people']:#list from people category in dat
        astronaut_names.append(i['name'])#name category from people

    ISS=turtle.Turtle()    
    ISS.penup()
    ISS.hideturtle()
    ISS.color('white')
    ISS.right(90)
    ISS.goto(-80,40)
    ISS.write('The following astronauts are in the ISS: ',align='left',font=(('Freestyle Script',18,'bold')))
    ISS.forward(15)
    k=0
    for j in astronaut_names:
        if k < 8 :
            ISS.forward(10)
            ISS.color(color_names[k])
            ISS.write(j,align='left',font=('Freestyle Script',12,'bold'))
            k=k+1
    display_message()   
    window.listen()
    window.onkey(main_menu,'m')


def ISS_passtimes():
    window.clearscreen()
    window.bgpic('Map.gif')
    window.title('ISS Passtimes')
    latitude=window.numinput('Latitude','Enter Latitude: ')
    longitude=window.numinput('Longitude','Enter Longitude')

    ISS=turtle.Turtle()
    ISS.penup()
    ISS.hideturtle()
    ISS.color('white')
    ISS.right(90)
    ISS.goto(0,80)
    #quary string is 'lat'and 'lon'
    parameters={'lat':latitude,'lon':longitude}#to send data to url
    url="http://api.open-notify.org/iss-pass.json"
    response=requests.get(url,params=parameters)#get the pass times
    #parameter is a dictionary like data in astronauts names
    #params is the key word for adding parameter
    #print(response.status_code)
    #data=response.json()
    #print(data)
    #Epoch time :1st Jan 1970 tillnow seconds ellapsed
    if  response.status_code !=200:#if the request is unsuccessful
        ISS.write('Invalid Coordinates',align='left',font=(('Freestyle Script',18,'bold')))
    else:
        data=response.json()
        epochtimes=[]#list to store the pass times

        for i in data['response']:#Extraxt risetimes
             epochtimes.append(i['risetime'])
             
        ISS.write('The next 5 passes of the ISS are:',align='left',font=('Freestyle Script',18,'bold'))
        ISS.goto(longitude,latitude)
        ISS.dot(6)
        k=0
        for j in epochtimes:
             ISS.forward(15)
             ISS.color(color_names[k])
             k=k+1
             ISS.write(datetime.fromtimestamp(j),align='left',font=('Freestyle Script',18,'bold'))
       #converting epoch time
    display_message()   
    window.listen()
    window.onkey(main_menu,'m')

def currentlocation():
    window.clearscreen()
    window.bgpic('Map.gif')
    window.title('Current Location')

    display_message()
    window.listen()
    window.onkey(main_menu,'m')

    url1='http://api.open-notify.org/iss-now.json'# to get the lat and long
    response1=requests.get(url1)
    data1=response1.json()
    #print(data1)
    time=datetime.fromtimestamp(data1['timestamp'])
    latitude=float(data1['iss_position']['latitude'])#to convert from string to float
    longitude=float(data1['iss_position']['longitude'])

    #longitude=72.9215
    #latitude=19.1254
    
    parameters={'lat':latitude,'lon':longitude,'format':'json'}#parameters
    #lat long format are the query type
    #to get the name of the place
    url2='https://us1.locationiq.com/v1/reverse.php?key=316aed2e9d379d'
    response2=requests.get(url2,params=parameters)
    data2= response2.json()
    #print(response2)
    #print(data2)

    ISS=turtle.Turtle()
    ISS.penup()
    ISS.hideturtle()
    ISS.color('white')
    ISS.right(90)
    ISS.goto(0,80)
    ISS.write('Current Location of the ISS',align='center',font=('Freestyle Script',18,'bold'))

    ISS.goto(longitude,latitude)
    ISS.dot(6)
    ISS.forward(15)

    place=''
    k=random.randint(0,4)
    ISS.color(color_names[k])
    #print(data2)
    if response2.status_code==200:#if the iss is over the country
        place=data2['address']['country']
        ISS.write(place,font=('Freestyle Script',18,'bold'))
    else:
        place='Ocean'
        ISS.write(place,font=('Freestyle Script',18,'bold'))

    insert_data(time,latitude,longitude,place)
          
    
def main_menu(): # function to display the main menu
    window.clearscreen()
    #window.bgpic('Space2.gif')
    window.bgpic('Space2.gif')
    window.title('Main Menu')
    menu=turtle.Turtle()
    menu.hideturtle()
    menu.penup()
    menu.color('white')
    menu.goto(0,60)
    menu.write('~~~ Explore Space ~~~',align='center',font=('Freestyle Script',24,'bold'))
    menu.goto(-140,30)
    menu.color('orange red')
    menu.right(90)
    menu.write('(a) Astronauts in the ISS',align='left',font=('Freestyle Script',18,'normal'))
    menu.color('yellow')
    menu.forward(20)
    menu.write('(b) Passtimes over a location',align='left',font=('Freestyle Script',18,'normal'))
    menu.color('lime')
    menu.forward(20)
    menu.write('(c) Current location',align='left',font=('Freestyle Script',18,'normal'))
    menu.color('royal blue')
    menu.forward(20)
    menu.write('(d) Track the ISS',align='left',font=('Freestyle Script',18,'normal'))
    menu.color('dark violet')
    menu.forward(20)
    menu.write('(e) Exit',align='left',font=('Freestyle Script',18,'normal'))
    menu.forward(20)

    window.listen()
    window.onkey(astronauts_in_ISS,'a')
    window.onkey(ISS_passtimes,'b')
    window.onkey(astronauts_in_ISS,'A')
    window.onkey(ISS_passtimes,'B')
    window.onkey(currentlocation,'c')
    window.onkey(currentlocation,'C')
    window.onkey(Track_ISS,'d')
    window.onkey(exit_window,'e')
    window.onkey(exit_window,'E')
#creating a window
window=turtle.Screen()

window.setup(820,460)
window.setworldcoordinates(-180,-90,180,90)# set the coordinates system to match the world
main_menu()
window.mainloop()# keep the application running










 

 
