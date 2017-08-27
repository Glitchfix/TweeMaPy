from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pygeocoder import Geocoder
import sys
import json
import matplotlib.pyplot as plt

#Variables that contains the user credentials to access Twitter API 
access_token = "ACCESS TOKEN"
access_token_secret = "ACCESS TOKEN SECRET"
consumer_key = "CONSUMER KEY"
consumer_secret = "CONSUMER SECRET"
log=open('data.json','a')

n=int(raw_input('Enter number of tweets: ')) #Number of tweets to filter from the stream

x,y=[],[] #X and Y axis data

#Listens to the Tweet stream
class StdOutListener(StreamListener):
	i=0 #Counter for tweets
	drop=0 #Count dropped addresses
	
	
	def on_data(self, data):
		scrap=json.loads(data) #Unicode to JSON

		g=scrap['user']['location'] #Location column
		print g
		try: #to prevent invalid location to get through and generate error
			coord=Geocoder.geocode(g) #Parsed to Geocoder to obtain the address on Google Map
			lat,lon=coord.coordinates #Coordinates assigned
			print lat,lon
			x.append(lon-2) #longitude added to x-axis
			y.append(lat-14) #latitude added to y-axis
		except: #Count the number of invalid addresses encountered
			self.drop+=1
			pass
		log.write('\n'+data+'\n') #append the data scrapped into file
		self.i+=1
		print self.i
		if self.i==n:
			print 'Number of drops: ',self.drop
			plt.ion() #Switches on interactive mode 
			img = plt.imread("world.jpg") #backgroud image(The map)
			fig, ax = plt.subplots() #Generates subplot layer
			ax.imshow(img, extent=[-180, 180, -90, 90]) #x and y axis limits
			ax.plot(x, y, '.', linewidth=1, color='blue') #Scatter plot implemented
			raw_input("Press enter to exit") #Press enter to exit
			return False #Stops reading further data
		else:
			return True #Continues reading
			
			
	def on_error(self, status):
		print 'Error code: ',status #Shows error in connecting to the API


if __name__ == '__main__':
	l = StdOutListener() #Listener object
	auth = OAuthHandler(consumer_key, consumer_secret) #O-Auth handler
	auth.set_access_token(access_token, access_token_secret) #Access token for API
	stream = Stream(auth, l) #Stream object to interact with the stream of tweets
	stream.filter(track=[raw_input("Enter your keyword: ")]) #Filter tweets based on keyword
	sys.exit() #Exit the application
