import tweepy
import re
import simplejson as json
from pprint import pprint
from tweepy import Stream
from tweepy import OAuthHandler
import urllib2
from tweepy.streaming import StreamListener
import enchant
d = enchant.Dict("en_US")

ckey = 'lze9Mi5g41FjkGVpcLdJYkP9y'
csecret = 'yfScEAGi7y5yI8IMEc03jIUb1kFBbJKLqUA2zfqxPczwFBGH3N'
atoken = '131102157-v2fUUmK2sUdST54LWslJbdCCNXxG1Ah1BJgdP1Ph'
asecret = 'iSbCHbN3ntNxQgQK7WUEKL0ypVkj4kwbQGaJ2laglnGWN'
from nltk.corpus import wordnet
auth = OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
global a
a= 0
b=0
i=0
Glob_url = 0
Glob_hash = 0
Yes = 0
No= 0
Glob_Length = 0
newdict = {}
spell_mistake = 0
New_Dict_Word = 0
most_commonn_error = "a"
Eng_Alphabets = 'abcdefghijklmnopqrstuvwxyz'
New_Added ={}
def edit_distance1(word):
    splited_words    = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    inserted_words    = [x + z + y     for x, y in splited_words for z in Eng_Alphabets]
    replaced_words   = [x + z + y[1:] for x, y in splited_words for z in Eng_Alphabets if y]
    transposed_words = [x + y[1] + y[0] + y[2:] for x, y in splited_words if len(y)>1]
    deleted_words    = [x + y[1:] for x, y in splited_words if y]
    return set(inserted_words+replaced_words+transposed_words+deleted_words)

def dictionary_words(words):
    return set(w for w in words if d.check(w))

class listener(StreamListener):

    
    def on_data(self,data):
        global Glob_url,Glob_hash,i,Yes,No,Glob_Length,New_Dict_Word,spell_mistake,most_commonn_error,New_Added
        data2 = json.loads(data)
        i=i + 1
        tweet = data2['text'].encode('ascii', 'ignore')
        #tweet1 = tweet.split(' ')
        tweet1 = re.findall('[a-z]+', tweet.lower())
        if tweet1[0] =='RT':
            tweet1.pop(0)
            tweet1.pop(0)
        length =  len(tweet1)
        for k in range(length):
            word = tweet1[k]
            if len(word)>2:
                if not d.check(tweet1[k]):
                    No = No + 1
                    if len(dictionary_words(edit_distance1(word)))>=1:
                        if newdict.get(word):
                            newdict[word] = newdict[word]+1
                        else :
                            newdict[word]=1
                        spell_mistake = spell_mistake +1
                    else:
                        if New_Added.get(word):
                            New_Added[word]= New_Added[word]+1
                        else:
                            New_Added[word]=1
                            New_Dict_Word=New_Dict_Word+1
                    
                else:
                    Yes = Yes+1
        most_commonn_error = max(newdict.iterkeys(), key=lambda k: newdict[k])
        Glob_Length = Glob_Length+length
        url= len(data2['entities']['urls'])
        Glob_url  = Glob_url + url
        hashtag = len(data2['entities']['hashtags'])
        Glob_hash = Glob_hash + hashtag
        if i%10==0:
            print'Crunched ' + str(i) + " tweets and " + str(Glob_Length) +" Words"
            print 'found '+ str(spell_mistake) + ' spelling mistakes '
            print 'most common spelling mistake is ' + str(most_commonn_error)+ ' and this mistake has been repeated '+str(newdict[most_commonn_error]) +' number of times'
            print 'added '+str(New_Dict_Word)+ ' new words to the dictionary'
            #print 'Total number of Dictionary words are '+ str(Yes)
            #print "Total number of Non Dictionary words are "+ str(No)
            print "Total score of URLs are " + str(Glob_url)
            print "Total score of HASHTAGS are " + str(Glob_hash)
        
        return True
        

    def on_error(self,status):
       print 1


twitterStream = Stream(auth,listener())
twitterStream.filter(track =["help"])
