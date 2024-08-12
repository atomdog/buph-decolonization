import sqlite3
import networkx as nx
import json
import storage

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

# Export graph data to GeoJSON by journal
def export_graph_to_geojson_by_journal(G, metrics):
    journal_features = {}

    # Nodes (Departments)
    for node_id, data in G.nodes(data=True):
        node_metrics = {
            "degree_centrality": metrics["Degree centrality"].get(node_id),
            "betweenness_centrality": metrics["Betweenness centrality"].get(node_id),
            "closeness_centrality": metrics["Closeness centrality"].get(node_id),
            "eigenvector_centrality": metrics["Eigenvector centrality"].get(node_id),
        }
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [data["lon"], data["lat"]]
            },
            "properties": {
                "id": node_id,
                "name": data["name"],
                **node_metrics
            }
        }

        # Determine the journals for this node
        for neighbor in G.neighbors(node_id):
            for article_id, journal_title in G[node_id].get('articles', []):
                if journal_title not in journal_features:
                    journal_features[journal_title] = {"nodes": [], "edges": []}
                journal_features[journal_title]["nodes"].append(feature)

    # Edges
    for source, target, data in G.edges(data=True):
        dept1 = G.nodes[source]
        dept2 = G.nodes[target]
        edge_feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [dept1["lon"], dept1["lat"]],
                    [dept2["lon"], dept2["lat"]]
                ]
            },
            "properties": {
                "source": source,
                "target": target,
                "weight": data["weight"],
                "articles": data["articles"]
            }
        }
        for article_id, journal_title in data['articles']:
            if journal_title not in journal_features:
                journal_features[journal_title] = {"nodes": [], "edges": []}
            journal_features[journal_title]["edges"].append(edge_feature)

    for journal_title, features in journal_features.items():
        graph_data = {
            "type": "FeatureCollection",
            "features": features["nodes"] + features["edges"]
        }

        file_name = f"graph_data_{journal_title.replace(' ', '_')}.geojson"
        with open(file_name, "w") as f:
            json.dump(graph_data, f, indent=4)

# Main execution
departments = storage.retrieve_all_departments()
article_dept_links = storage.get_article_department_links()
G = create_graph(departments, article_dept_links)
metrics = calculate_graph_metrics(G)
export_graph_to_geojson_by_journal(G, metrics)
