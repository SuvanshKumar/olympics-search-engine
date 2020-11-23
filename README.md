# Olympics Search Engine
![alt text](https://github.com/sadam-99/Olympics-Search-Engine/blob/master/UI-Front-End/homepage.png?raw=true)


Created this search engine specifically based on the Olympics. Like if a user wants to search for a specific olympics sports or medalists winners, our search engine is displaying the results according to the searched query. So in our search engine we crawled the data via Apache Nutch from specific seed links which are related to the olympics only, then we created the indexing based on the Crawled data from Apache Solr. We could manage to crawl only 100000 web pages so the results are not that good which are supposed to be in order to improve the search query we could crawl for 1 billion web pages. The clustering is also performed to improve the results from our relevance model. The Page ranking is also performed in order to display the top results at the top so that the users don’t need to scroll much in order to search for the results. The UI which we have created is pretty simple it is displaying the Title, URL and the small content of the webpage, this could be enhanced to images and videos as well just like Google but we need trillions of web pages to crawl and the indexing and the clustering files will also be so huge, So our search engine was giving pretty good and similar results with many of the Olympic medalists searches on our Search Engine like Michael Phelps and Carl Lewis who are the greatest olympics athletes of all time.

A search engine built to retrieve the information about any Olympics Games and related to those events and Players.

# Crawling
Apache Nutch is used to crawl the relevant web pages from the 76 seed URLs(related to Official Olympics websites) given.

# Indexing
Apache Solr is used to index the crawled web pages. The default page rank model of indexing using solr gives satisfactory results. The results are further improved by implementing and applying HITS algorithm.

# User Interface(UI-Front End)
The results obtained using different indexing methods, different clustering methods and different query expansion methods are compared with the results obtained on the same query using Google and Bing.

# Clustering
Both flat clustering (K-means) as well as hierarchical clustering (single-link) is used to group similar web pages together, and improve search results.

# Query Expansion
Associative, metric and scalar clustering are used to get the new, modified, enhanced expanded query to improve search results.
![alt text](https://github.com/sadam-99/Olympics-Search-Engine/blob/master/UI-Front-End/homepage1.png?raw=true)

For more information on the Olympics search engine, refer "Project 8 Report Olympics Games.pdf".
