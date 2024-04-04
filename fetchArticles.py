from bs4 import BeautifulSoup
import requests
import pmNodes


# get article by 8-digit pubmed ID
# ID appears in URL: https://pubmed.ncbi.nlm.nih.gov/<**ID**>/
def getByArticleID(articleID):
    #ensure type is appropriate
    try:
        assert type(articleID) is int
    except:
        print("Assertion Error: An integer is required but you passed a: " + str(type(articleID)))
        return(-1)

    
    #make request
    r = requests.get("https://pubmed.ncbi.nlm.nih.gov/"+ str(articleID) + "/")
    articleContent = r.text
    articleSoup = BeautifulSoup(articleContent, 'html.parser')

    #create list to store authorship records for article 
    authorships = []

    #fetch authors list div
    divs = articleSoup.find("div", {"class": "authors-list"})
    #fetch the items of the authors list
    spans = divs.find_all('span', attrs={'class':'authors-list-item'})


    for span in spans:
        #initialize variables to None 
        authorName = None
        authorLink = None
        AffTitle = None
        fullViewAffLink = None
        #for each author, get full name and link to search for authored articles
        for each_author in span.find_all('a', attrs={'class':'full-name'}):
            authorName = each_author['data-ga-label']
            authorLink = each_author['href']

        #for each affiliation, get the title and link to search for other published articles
        for each_Aff in span.find_all('a', attrs={'class':'affiliation-link'}):
            AffTitle = each_Aff['title']
            fullViewAffLink = "https://pubmed.ncbi.nlm.nih.gov/"+ str(articleID) + "/" + each_Aff['href']

        authorship = {"authorName": authorName, "authorLink": authorLink, "affiliationTitle": AffTitle, "affiliationLink": fullViewAffLink}
        #store in list of article authorships
        authorships.append(authorship)

    #list to store all grants
    articleGrants = []
    area_of_focus = articleSoup.find('div', {'class' : 'grants-list'})
    grantlinklist = []
    try:
        grantlinklist = area_of_focus.findAll('li')
    except:
        pass
    
    for grant in grantlinklist:
        #get all links per item in grant list
        for each_grant in grant.find_all('a'):
            #extract grant name and link to all articles funded by said grant
            grant_title = each_grant['title'].replace("All articles for grant ", "")
            grant_link = each_grant['href']
            articleGrants.append({"grantTitle":grant_title, "grantLink": grant_link})
    
    #retrieve article title
    titleDiv = articleSoup.find("header", {"class": "heading"}).find("h1", {'class': "heading-title"})
    articleTitle = titleDiv.getText().rstrip().lstrip()

    #retrieve journal title and journal link
    citDiv = articleSoup.find("header", {"class": "heading"}).find('div', {'class' : 'article-source'}).find("div", {'class': "content"}).find('a', {'class': "search-in-pubmed-link dropdown-block-link"})
    journalTitle = citDiv['data-ga-label']
    journalLink = citDiv['href']

    citDiv2 = articleSoup.find("header", {"class": "heading"}).find('div', {'class' : 'article-source'}).find("span", {'class': "cit"})
    citDiv3 = articleSoup.find("header", {"class": "heading"}).find('div', {'class' : 'article-citation'}).find("span", {'class': "citation-doi"})
    citDiv4 = articleSoup.find("header", {"class": "heading"}).find('div', {'class' : 'article-citation'}).find("span", {'class': "secondary-date"})

    cD_0 = citDiv2.getText()
    doi = citDiv3.getText().rstrip().lstrip()
    if(citDiv4!=None):
        secondaryDate = citDiv4.getText().rstrip().lstrip()
    else:
        secondaryDate = None


    abstract = articleSoup.find("div", {"class": "abstract"}).getText().rstrip().lstrip().replace('\n', '').replace('"', '#QUOTE#').replace("'", '#QUOTE#')

    articleObject = {'authorship': authorships, 
                    'articleTitle': articleTitle, 
                    'journalTitle': journalTitle, 
                    'journalLink': journalLink,
                    'cit': cD_0,
                    'doi': doi,
                    'secondaryDate': secondaryDate, 
                    'grants': articleGrants,
                    'abstract': abstract}
    return(articleObject)







print(getByArticleID(38565142))

def getByAuthorID(authorID):
    try:
        assert type(authorID) is int
    except:
        print("Assertion Error: An integer is required but you passed a: " + str(type(authorID)))
        return(-1)
    r = requests.get("https://pubmed.ncbi.nlm.nih.gov/"+str(authorID) + "/")
        