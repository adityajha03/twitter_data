import tweepy
import csv
from textblob import TextBlob

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_all_tweets(screen_name):
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#saving the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#grabbing tweets until there are no tweets left
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	for i in alltweets:
		analysis=TextBlob(i.text)
		sentimentAnalysis=analysis.sentiment


	user=api.get_user(25073877)
	#writing into csv	
	outtweets = [[user.name,user.screen_name,user.followers_count,tweet.user.id,tweet.place,user.description,tweet.created_at,tweet.id_str,tweet.text.encode("utf-8"),tweet.source,tweet.retweeted,tweet.in_reply_to_screen_name,tweet.in_reply_to_user_id,sentimentAnalysis] for tweet in alltweets]

	#write the csv	
	with open('realDonaldTrump.csv','w') as f:
		writer = csv.writer(f)
		writer.writerow(["name","username","Total followers","User ID","User place","User Description","Date of tweet","Tweet id","Tweet text","Tweet source","Tweet Retweeted","Tweet reply to name""id","Tweet reply to ID","Sentimental Analysis"])
		writer.writerows(outtweets)
	
	pass


if __name__ == '__main__':
	get_all_tweets("realDonaldTrump")