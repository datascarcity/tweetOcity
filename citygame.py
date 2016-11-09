import tweepy
import time
import random
import urllib

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

#MAIN VARIABLES
lat = 0 #Starting latitude and longitude
lon = 0
sleeping = 60 #Defines the waiting time between the tweets in seconds
increase = 0.10 #Defines the coordinates increment
iteration = 35 #Number of iterations counter
zoom = 15 #Zoom Level
random.seed()

#OPENING THE CITIES DATABASE
with open('cities.txt') as f:
    numcities =  sum(1 for _ in f)
    f.close()
    
cities = open('cities.txt','r') #thanks to gael varoquaux for this file
cities = cities.readlines()

#MAIN LOOPS GENERATING THE IMAGE
while True:
    api.update_status("Get ready! A new #quiz will be published in 10 minutes! Quiz nr. "+str(iteration))
    time.sleep(10)
    n = random.randrange(1,numcities,1)
    print cities [n]
    cityline = cities[n]
    cityline = cityline.rstrip()
    cityline = cityline.split('\t')
    print cityline
    lon = cityline[1]
    lat = cityline[2]
    zoom = 15
    test = "https://maps.googleapis.com/maps/api/staticmap?center="+str(lat)+","+str(lon)+"&zoom="+str(zoom)+"&size=640x640&maptype=satellite"
    urllib.urlretrieve(test, "image"+".png") #Saves the image overwriting the existing one
    time.sleep(5) #gives time to fetch the content and save it
    api.update_with_media('image.png',"Guess the city! You have 12 hours to reply and win. Quiz nr. "+str(iteration))
   # api.update_with_media('image.png',"A random piece of earth. "+cityline[0]+" Lat: "+str(lat)+" Lon: "+str(lon))
    time.sleep(sleeping)
    api.update_status("Nobody has guessed yet... so let's make it easier. Quiz nr. "+str(iteration))
    zoom = 10
    test = "https://maps.googleapis.com/maps/api/staticmap?center="+str(lat)+","+str(lon)+"&zoom="+str(zoom)+"&size=640x640&maptype=satellite"
    urllib.urlretrieve(test, "image"+".png") #Saves the image overwriting the existing one
    time.sleep(5) #gives time to fetch the content and save it
    api.update_with_media('image.png',"Here it comes a wider view. You have 6 hours left to guess... Quiz nr. "+str(iteration))
    time.sleep(sleeping)
    tweets = api.home_timeline()
    print len(tweets)
    print type(tweets)
    t = [cityline[0]]
    print t
    for s in tweets:
        for i in t:
            if i == s.text:
                sn = s.user.screen_name
                m = str(sn)+"got it right"
                api.update_status(m)
        print s.text
    iteration = iteration +1
"""
twts = api.search(q="aribot")     
 
#list of specific strings we want to check for in Tweets
t = ['aribot']
 
for s in twts:
    for i in t:
        if i == s.text:
            sn = s.user.screen_name
            m = "@%s Hello again again meow!" % (sn)
            s = api.update_status(status=m)
"""
