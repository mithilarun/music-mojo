import requests
from lxml import html

def extractLyrics(htmlPage):
	page = requests.get(htmlPage)
	tree = html.fromstring(page.content)
	
	print(txt)




def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

extractLyrics('http://lyrics.wikia.com/wiki/Miranda_Lambert:Tin_Man')