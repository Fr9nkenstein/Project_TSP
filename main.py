import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def Prim(Edges, n=30):
    init = np.random.randint(0, n)  # Randomly select a node to start with
    unvisited = list(range(n))  # List of nodes not included in the tree
    unvisited.remove(init)  # Remove the initial node from the list of unvisited nodes
    visited = [init]  # List of nodes included in the tree
    tree = []  # List of edges included in the tree
    cost = 0  # Cost of the tree

    for _ in range(n - 1):
        # Find the edge with the minimum cost from the current tree to another node not included in the tree
        min_cost = np.inf
        for node1 in visited:
            for node2 in unvisited:
                if Edges[node1, node2] < min_cost:
                    min_cost = Edges[node1, node2]
                    min_node1 = node1
                    min_node2 = node2
        # Add the node to the tree
        visited.append(min_node2)
        unvisited.remove(min_node2)
        tree.append((min_node1, min_node2))
        cost += min_cost

    return tree, cost


def Christofides(n, random_seed=42):
    np.random.seed(random_seed)
    X = np.random.uniform(-10, 10, (n,))
    Y = np.random.uniform(-10, 10, (n,))
    Nodes = [(x, y) for x, y in zip(X, Y)]

    Edges = []

    for node1 in Nodes:
        edge = []
        for node2 in Nodes:
            if node1 == node2:
                edge.append(np.inf)
            else:
                edge.append(np.sqrt((node1[0] - node2[0]) ** 2.0 + (node1[1] - node2[1]) ** 2.0))
        Edges.append(edge)

    Edges = np.array(Edges)

    # Find the minimum spanning tree of the graph
    tree, cost_MST = Prim(Edges,n)
    Tree = nx.MultiGraph()
    for i in range(n):
        Tree.add_node(i, pos=Nodes[i])

    for edge in tree:
        Tree.add_edge(edge[0], edge[1], weight=Edges[edge[0], edge[1]])

    # Find the set of nodes with odd degree in the MST
    odd_nodes = []
    for node in range(n):
        degree = 0
        for edge in tree:
            if node in edge:
                degree += 1
        if degree % 2 == 1:
            odd_nodes.append(node)

    odd_tree = nx.Graph()
    for odd_node in odd_nodes:
        odd_tree.add_node(odd_node, pos=Nodes[odd_node])

    for odd_node1 in odd_nodes:
        for odd_node2 in odd_nodes:
            if odd_node1 != odd_node2:
                odd_tree.add_edge(odd_node1, odd_node2, weight=Edges[odd_node1, odd_node2])

    # Find the perfect matching for the odd nodes
    odd_matching = nx.algorithms.min_weight_matching(odd_tree)

    # Add the edges of the matching to the MST to make all the nodes have even degree


    for edge in odd_matching:
        Tree.add_edge(edge[0], edge[1], weight=Edges[edge[0], edge[1]])


    # Find an Eulerian tour of the graph
    Eulerian_tour = list(nx.eulerian_circuit(Tree))

    # Make the Eulerian tour a Hamiltonian tour by skipping the repeated nodes
    Hamiltonian_tour = []
    for edge in Eulerian_tour:
        if edge[0] not in Hamiltonian_tour:
            Hamiltonian_tour.append(edge[0])
        if edge[1] not in Hamiltonian_tour:
            Hamiltonian_tour.append(edge[1])

    Hamiltonian_tour.append(Hamiltonian_tour[0])
    cost_Christofides = 0
    for i in range(n):
        cost_Christofides += Edges[Hamiltonian_tour[i], Hamiltonian_tour[i + 1]]

    return cost_MST, cost_Christofides


print(Christofides(80, random_seed=114514))
