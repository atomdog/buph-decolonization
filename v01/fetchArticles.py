from bs4 import BeautifulSoup
import requests
from geopy.geocoders import Nominatim
import json 

MAPBOXTOKEN = open("mapbox.txt", "r").read().strip()
#given an article ID number, we request and parse the page. we return a json containing our data.
def getByArticleID(article_id):
    url = f'https://pubmed.ncbi.nlm.nih.gov/{article_id}/?format=pubmed'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lines = soup.get_text().splitlines()
    article_info = {
        "articleTitle": None,
        "journalTitle": None,
        "datePublished": None,
        "abstract": None,
        "authorsList": [],
        "departmentList": []
    }

    flags = {"titleActive": False, "abstractActive": False, "departmentActive": False}
    for line in lines:
        if line.startswith("DP"):
            article_info["datePublished"] = line[2:].replace("-", "").strip()
        if line.startswith("TI"):
            article_info["articleTitle"] = line[2:].replace("-", "").strip()
            flags["titleActive"] = True
        elif flags["titleActive"]:
            if line.startswith("PG"):
                flags["titleActive"] = False
            else:
                article_info["articleTitle"] += " " + line.strip()
        if line.startswith("JT"):
            article_info["journalTitle"] = line[2:].replace("-", "").strip()
        if line.startswith("AB"):
            article_info["abstract"] = line[2:].replace("-", "").strip()
            flags["abstractActive"] = True
        elif flags["abstractActive"]:
            if line.startswith("CI"):
                flags["abstractActive"] = False
            else:
                article_info["abstract"] += " " + line.replace('\\', "").strip()
        if line.startswith("FAU"):
            article_info["authorsList"].append(line[3:].replace("-", "").strip())
        if line.startswith("AD"):
            article_info["departmentList"].append(line[2:].replace("-", "").strip())
            flags["departmentActive"] = True
        elif flags["departmentActive"]:
            if line.startswith("FAU") or line.startswith("LA"):
                flags["departmentActive"] = False
            else:
                article_info["departmentList"][-1] += " " + line.strip()
    try:
        assert len(article_info["authorsList"]) == len(article_info["departmentList"])
    except Exception as e:
        print(len(article_info["authorsList"]))
        print(len(article_info["departmentList"]))
        print(article_info["authorsList"])
        print(article_info['departmentList'])
        print(url)
    return article_info

#this takes two arguments: the constructed query for the journal and the page number of the results we want to return.
def getByJournal(journal_query, pagenum):
    if not isinstance(journal_query, str):
        print(f"Assertion Error: A string is required but you passed a: {type(journal_query).__name__}")
        return None
    article_id_list = []
    base_url = "https://pubmed.ncbi.nlm.nih.gov/"
    
    response = requests.get(f"{base_url}{journal_query}&page={pagenum}")
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', class_='docsum-title')
    for link in links:
        article_id_list.append(link['href'])
    return article_id_list

#this takes the string containing the institution and geolocates it, returning a pair of coordinates (latitude, longitude)
def mapboxGeolocate(fuzzloc):
    #print(">> Accessing Mapbox API: " + fuzzloc)
    location =[]
    url = "https://api.mapbox.com/search/geocode/v6/forward?q="+fuzzloc+"&access_token="+MAPBOXTOKEN
    data = requests.get(url).text
    
    data = json.loads(data)
    if data['features']:
        # Extract the coordinates
        coordinates = data['features'][0]['geometry']['coordinates']
        location = [coordinates[1], coordinates[0]]
    
    #print(">> Mapbox Query Resulted in: " +str(location))

    return(location)

#this cleans and extracts department locations.
def CleanExtractDepartmentLocation(departmentstring):
    latlong = None
    #print("> Cleaning and Extracting Department Location: ")
    if("Electronic address:" in departmentstring):
        departmentstring = departmentstring.split("Electronic address:")[0]
    if(";" in departmentstring):
        departmentstring = departmentstring.split(";")[0]
    try:
        latlong = mapboxGeolocate(departmentstring)

    except Exception as e:
        print(e)
    return([departmentstring, latlong])


# Example usage:
articlesForJournal_cell = (getByJournal('?term="Cell"%5Bjour%5D&sort=date&sort_order=desc', 1))
articleStore = []
for i in range(0, len(articlesForJournal_cell)):
    print(str(i) + " of "+ str(len(articlesForJournal_cell)))
    articleStore.append()

#given a journal query, we 
# 1. get the ID of every article on the first page of results (most recent)
# 2. get the 
def aggregate_by_journalquery(querystr):
    articlesForJournal= (getByJournal(querystr, 1))
    for i in range(0, len(articlesForJournal)):
        #using the article ID, get and parse data
        current_item = getByArticleID(int(articlesForJournal[i].replace("/","")))
    
        articleItems = current_item[i]['articleTitle']
        #these two variables keep track of our author and department insertion IDs so we can tie them to the article
        authorIDList = []
        departmentIDList = []

        #insert the article into the database, this returns the article ID
        #store the current working article ID in the variable article_id
        #this is necessary for later to match our author
        article_id = insert_article(current_item['articleTitle'], 
                                current_item['journalTitle'],
                                current_item['datePublished'],
                                current_item['abstract'])

        #for every author in the author list, insert the author
        #store the ID
        for author in current_item['authorList']:
            authorID = insert_author(author)
            authorIDList.append(authorID)
        #for every department in the department list, insert the department
        #store the ID
        for department in current_item['departmentList']
            extracted = CleanExtractDepartmentLocation(department)
            departmentID = insert_department(extracted[0], extracted[1][0], extracted[1][1])
            departmentIDList.append(departmentID)
        
        #now the identifiers for the authors and departments must be tied to the current article.
        #we will make use of the  author, article, department database
        assert len(departmentIDList) == len(authorIDList)
        for i in range(0, len(departmentIDList)):
            currenttie = tie_article_author_department(article_id, author_id, department_id)
            
    

    #print(CleanExtractDepartmentLocation(i))
aggregate_by_journalquery(querystr='?term="Cell"%5Bjour%5D&sort=date&sort_order=desc')