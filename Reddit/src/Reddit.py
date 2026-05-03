import os
import sys

import PySimpleGUI as sg


def resolve_path(path):

        if getattr(sys, "frozen", False):
            # If the 'frozen' flag is set, we are in bundled-app mode!
            resolved_path = os.path.abspath(os.path.join(sys._MEIPASS, path))
        else:
            # Normal development mode. Use os.getcwd() or __file__ as appropriate in your case...
            resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))

        return resolved_path
    
sys.path.append(os.path.abspath(resolve_path("reddit/src")))
from RedditData import reddit_data


class reddit_interface:

    def __init__(self, window):
        self.window = window
        self.myRedditData = reddit_data()
        self.newlyScraped = []

    
    def scrape(self, numPosts):
        xx = 1
        number_appened = 0
        try:
            #print(self.myRedditData.querys)
            for _sub in self.myRedditData.subs:
                curr_sub = self.myRedditData.reddit.subreddit(_sub)
                for _query in self.myRedditData.querys:
                    for post in curr_sub.search(query=_query, sort="new", limit=int(numPosts)):
                        
                        self.window["-scrape_output-"].print(str(xx) + " posts scraped. Currently scrapping: " + str(_sub))
                        xx +=1
                        if(xx %10 == 0):
                            self.window["-scrape_output-"].print("note that not all scraped posts are valid...", font='Courier 12', colors='black on blue')

                        if not(post.stickied) and not(post.id in self.myRedditData.ids):
                            self.newlyScraped.append(self.myRedditData.reddit.submission(post.id))
                            number_appened +=1 #this is for the progress bar and the number of posts in the GUI
                        if(number_appened == int(numPosts)):
                            break
                            #self.myRedditData.ids.append(post.id)
                    if(number_appened == int(numPosts)):
                        break
                
        except Exception as e:
            print(e)
            self.window["-scrape_output-"].print("Error when scrapping.. probably some input, check subreddits?")
                    
                    
    def chatRespond(self):
        pass
    
    def dmRespond(self):
        pass
    
    def generateResponse():
        pass
    
    def updateSubreddits(self, subreddits):
        self.myRedditData.subs = subreddits
        self.myRedditData.pickleMe()
    
    def updateQuerys(self, querys):
        self.myRedditData.querys = querys
        
        
    def updateMessage(self, message):
        self.myRedditData.message = message
        self.myRedditData.pickleMe()
        
    def getTitles(self):
        out = []
        for x in self.newlyScraped:
            out.append(x.title)
        return out
        