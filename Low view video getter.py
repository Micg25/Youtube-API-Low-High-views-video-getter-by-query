import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time

session = requests.session()
 

api_key="" #Insert your api key here

weeks = datetime.now() - timedelta(weeks=2)
days  = datetime.now() - timedelta(days=5)
query_string="" #insert your query string here
chunks=5    #number of chunks of search query the code will do
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}


params = {
    "part": "snippet",
    "q":f"{query_string}",
    "type":"video",
    "order": "relevance",
    "publishedAfter":(str(days.isoformat())+"Z"),  #will fetch the videos published after a certain date, the format is: RFC 3339 (1970-01-01T00:00:00Z).
    "regionCode":""     #put your regionCode Here
    
}

startToken=""

with open ("nextPageToken.txt","r") as file:      #will read in the nextPageToken file if there is actually something, if there is it will take the last nextPageToken value
    for line in file:                             #and it will start the next fetch from this value 
        startToken=str(line.strip())              #this is useful if you want to search for the same query but in different moments, so you can resume your search where you stopped it

with open("current_url.txt","w") as file:  #it will save all of the urls fetched in the current_url file
    if(startToken!=""):                    #if there was a start token in nextPageToken.txt it will start from that
        print("start token found:", startToken)
        nextPageToken=str(startToken)
        response = session.get(f"https://www.googleapis.com/youtube/v3/search?key={api_key}", params=params)
        print(response.status_code)
        soup=response.json()
        for item in soup["items"]:
            file.write(f'https://www.youtube.com/watch?v={str(item["id"]["videoId"])}'+"\n")

    else:      #if there is no start token found it will proceed making the first request not specifying it
        response = session.get(f"https://www.googleapis.com/youtube/v3/search?key={api_key}", params=params)
        print("first response",response.status_code)
        soup=response.json()
        for item in soup["items"]:
            file.write(f'https://www.youtube.com/watch?v={str(item["id"]["videoId"])}'+"\n")
    
    for i in range (chunks): #actual iterator of all the chunks
        time.sleep(2)
        print("chunk:",i)
        if "nextPageToken" in soup:
            nextPageToken=soup["nextPageToken"]
            params["pageToken"]=str(nextPageToken)
            response = session.get(f"https://www.googleapis.com/youtube/v3/search?key={api_key}", params=params)
            soup=response.json()
            print(response.status_code)
            for item in soup["items"]:
                file.write(f'https://www.youtube.com/watch?v={str(item["id"]["videoId"])}'+"\n")
        else:
            break

urls=[]


with open ("low_views_url.txt","w", encoding="utf8") as lowfile:     
    with open("current_url.txt", "r", encoding="utf8") as file:
        for line in file:                                           #this cycle will iter all of the urls fetched before one by one 
            response = requests.get(line.strip())                   #in order to check if the visuals are lower than a certan value
            print("searching low views videos: ", response.status_code)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                script_tags = soup.find_all("script")

                for script in script_tags:
                    if "viewCount" in str(script):
                        #regex
                        view_count_match = re.search(r'"viewCount":"(\d+)"', str(script))
                        title_match = re.search(r'"title":"([^"]+)"', str(script))
                        title = title_match.group(1)
                        print(str(title))
                        if view_count_match:
                            view_count_str = view_count_match.group(1)
                            view_count_str = view_count_str.replace(".", "")
                            view_count = int(view_count_str)
                            print(f"{str(title)} Visualizzazioni: {view_count}")

                            if view_count <= 20:  #if the views are lower than "20" this code will write it in the "low_views_url.txt" file
                                lowfile.write(str(line.strip())+" "+str(title)+" "+"Visualizzazioni:"+str(view_count)+"\n")
                        

with open("nextPageToken.txt","w") as file: #saving the last nextPageToken
        file.write(str(nextPageToken))      #if you don't want to use it in the next run you can simply delete it from the "nextPageToken.txt" content