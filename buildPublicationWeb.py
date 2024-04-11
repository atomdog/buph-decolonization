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
    for i in data:
        articleCooperation = []
        for authorship in i['authorship']:
            rv = ''
            if(authorship['affiliationTitle'] is not None):
                if('Electronic address' in authorship['affiliationTitle']):
                    beforeEmail = authorship['affiliationTitle'].split('Electronic address')[0]
                    rv = beforeEmail
                else:
                    rv = authorship['affiliationTitle']
            rv = rv.split(";")[0]
            articleCooperation.append(rv)
            if( not G.has_node(rv)):
                G.add_node(rv)
            
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
    fig, axe = plt.subplots(figsize=(24,14))
    axe.set_title('Affil. Colab Network- Average # of edges: '+str(averageconnectedness), loc='right')

    pos = nx.kamada_kawai_layout(G)
    nx.draw(G, pos, node_size=1)
    #nx.draw_networkx_labels(G, pos, font_size=5, font_color='k', font_family='sans-serif')
    plt.show()

loadArticleJson('cell.json')