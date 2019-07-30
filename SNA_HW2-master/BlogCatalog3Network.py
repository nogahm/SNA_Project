import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from functools import reduce
from networkx.algorithms import community
from networkx.algorithms.community.centrality import girvan_newman
import csv


# globals
graph={}

# read csv file into graph object
def csvToGraph():
    global graph
    Data=pd.read_csv('BlogCatalog3\\edges.csv', header=None, names=["A", "B"])
    graph=nx.from_pandas_edgelist(Data, source="A", target="B")
    graph=nx.Graph(graph)
    print(graph)

# remove nodes with less than 250 neighbors
def removeEdges():
    global graph
    # get nodes to remove
    remove = [node for node in graph.nodes() if len(list(graph.neighbors(node))) < 250]
    graph.remove_nodes_from(remove)
    # remove nodes with no edge
    graph.remove_nodes_from(list(nx.isolates(graph)))

# print graph's parameters
def printGraphParams():
    print(nx.info(graph))
    # print average clustering coefficient
    print('average clustring coefficient is:', nx.average_clustering(graph))
    # print density
    print('density is: ', nx.density(graph))
    # print diameter
    print('diameter is: ', nx.diameter(graph))
    # degree distribution histogram
    degrees=[graph.degree(n) for n in graph.nodes()]
    plt.hist(degrees)
    plt.title("Degree Distribution Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    plt.show()
    # average path length
    print('average path length is: ', nx.average_shortest_path_length(graph))

# print DF for each kind of centrality
def printTopTenByCenterality():
    global graph
    topTenDF=[]
    # degree centerality
    result=nx.degree_centrality(graph)
    topTen1 = dict(sorted(result.items(), key=lambda t: t[1], reverse=True)[:10])
    print('degree centrality top ten:')
    df=pd.DataFrame.from_dict(topTen1, orient='index')
    df.columns=['Centrality']
    print(df)
    # eigenvector centrality
    result=nx.eigenvector_centrality(graph)
    topTen2 = dict(sorted(result.items(), key=lambda t: t[1], reverse=True)[:10])
    print('eigenvector centrality top ten:')
    df=pd.DataFrame.from_dict(topTen2, orient='index')
    df.columns=['Centrality']
    print(df)
    # betweenness centrality
    result = nx.betweenness_centrality(graph)
    topTen3 = dict(sorted(result.items(), key=lambda t: t[1], reverse=True)[:10])
    print('betweenness centrality top ten:')
    df=pd.DataFrame.from_dict(topTen3, orient='index')
    df.columns=['Centrality']
    print(df)
    # closeness centrality
    result = nx.closeness_centrality(graph)
    topTen4 = dict(sorted(result.items(), key=lambda t: t[1], reverse=True)[:10])
    print('closeness centrality top ten:')
    df=pd.DataFrame.from_dict(topTen4, orient='index')
    df.columns=['Centrality']
    print(df)

    intersectionTop([topTen1,topTen3, topTen2, topTen4])

# intersection between all types of centraluty
def intersectionTop(dicts):
    ld=dicts
    res = list(reduce(lambda x, y: x & y.keys(), ld))
    # print the intersection between all top10 lists
    print("The most central blogers in all centrality types: ",str(res))

# find communities
def findCommunity():
    global graph
    import community
    comm = community.best_partition(graph)
    return comm



# top 10 predictions to link - jaccard
def linkPredictionJaccard():
    global graph
    preds_jc = nx.jaccard_coefficient(graph)
    pred_jc_dict = {}
    for u, v, p in preds_jc:
        pred_jc_dict[(u, v)] = p
    print(sorted(pred_jc_dict.items(), key=lambda x: x[1], reverse=True)[:10])

# top 10 predictions to link - adamic
def linkPredictionAdamic():
    global graph
    preds_aa = nx.adamic_adar_index(graph)
    pred_aa_dict = {}
    for u, v, p in preds_aa:
        pred_aa_dict[(u, v)] = p
    print(sorted(pred_aa_dict.items(), key=lambda x: x[1], reverse=True)[:10])

# Draw network graph
def drawGraphWithCommunitiesAndCentrality(comm):
    global graph
    # size by degree centrality
    lower, upper = 10, 1000
    temp = ({k:  v for k, v in nx.degree_centrality(graph).items()}).values()
    node_size = [lower + (upper - lower) * x for x in temp]

    # remove edges of nodes with less than 250 neighbors
    tempGraph=graph.copy()
    remove = [node for node in tempGraph.nodes() if len(list(tempGraph.neighbors(node))) < 250]
    tempGraph.remove_nodes_from(remove)
    # remove nodes with no edge
    tempGraph.remove_nodes_from(list(nx.isolates(tempGraph)))

    partition=comm
    pos = nx.random_layout(graph)  # compute graph layout
    plt.figure(figsize=(10, 10))  # image is 10 x 10 inches
    plt.axis('off')
    plt.title("Bloggers Network: Colored by community, Sized by degree centrality")
    nx.draw_networkx_nodes(graph, pos, node_size=node_size, node_color=list(partition.values()))
    nx.draw_networkx_edges(tempGraph, pos, alpha=0.3)
    nx.draw_networkx_labels(graph,pos, font_size =8, font_color ='grey')
    plt.show(graph)

# main
def main():
    csvToGraph()
    removeEdges()
    printGraphParams()
    printTopTenByCenterality()
    comm=findCommunity()
    linkPredictionAdamic()
    linkPredictionJaccard()
    drawGraphWithCommunitiesAndCentrality(comm)

main()