# WikiSpider
Wikipedia spider that attempts to reach philosophy

This Wikipedia Crawler clicking on the first link in the main body of a Wikipedia article and repeating the process for subsequent 
articles till it leads to the article Philosophy.

The program should receive a Wikipedia link as an input, go to another normal link and repeat this process until either 
Philosophy page is reached, or we are in an article without any outgoing Wikilinks, or stuck in a loop.

A "normal link" is a link from the main page article, not in a box, is blue (red is for non-existing articles), 
not in parentheses, not italic and not a footnote.  the script works with the current Wikipedia style as of July 2019.

This script uses Scrapy for the crawling functions and beacutifulsoap for component manipulation funtions.

To run this script you should have Scrapy and Pythom 3+ installed, I utilized Anaconda for both installations, though any other method should be sufficient.

To run the script simply go to the script directory and run the below command:
scrapy runspider spider.py -a start_url="https://en.wikipedia.org/wiki/Special:Random"
or you can replace the random page with any Wikipedia page of your choice.
