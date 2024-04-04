from bs4 import BeautifulSoup
import requests
import pmNodes

#https://pubmed.ncbi.nlm.nih.gov/38446676/
def getByArticleID(articleID):
    try:
        assert type(articleID) is int
    except:
        print("Assertion Error: An integer is required but you passed a: " + str(type(articleID)))
        return(-1)
    r = requests.get("https://pubmed.ncbi.nlm.nih.gov/"+ str(articleID) + "/")
    articleContent = r.text
    articleSoup = BeautifulSoup(articleContent, 'html.parser')
    #print(articleSoup.prettify())
    divs = articleSoup.find("div", {"class": "authors-list"})
    spans = divs.find_all('span', attrs={'class':'authors-list-item'})
    #print(divs)
    #print(len(spans))
    #print(spans)
    for span in spans:
        #print(span)
        #spanSoup = BeautifulSoup(span)
        for each_author in span.find_all('a', attrs={'class':'full-name'}):
            authorName = each_author['data-ga-label']
            authorLink = each_author['href']
            #authorID = authorLink.split("&")[1].replace("cauthor_id=", "")
            #print(authorID)
        for each_Aff in span.find_all('a', attrs={'class':'affiliation-link'}):
            AffTitle = each_Aff['title']
            fullViewAffLink = "https://pubmed.ncbi.nlm.nih.gov/"+ str(articleID) + "/" + each_Aff['href']
        
        #print(span.string)data
        #print(span.attrs['author_link'])
        #if(span != None and span.attr != None):
            #print(span.attr.keys()[0]["data-ga-label"])



getByArticleID(38447573)   

def getByAuthorID(authorID):
    try:
        assert type(authorID) is int
    except:
        print("Assertion Error: An integer is required but you passed a: " + str(type(authorID)))
        return(-1)
    r = requests.get("https://pubmed.ncbi.nlm.nih.gov/"+str(authorID) + "/")
    