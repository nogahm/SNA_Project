import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
# import community
from functools import reduce
from networkx.algorithms.community import girvan_newman
import csv

# globals
graph={}

# read csv file into graph
def csvToGraph():
    global graph
    Data=pd.read_csv('thrones-network.csv')
    graph=nx.from_pandas_edgelist(Data,source='Node A', target='Node B', edge_attr='Weight')
    graph=nx.to_undirected(graph)
    graph=nx.Graph(graph)
    # print(graph)

# remove edges with weight<6
def removeEdges():
    global graph
    remove = [edge for edge in graph.edges().items() if edge[1]['Weight'] < 6]
    remove_list=[remove[i][0] for i in range(len(remove))]
    graph.remove_edges_from(remove_list)
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
    # degree distribution
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

    intersectionTop([topTen1, topTen2, topTen3, topTen4])

# intersection between all types of centraluty
def intersectionTop(dicts):
    ld=dicts
    res = list(reduce(lambda x, y: x & y.keys(), ld))
    # print the intersection between all top10 lists
    print("The most central characters in all centrality types: ",str(res))

# find communities
def findCommunity():
    global graph
    gn_comm=girvan_newman(graph)
    for i in range(0,2):
        current=(tuple(sorted(c) for c in next(gn_comm)))
        # print("partition "+ str(i))
        # print(dict(enumerate(current)))

    comm=tuple(sorted(c) for c in next(gn_comm))
    for c in comm:
        print(c)
        subGraph=graph.subgraph(c)
        print(nx.info(subGraph))
        print("Density: ", nx.density(subGraph))
    d=dict(enumerate(comm))
    # print(d)

    inverse = dict()
    for key in d:
        # Go through the list that is saved in the dict:
        for item in d[key]:
            inverse[item] = key
    return inverse

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

def drawGraphWithCommunitiesAndCentrality(comm):
    global graph
    # size by betweenness centrality
    lower, upper = 100, 2000
    temp = ({k:  v for k, v in nx.betweenness_centrality(graph).items()}).values()
    node_size = [lower + (upper - lower) * x for x in temp]

    partition=comm
    pos = nx.spring_layout(graph)  # compute graph layout
    plt.figure(figsize=(10, 10))  # image is 10 x 10 inches
    plt.axis('off')
    plt.title("Games Of Thrones: Colored by community, Sized by betweennes centrality")
    nx.draw_networkx_nodes(graph, pos, node_size=node_size, node_color=list(partition.values()))
    nx.draw_networkx_edges(graph, pos, alpha=0.3)
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