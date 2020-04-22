import scrapy
from scrapy.linkextractors import LinkExtractor
import time
from url_download import download_webpage
import os
from datetime import datetime

start_time =datetime.now()

class OlympicSpider(scrapy.Spider):
    name = "olympic"
    # These are the seed,inks
    start_urls = [
    'https://www.olympic.org', 'https://tokyo2020.org/en/',
    'https://www.nbcolympics.com/', 'https://www.teamusa.org/', 'https://www.olympicchannel.com/en/', 'https://www.loc.gov/rr/main/olympics/internet.html',
    'https://www.specialolympics.org/', 'https://www.soiowa.org/', 'https://www.2022specialolympicsusagames.org/', 
    'https://www.espn.com/olympics/', 'https://www.nytimes.com/section/sports/olympics', 'https://www.britannica.com/sports/Origins-of-the-Olympic-Winter-Games',
    'https://www.bbc.com/sport/olympics/rio-2016', 'https://www.cbssports.com/olympics/', 'https://www.foxsports.com/olympics', 
    'http://en.beijing2008.cn/en/','https://www.abc.net.au/news/rio-olympics-2016/','https://www.worldathletics.org',
    'https://www.olympic.org/vancouver-2010','https://www.olympic.org/london-2012','https://www.cbc.ca/sports/olympics','https://sports.yahoo.com/olympics/pyeongchang-2018/',
    'https://www.factmonster.com/features/olympics', 'https://olympics.nbcsports.com/', 'https://www.foxnews.com/category/sports/olympics',
    'https://www.livescience.com/26654-olympia.html','https://www.olympicchannel.com/en/sports/','https://www.sciencekids.co.nz/sciencefacts/sports/summerolympics.html',
    'https://www.sciencekids.co.nz/sciencefacts/sports/winterolympics.html','https://www.loc.gov/rr/main/olympics/dates.html',
    'https://time.com/5689792/2020-tokyo-olympics-when-where/' ,'https://www.timeanddate.com/events/summer-olympic-games.html',
    'https://web.archive.org/web/20081009043255/http://www.sok.se/inenglish/stockholmmelbourne1956.4.18ea16851076df63622800011093.html',
    'https://sok.se/om-webbplatsen/webbkarta.html', 'https://www.paralympic.org/powerlifting','https://web.archive.org/web/20110429094019/http://multimedia.olympic.org/pdf/en_report_1138.pdf',
    'https://web.archive.org/web/20090324234949/http://multimedia.olympic.org/pdf/en_report_1303.pdf', 'https://olympics.fandom.com/wiki/Athens_2004',
    'http://www.frbsf.org/economic-research/files/wp09-06bk.pdf','https://web.archive.org/web/20070927021042/http://www.fasterskier.com/racing4278.html','https://www.disabled-world.com/sports/paralympics/'
                ]

    count_links = 0
    olympics_links = [] 
    queue = []

    exploration = True
    MAX_LINK_COUNT = 100000
    visited = 0

    def extract_and_enqueue_links(self, response):

        print("Vising URL: ",response.url)
        with open('linkslists.txt', 'a') as filehandle:
            filehandle.write('%s\n' % response.url)
        self.visited += 1
        # Downloading this webpage from the URL
        # download_webpage(response.url, self.visited)
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