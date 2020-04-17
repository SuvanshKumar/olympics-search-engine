import scrapy
from scrapy.linkextractors import LinkExtractor
import time
from url_download import download_webpage
import os
from datetime import datetime

start_time =datetime.now()

class OlympicSpider(scrapy.Spider):
    name = "olympic"
    start_urls = [
        'https://www.olympic.org',
    ]
    
    
    count_links = 0
    olympics_links = [] 
    queue = []

    exploration = True
    MAX_LINK_COUNT = 10000
    visited = 0

    def extract_and_enqueue_links(self, response):

        print("Vising URL: ",response.url)
        with open('linkslists.txt', 'a') as filehandle:
            filehandle.write('%s\n' % response.url)
        self.visited += 1
        # Downloading this webpage from the URL
        download_webpage(response.url, self.visited)
        print("Visited count: ", self.visited)
        self.olympics_links.append(response.url)

        title = response.css('title::text').get()
        content = response.css('p::text').getall()
    
        if self.exploration is True:  

            links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)  

            self.queue.extend(links)    

            self.count_links += len(links)

            if self.count_links >= self.MAX_LINK_COUNT:
                self.exploration = False

    

    def parse(self, response):
        
        self.extract_and_enqueue_links(response)

        while len(self.queue) != 0:

            print("Queue size: ", len(self.queue))
            # print(self.visited)
            time.sleep(0.001)   

            link = self.queue.pop(0)

            yield response.follow(link, self.extract_and_enqueue_links)


end_time =datetime.now()  
        
print("Total Time for crawling and downloading the webpages: ",end_time-start_time)

   # How to Run the file: scrapy runspider olympics_crawler.py
#    TODO Implement with BFS