# Olympics Search Engine
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

For more information on the Olympics search engine, refer "Project 8 Report Olympics Games.pdf".
