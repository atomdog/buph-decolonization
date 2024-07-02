import networkx as nx
import json 
import matplotlib.pyplot as plt
import spacy
from geopy.geocoders import Nominatim

def loadArticleJson(filetitle):
    G = nx.Graph()
    f = open(filetitle)
    data = json.load(f)
    # Iterating through the json
    # list
    i_index = 0
    color_map = []
    labeldict = {}

    for i in data:
        articleCooperation = []
        for authorship in i['authorship']:
            rv = ''
            if(authorship['affiliationTitle'] is not None):
                if('Electronic address' in authorship['affiliationTitle']):
                    afterEmail = authorship['affiliationTitle'].split('Electronic address')[1]
                    rv = afterEmail
                else:
                    rv = authorship['affiliationTitle']
            rv = rv.split(";")[0]
            articleCooperation.append(rv)
            if( not G.has_node(rv)):
                G.add_node(rv)
                labeldict[rv] = rv
                if(i['journalTitle'] == "Cell"):
                    color_map.append('green')
                elif(i['journalTitle'] == "Lancet"):
                    color_map.append('red')
                else:
                    color_map.append('blue')

            
        for n in articleCooperation:
            for n2 in articleCooperation:
                if(n!=n2):
                    G.add_edge(n, n2)
                    print(n + " <-----> " + n2)
        

        #print(articleCooperation)

    #print(G.edges())

    averageconnectedness = 0
    for i in G.nodes():
        print(len(G.edges(i)))
        averageconnectedness += len(G.edges(i))
    averageconnectedness = averageconnectedness/ len(G.nodes())

    fig, axe = plt.subplots(figsize=(28,18))
    axe.set_title('Authorship Colab. Network (By Email Domain) - Average # of edges: '+str(averageconnectedness), loc='right')


    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_color=color_map, node_size=2, labels=labeldict, with_labels=False)
    nx.draw_networkx_labels(G, pos, font_size=5, font_color='k', font_family='sans-serif')
    plt.show()
    plt.savefig("jun21_authorship")


def merge_location_entities(spacypipe, doct):
    doc = spacypipe(doct)
    new_ents = []
    skip_next = False

    for i, ent in enumerate(doc.ents):
        if skip_next:
            skip_next = False
            continue

        # If current entity is a location and next entity is also a location, merge them
        if ent.label_ in {"GPE", "LOC"}:
            if i + 1 < len(doc.ents):
                next_ent = doc.ents[i + 1]
                if next_ent.label_ in {"GPE", "LOC"}:
                    # Create a merged span from the start of the first entity to the end of the second
                    start = ent.start_char
                    end = next_ent.end_char
                    merged_span = doc.char_span(start, end, label="GPE")
                    
                    # Check if the merged span is valid
                    if merged_span:
                        new_ents.append(merged_span)
                        skip_next = True
                    else:
                        new_ents.append(ent)
                else:
                    new_ents.append(ent)
            else:
                new_ents.append(ent)
        else:
            new_ents.append(ent)
    # Replace the old entities with the new merged entities
    if(new_ents is not None):
        doc.ents = new_ents

    return doc



def extract_authorship_location(filetitle):
    G = nx.Graph()
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('merge_noun_chunks')
    nlp.add_pipe("merge_entities")
    
#ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents":True})


    f = open(filetitle)
    data = json.load(f)
    # Iterating through the json
    # list
    i_index = 0
    color_map = []
    labeldict = {}
    geolocator = Nominatim(user_agent="myApp")


    for i in data:
        articleCooperation = []
        for authorship in i['authorship']:
            rv = ''
            gpe = []
            loc = []
            latlong = []
            #if this isn't a none
            if(authorship['affiliationTitle'] is not None):
                if(";" in authorship['affiliationTitle']):
                    splitaffil = authorship['affiliationTitle'].split(";")
                    for i in splitaffil:
                        doc = merge_location_entities(nlp, i)
                        ltlg = []
                        gpe2 = []
                        loc2 = []
                        for entity in doc.ents:
                            #print(doc)
                            if (entity.label_ == 'GPE'):
                                gpe2.append(entity.text)
                                ltlg.append(geolocator.geocode(entity.text))
                            elif (entity.label_ == 'LOC'):
                                loc2.append(entity.text)
                        gpe.append(gpe2)
                        loc.append(loc2)
                        latlong.append(ltlg)
                else:
                    doc = merge_location_entities(nlp, authorship['affiliationTitle'])
                    
                    gpe2 = []
                    loc2 = []
                    ltlg = []
                    for entity in doc.ents:
                        #print(doc)
                        if (entity.label_ == 'GPE'):
                            gpe2.append(entity.text)
                            ltlg.append(geolocator.geocode(entity.text))
                        elif (entity.label_ == 'ORG'):
                            loc2.append(entity.text)
                    gpe.append(gpe2)
                    loc.append(loc2)
                    latlong.append(ltlg)

                node_author_name = authorship['authorName']
                for location in ltlg:
                    if(not G.has_node(authorship['authorName'])):
                        if(location is not None):
                            G.add_node(node_author_name, lat=location.latitude, long=location.longitude)
                            labeldict[node_author_name] = node_author_name
                            articleCooperation.append(node_author_name)
            

            else:
                pass
            for n in articleCooperation:
                for n2 in articleCooperation:
                    if(n!=n2):
                        G.add_edge(n, n2)
                        print(n + " <-----> " + n2)
            #print(gpe)
            print(latlong)

    averageconnectedness = 0
    for i in G.nodes():
        print(len(G.edges(i)))
        averageconnectedness += len(G.edges(i))
    averageconnectedness = averageconnectedness/ len(G.nodes())

    fig, axe = plt.subplots(figsize=(28,18))
    axe.set_title('Authorship Colab. Network (Entity Extraction) - Average # of edges: '+str(averageconnectedness), loc='right')


    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_color=color_map, node_size=2, labels=labeldict, with_labels=False)
    nx.draw_networkx_labels(G, pos, font_size=5, font_color='k', font_family='sans-serif')
    plt.show()
    plt.savefig("july2_authorship")
    return(G)
                #print(loc)
                

                
#G = extract_authorship_location('cell3.json')
#createFoliumMap(G)
#loadArticleJson('cell2.json')
import pickle
#pickle.dump(G, open('g.pickle', 'wb'))
import folium
# load graph object from file
G = pickle.load(open('g.pickle', 'rb'))

def createFoliumMap(G):
    m = folium.Map(location=[41.9, -97.3], zoom_start=4)
    for n,d in G.nodes(data=True):
        for destnode in  G.edges(n, data=True):
            #print(G[n]['lat'])

            print(G.nodes.data()[None:1:None])

            locations = [(d['lat'], d['long']),(de.lat,de.long)]
            
            folium.PolyLine(locations,
                            color='red',
                            weight=15,
                            opacity=0.8).add_to(m)

    m.save("connectionsgeo.html")

createFoliumMap(G)
