# Youtube-API-Low-High-views-video-getter-by-query
A code that uses youtube api v3 in order to get videos with a certain number of views that you decide

In order to make this code works you're gonna need a working api v3 key for youtube, iots easy and free to get it, follow this tutorial:https://blog.hubspot.com/website/how-to-get-youtube-api-key

After that change the values of the variables that I pinned, the code will make a set of chunks (you can decide how many) of query search with youtube, then will process all the urls that you got in order to save only the videos with a certain number of views. You can decide the value, if its gonna be lower than x_views or higher than x_views exc...
I implemented a system that will save you the last nextPageToken value that you got form the response. This can be useful if you want to resume a certain query search from the point where you stopped, of course use it across a run of the code and another but don't change the query string search. If you don't want to use it simply erase it from the "nextPageToken.txt" file, or modify the code.


Packages needed: requests, BeautifulSoup