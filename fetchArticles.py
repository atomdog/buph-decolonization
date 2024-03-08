from bs4 import BeautifulSoup
import requests
#https://pubmed.ncbi.nlm.nih.gov/38446676/
def getByID(articleID):
    try:
        assert type(articleID) is int
    except:
        print("Assertion Error: A integer is required but you passed a: " + str(type(articleID)))
        return(-1)
    r = requests.get("https://pubmed.ncbi.nlm.nih.gov/"+ str(articleID) + "/")
    articleContent = r.text
    articleSoup = BeautifulSoup(articleContent, 'html.parser')
    #print(articleSoup.prettify())
    divs = articleSoup.find("div", {"class": "authors-list"})
    spans = divs.find('span', attrs={'class':'authors-list-item'})
    #print(divs)
    print(len(spans))
    for span in spans:
        #print(span.string)
        #print(span.attrs['author_link'])
        if(span != None):
            print(span.attr.keys()[0]["data-ga-label"])


getByID(38446676)   