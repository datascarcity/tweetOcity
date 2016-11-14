import tweepy
import time
import random
import urllib
from dbfread import DBF

#AUTHENTICATION
key = open('keys', 'r') #opens the file with the secret keys

CONSUMER_KEY = key.readline().rstrip() #reads each line and strips the NewLine
CONSUMER_SECRET = key.readline().rstrip()
ACCESS_KEY = key.readline().rstrip()
ACCESS_SECRET = key.readline().rstrip()
key.close()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#LOADING THE TABLE FILE, IT ACTUALLY LOAD ALL THE FILE
cities = DBF('ne_10m_populated_places_simple.dbf', load=True)

#MAIN VARIABLES
lat = 0 #Starting latitude and longitude
lon = 0
sleeping = 21600 #Defines the waiting time between the tweets in seconds
iteration = 0 #Number of iterations counter
zoom = 15 #Zoom Level
numcities = len(cities)
random.seed()

#MAIN LOOPS GENERATING THE IMAGE
while True:

    n = random.randrange(1,numcities,1)
    while cities.records[n]['scalerank']>3: #Picks a city only if it is big enough to be known
        n= random.randrange(1,numcities,1)
    
    print cities.records[n]['name']
    print cities.records[n]['longitude']
    print cities.records[n]['latitude']
    city = cities.records[n]['name']
    lon = cities.records[n]['longitude']
    lat = cities.records[n]['latitude']
    rank = cities.records[n]['scalerank']
    country = cities.records[n]['sov0name']
    region = cities.records[n]['adm1name']
    inhab =  cities.records[n]['pop_max']
    zoom = 15
    iteration = iteration +1

    #
    #GAME
    #

    api.update_status("Get ready! A new #quiz will be published in 10 minutes! Quiz nr. "+str(iteration))

    time.sleep(600)
    test = "https://maps.googleapis.com/maps/api/staticmap?center="+str(lat)+","+str(lon)+"&zoom="+str(zoom)+"&size=640x640&maptype=satellite"
    urllib.urlretrieve(test, "image"+".png") #Saves the image overwriting the existing one
    time.sleep(5) #gives time to fetch the content and save it
    api.update_with_media('image.png',"Guess the city! You have 12 hours to reply and win. Quiz nr. "+str(iteration))
   # api.update_with_media('image.png',"A random piece of earth. "+cityline[0]+" Lat: "+str(lat)+" Lon: "+str(lon))
    time.sleep(sleeping)

    api.update_status("Nobody has guessed yet... so let's make it easier. Quiz nr. "+str(iteration))
    zoom = 14
    test = "https://maps.googleapis.com/maps/api/staticmap?center="+str(lat)+","+str(lon)+"&zoom="+str(zoom)+"&size=640x640&maptype=satellite"
    urllib.urlretrieve(test, "image"+".png") #Saves the image overwriting the existing one
    time.sleep(5) #gives time to fetch the content and save it
    api.update_with_media('image.png',"Here it comes a wider view. You have 6 hours left to guess... Quiz nr. "+str(iteration))
    time.sleep((sleeping / 2))

    api.update_status("Still nothing... Then you should know that the city is in "+country+ ". Three hours to go. Quiz nr. "+str(iteration))
    time.sleep(sleeping/6*2)

    api.update_status("Last clue, it is in the "+region+" region. Last chance to answer! One hour to go! Quiz nr. "  +str(iteration))
    time.sleep(sleeping/6)
    api.update_status("The time is over! Let's see the results of Quiz nr. "+ str(iteration))

    #
    #RESULTS CHECK
    #

    tweets = api.home_timeline()
    print len(tweets)
    print type(tweets)
    print city
    for s in tweets:
        for i in city:
            if i == s.text:
                sn = s.user.screen_name
                m = str(sn)+"got it right! Congratulations!"
                api.update_status(m)
                api.update_status("The city is " + name + "! It is situated in "+ country + " and it has " +str(inhab) + " inhabitants!")
            else:
                api.update_status("Nobody got it right... The city is " + city + "! It is situated in "+ country + " and it has " + str(inhab) + " inhabitants!")
                
    time.sleep(600)
