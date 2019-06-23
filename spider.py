import scrapy
import time
from bs4 import BeautifulSoup

#Function to remove () and it's contents from paragraphs, check <> to not mess up links
def remove_parentheses(html):
  paren_count = 0
  bracket_count = 0
  result = ""
  for char in html:
    if char == '<':
      bracket_count += 1
    elif char == '>':
      bracket_count -= 1
    elif char == '(' and bracket_count == 0:
      paren_count += 1
    elif char == ')' and bracket_count == 0:
      paren_count -= 1
      continue
    if paren_count == 0:
      result += char
  return result

class PhilosophySpider(scrapy.Spider):
    name = 'philosophy_spider'
    # {path, steps to phiosophy}
    bad_http_list = [400, 404, 500]
    visited_links = []
    
    def __init__(self, *args, **kwargs): 
      super(PhilosophySpider, self).__init__(*args, **kwargs) 
      self.start_urls = [kwargs.get('start_url')] 
      
    def parse(self, response):
      self.visited_links.append(response.url)
      xpath = "//div[@class='mw-parser-output']/p"
      next_link = None
      if (response.status in self.bad_http_list):
        yield 'This link has a deadend'
        return
      html_components = response.xpath(xpath)
      for component in html_components:        
        # Remove parentheses & brackets
        clean_text = remove_parentheses(component.extract())
        soup = BeautifulSoup(clean_text, 'html.parser')
        # Remove italics
        [s.extract() for s in soup('i')]
        # Remove small text that isn't part of the main text
        [s.extract() for s in soup.find_all(attrs={"style": "font-size: small;"})]
        links = [a for a in soup.find_all('a') if not self.is_bracket_a_tag(a)]
        # Remove trailing # content
        if links:
          next_link = links[0]['href'].split('#')[0]
          break
          
      if (not next_link or next_link.startswith('http')):
          #deadend or outgoing link encountered
          print('We have reached a deadend')
          print('Unfortunatly we have reached a loop in '+str(len(self.visited_links))+' Steps')
          print('Below are the links visited \n')
          print(*self.visited_links, sep='\n')
          
      elif('https://en.wikipedia.org'+next_link in self.visited_links):
        # Return visited links if loop encountered
        self.visited_links.append('https://en.wikipedia.org' + next_link)
        print('Unfortunatly we have reached a loop in '+str(len(self.visited_links))+' Steps')
        print('Below are the links visited \n')
        print(*self.visited_links, sep='\n')
      elif(next_link=='/wiki/Philosophy'):
        self.visited_links.append('https://en.wikipedia.org' + next_link)
        print('Congrats we have reached Philosophy in '+str(len(self.visited_links))+' Steps')
        print('below are the links visited \n')
        print(*self.visited_links, sep='\n')
      else:
        #print(next_link)
        time.sleep(0.5)
        yield scrapy.Request('https://en.wikipedia.org' + str(next_link), callback=self.parse)
    def is_bracket_a_tag(self, a):
        return a.text and a.text[0] == '[' and a.text[-1] == ']'