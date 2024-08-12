import sqlite3
import networkx as nx
import folium
from haversine import haversine
import storage
from folium.plugins import MarkerCluster

# Create NetworkX graph from department data and shared articles
def create_graph(departments, article_dept_links):
    G = nx.Graph()
    
    # Add departments as nodes
    for dept in departments:
        dept_id, name, lat, lon = dept
        G.add_node(dept_id, name=name, lat=lat, lon=lon)
    
    # Add edges based on shared articles
    for link in article_dept_links:
        dept1_id, dept2_id, article_id, journal_title = link
        if G.has_edge(dept1_id, dept2_id):
            G[dept1_id][dept2_id]['weight'] += 1
            G[dept1_id][dept2_id]['articles'].append((article_id, journal_title))
        else:
            G.add_edge(dept1_id, dept2_id, weight=1, articles=[(article_id, journal_title)])
    
    return G

# Calculate graph metrics
def calculate_graph_metrics(G):
    cliques = list(nx.find_cliques(G))
    connectivity = nx.node_connectivity(G)
    avg_clustering = nx.average_clustering(G, weight='weight')
    density = nx.density(G)
    assortativity = nx.degree_assortativity_coefficient(G, weight='weight')
    transitivity = nx.transitivity(G)
    
    # Calculate per-node metrics
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G, weight='weight', normalized=True)
    closeness_centrality = nx.closeness_centrality(G)
    
    try:
        eigenvector_centrality = nx.eigenvector_centrality(G, weight='weight', max_iter=500)
    except nx.exception.PowerIterationFailedConvergence:
        eigenvector_centrality = {node: None for node in G.nodes()}
    
    metrics = {
        "Number of cliques": len(cliques),
        "Network connectivity": connectivity,
        "Average clustering coefficient": avg_clustering,
        "Graph density": density,
        "Assortativity coefficient": assortativity,
        "Transitivity": transitivity,
        "Degree centrality": degree_centrality,
        "Betweenness centrality": betweenness_centrality,
        "Closeness centrality": closeness_centrality,
        "Eigenvector centrality": eigenvector_centrality,
        "Cliques": cliques
    }
    
    return metrics

# Create Folium map with department connections and metrics
def create_map(G, metrics):
    # Create base map with clustering
    m = folium.Map(location=[0, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add nodes to map with metrics
    for node in G.nodes(data=True):
        node_id = node[0]
        node_data = node[1]
        name = node_data['name']
        lat = node_data['lat']
        lon = node_data['lon']
        degree = metrics['Degree centrality'][node_id]
        betweenness = metrics['Betweenness centrality'][node_id]
        closeness = metrics['Closeness centrality'][node_id]
        eigenvector = metrics['Eigenvector centrality'][node_id]
        
        popup_text = (f"Department: {name}<br>"
                      f"Degree Centrality: {degree:.4f}<br>"
                      f"Betweenness Centrality: {betweenness:.4f}<br>"
                      f"Closeness Centrality: {closeness:.4f}<br>"
                      f"Eigenvector Centrality: {eigenvector if eigenvector is not None else 'N/A'}")
        
        folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            icon=folium.Icon(color='blue')
        ).add_to(marker_cluster)
    
    # Add edges to map and create journal layers
    journal_layers = {}
    for edge in G.edges(data=True):
        dept1 = G.nodes[edge[0]]
        dept2 = G.nodes[edge[1]]
        points = [(dept1['lat'], dept1['lon']), (dept2['lat'], dept2['lon'])]
        for article_id, journal_title in edge[2]['articles']:
            if journal_title not in journal_layers:
                journal_layers[journal_title] = folium.FeatureGroup(name=journal_title)
            folium.PolyLine(points, color='green', weight=edge[2]['weight']).add_to(journal_layers[journal_title])
    
    for journal_title, layer in journal_layers.items():
        m.add_child(layer)
    
    # Add cliques as separate layers
    for i, clique in enumerate(metrics["Cliques"]):
        clique_layer = folium.FeatureGroup(name=f'Clique {i+1}')
        for node_id in clique:
            node_data = G.nodes[node_id]
            folium.Marker(
                location=[node_data['lat'], node_data['lon']],
                popup=f'Clique {i+1}: {node_data["name"]}',
                icon=folium.Icon(color='orange')
            ).add_to(clique_layer)
        m.add_child(clique_layer)
    
    folium.LayerControl().add_to(m)

    # Add overall graph metrics to map as a separate layer
    metrics_popup = folium.Popup(
        f"Graph Metrics:<br>"
        f"Number of cliques: {metrics['Number of cliques']}<br>"
        f"Network connectivity: {metrics['Network connectivity']}<br>"
        f"Average clustering coefficient: {metrics['Average clustering coefficient']:.4f}<br>"
        f"Graph density: {metrics['Graph density']:.4f}<br>"
        f"Assortativity coefficient: {metrics['Assortativity coefficient']:.4f}<br>"
        f"Transitivity: {metrics['Transitivity']:.4f}",
        max_width=300
    )
    folium.Marker(
        location=[0, 0],
        popup=metrics_popup,
        icon=folium.Icon(color='red')
    ).add_to(m)
    
    return m

# Main execution
departments = storage.retrieve_all_departments()
article_dept_links = storage.get_article_department_links()
print(article_dept_links)
G = create_graph(departments, article_dept_links)
metrics = calculate_graph_metrics(G)
map_ = create_map(G, metrics)

# Save map to HTML file
map_.save("department_network_map.html")

# If you want to display the map directly in a Jupyter Notebook, you can use:
# from IPython.display import IFrame
# IFrame('department_network_map.html', width=800, height=600)
