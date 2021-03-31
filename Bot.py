import random
import sys
import time
import os

prereq = ['pandas', 'pytrends','webbrowser','googlesearch']
def check_import(package):
    try:
        __import__(package)
    except ImportError:
        print(package, " not found please make sure it is installed")

for i in prereq:
    check_import(i)


import pandas as pd
from pytrends.request import TrendReq
import webbrowser
from googlesearch import search



"""
    Function to get amount of time to run program for
"""

def get_time():
     
     while True:
         try:
             time_to_run = int(input("How many minutes do you want to run the search for"+
                                     " please enter a whole number"))
             
             break
         except ValueError:
             print("Please enter a number")
     return round(time_to_run * 60,0)

""" 
    Helper function responsible for calculating probabilites that each
    search result will be opened
"""

def start_up_prob():
    #Weights start at lower bound a random amound added each time which
    #doesn't exceed the upper bound
    adjusted_weights = []
    adjusted_weights.append(25 + round(random.uniform(1, 7),1))
    adjusted_weights.append(15 + round(random.uniform(1,9),1))
    adjusted_weights.append(11 + round(random.uniform(1,7),1))
    adjusted_weights.append(8 + round(random.uniform(0.5,4),1))
    adjusted_weights.append(7 + round(random.uniform(0.5,2),1))
    
    constant_weightings = [5.1,4,3.2,2.8,2.6]
    
    #Final weightings 
    url_weightings = adjusted_weights + constant_weightings
    url_weightings = [round(i/100,2) for i in url_weightings]
    
    return url_weightings


class PrivacyBot():
       
    def __init__(self, weightings):
        self.weightings = weightings
        self.open_tabs = 0
    
    """ 
    This method is responsible for retrieving a single search term from the
    text file containing over 300,000 unique words.
    
    """

    def get_keyword(self):
    #If the text file is not found exit program
        try:
            file_words = open("words_alpha.txt")
        except FileNotFoundError:
            print("File 'words_alpha.txt' was not found please ensure this file is " 
                     "in the same folder as this python file.")
            sys.exit()
            
        line_to_select = random.randint(0, 370103)
        self.keyword = ''
        count = 0   
        for line in file_words:
            count+=1
            if count == line_to_select:
                self.keyword = line.rstrip()
                break        
        file_words.close()
    
    """     
    This method is responsible for taking the selected keyword and getting
    all related querys from google trends. If there is no related querys the 
    keyword is used alone.
    
    If more than 10 querys are returned we want to take at least 5 of them to 
    make it look like you have an interest in that subject.

    """
        
    def get_search_terms(self):

        #Retrival of data from Google Trends
        pytrends = TrendReq(hl='en-US',tz=360)
        keywords = [self.keyword]
        pytrends.build_payload(kw_list=keywords, timeframe='today 5-y', geo='',gprop='')
        data = pytrends.related_queries()
        top_related_querys = pd.DataFrame(data[keywords[0]]['top'])
        querys_to_use = []
       
        
        #Random.sample requires a sequence or set so the numbers in this relate
        #To the index positon of elements in top_related_querys
        mapping_list = [i for i in range(0,len(top_related_querys))]
        
        #If no related query we just use the keyword
        if len(top_related_querys) == 0:
            return [self.keyword]
        elif len(top_related_querys) > 10:
            number = random.randint(5,10)
        else:
            number = random.randint(1, len(top_related_querys))
        
        for i in random.sample(mapping_list, number):
            querys_to_use.append(top_related_querys.iloc[i]['query'])
            
        return querys_to_use
    
    """
    Method responsible for getting number of urls to vist.
    Will always return at least 1 link
    
    """
    
    
    
    def get_num_url(self):
    
        num_url_visit = []
        isEmpty = True 
        #Loop ensures at least 1 url selected
        while isEmpty:
            for i in range(0,len(self.weightings)):         
                if random.random() <= self.weightings[i]:
                    num_url_visit.append(i)
                    isEmpty = False      
        return num_url_visit
    
    """Method to actually preform searchs and open links"""
    
    def run(self):
        self.get_keyword()
        search_querys = self.get_search_terms()
        """Search each query in Google"""
        for i in search_querys:
            self.check_tabs()
            urls = [x for x in search(query=i,tld='co.in',lang='en',num=10,stop=10,pause=2)]         
            webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=%s' % i)
            self.open_tabs += 1
            time.sleep(5)
            """Get number of links to use"""
            number_of_url = self.get_num_url()
            """Open the corresponding links"""
            for i in number_of_url:
                self.open_tabs += 1
                webbrowser.open_new_tab(urls[i])
                time.sleep(random.randint(30, 60))
   
    """Method to ensure we don't have to many open tabs"""
    
    def check_tabs(self):
        if self.open_tabs >= 12:
            browserExe = "chrome.exe" 
            os.system("taskkill /f /im "+browserExe) 
            self.open_tabs = 0
        




timeout = get_time()
weightings = start_up_prob()
bot = PrivacyBot(weightings)
time_start = time.time()

while time.time() < time_start + timeout:
    bot.run()
 

browserExe = "chrome.exe" 
os.system("taskkill /f /im "+browserExe)   
sys.exit()
    


