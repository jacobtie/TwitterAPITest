import tweepy
import heapq
# import time

class SingleTweet:
    def __init__(self, screenName, postTime, tweetText, followersCount, retweetCount):
        self.screenName = screenName
        self.postTime = postTime
        self.tweetText = tweetText
        self.followersCount = followersCount
        self.retweetCount = retweetCount

def findHighestNUsers(tweetList, n):
    userList = []
    for tweet in tweetList:
        userList.append(tweet.screenName.screen_name)
    
    userSet = set(userList)
    userDict = {}
    for user in userSet:
        userDict[user] = 0
    
    for tweet in tweetList:
        userDict[tweet.screenName.screen_name] = userDict[tweet.screenName.screen_name] + 1
        
    return heapq.nlargest(n, userDict, key=userDict.get)
    
def mostFollowers(tweetList, n):
    userList = []
    uniqueTweets = []
    uniqueTweetsUsers = []
    for tweet in tweetList:
        if tweet.screenName.screen_name not in uniqueTweetsUsers:
            uniqueTweetsUsers.append(tweet.screenName.screen_name)
            uniqueTweets.append(tweet)
    for tweet in uniqueTweets:
        userList.append(tweet.screenName)
    
    userSet = list(set(userList))
    userDict = {}
    for user in userSet:
        userDict[user] = user.followers_count
    return heapq.nlargest(n, userDict, key=userDict.get)

def mostRetweets(tweetList, n):
    tweetDict = {}
    uniqueTweets = []
    uniqueTweetsText = []
    for tweet in tweetList:
        if tweet.tweetText not in uniqueTweetsText:
            uniqueTweetsText.append(tweet.tweetText)
            uniqueTweets.append(tweet)
    for tweet in uniqueTweets:
        tweetDict[tweet] = tweet.retweetCount
    return heapq.nlargest(n, tweetDict, key=tweetDict.get)

ACCESS_TOKEN = '479067544-i7g0ea36ba4VkJ9G9tgofRAyaQ6EA20imFl5qoiZ'
ACCESS_SECRET = 'YWbSOfq9RfJppctzIHElrqo7qj0rXWVc0Blay1omlTvlv'
CONSUMER_KEY = 'yNV1CTzcDSHxmCZl5J4JYoIBh'
CONSUMER_SECRET = 'bTpQshWwoirJ9AyRqYBjZBwwHjgxkda8qHAntmf2lOmkPPRL7a'
SEARCH=input("Enter the search string ")
FROM=input("Enter the from date (YYYY-MM-DD format) ")
TO=input("Enter the to data (YYYY-MM-DD format) ")
INPUT_FILE_PATH= './'+SEARCH+'.txt'

num=int(input("Enter the number of tweets you want to retrieve for the search string "))
auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
i=0;

f = open(INPUT_FILE_PATH, 'w', encoding='utf-8')
tweetList = []

for res in tweepy.Cursor(api.search, q=SEARCH, rpp=100, count=20, result_type="recent", since = FROM,until =TO, include_entities=True, lang="en").items(num):
	tweetList.append(SingleTweet(res.user, res.created_at.strftime("%d/%b/%Y:%H:%M:%S %Z"), res.text.replace('\n',''), res.user.followers_count, res.retweet_count))
	f.write(tweetList[i].screenName.screen_name)
	f.write(' ')
	f.write('[')
	f.write(tweetList[i].postTime)
	f.write(']')	
	f.write(" ")
	f.write('"')
	f.write(tweetList[i].tweetText)
	f.write('"')
	f.write(" ")
	f.write(str(tweetList[i].followersCount))
	f.write(" ")
	f.write(str(tweetList[i].retweetCount))
	f.write('\n')
	i+=1
f.close()
print("Tweets retrieved ",i)

n = int(input("Enter a value n: "))
largestTweetsFile = open('./'+SEARCH+'_mosttweetsusers.txt', 'w', encoding='utf-8')
for item in findHighestNUsers(tweetList, n):
    largestTweetsFile.write(item)
    largestTweetsFile.write('\n')
largestTweetsFile.close()
mostFollowersFile = open('./'+SEARCH+'_mostfollowers.txt', 'w', encoding='utf-8')
for item in mostFollowers(tweetList, n):
    mostFollowersFile.write(item.screen_name)
    mostFollowersFile.write('\n')
mostFollowersFile.close()
mostRetweetsFile = open('./'+SEARCH+'_mostretweets.txt', 'w', encoding='utf-8')
for item in mostRetweets(tweetList, n):
    mostRetweetsFile.write(item.tweetText)
    mostRetweetsFile.write('\n')
mostRetweetsFile.close()
