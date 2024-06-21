import networkx as nx
import json 
import matplotlib.pyplot as plt

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

loadArticleJson('cell2.json')