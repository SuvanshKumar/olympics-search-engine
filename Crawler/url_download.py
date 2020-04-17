# import urllib.request, urllib.error, urllib.parse
import nltk   
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

webpage_dir = r"Webpages"
# webpage_count = 1
        
def download_webpage(url, webpage_count):

    
    html = urlopen(url).read()    
    # html = html.decode('utf-8')

    # html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    txt = '\n'.join(chunk for chunk in chunks if chunk)
    text = txt.encode('unicode-escape').decode('utf-8')
    text = text.replace("\n", " ")
    # print(text)
    page = "webpage" + str(webpage_count) +  ".txt"
    # webpage_count = webpage_count + 1
    filename = os.path.join(webpage_dir, page)
    with open(filename, 'w') as filehandle:
                filehandle.write('%s\n' % text)


if __name__ == '__main__':
    url = 'https://www.olympic.org/los-angeles-1932' 
    download_webpage(url)
