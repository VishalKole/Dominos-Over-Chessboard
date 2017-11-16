__author__ = 'Vishal Kole'
__author__ = 'Naman Kothari'
"""
Algorithms HW 6.1

Author: Vishal Kole(vvk3025@g.rit.edu)
Author: Naman Kothari(nsk2400@g.rit.edu)

This program computes to decide if it is possible to cover all of
the empty squares on the chess board by non-overlapping dominos.
"""

class Node:
    """
    The object of this class represents an instance
    of a graph node which a chess block in this problem.
    """

    __slots__ = 'neighbours', 'parent'

    def __init__(self):
        """
        This method initializes the slot variables of the node.
        """
        self.neighbours = []
        self.parent = None

    def add_neighbour(self, node):
        """
        This method adds a node to the neighbor list of a given node
        :param node: node to be added as neighbor
        :return: None
        """
        self.neighbours.append(node)

    def get_neighbours(self):
        """
        This method returns the list of neighbors of a graph node
        :return: neighbors of graph node
        """

        return self.neighbours

    def get_parent(self):
        """
        This method returns the parent node of the current node
        :return: parent node
        """
        return self.parent

    def remove_neighbour(self, node):
        """
        This method removes a node from the list of neighbour nodes
        :param node: node to be removed
        :return: None
        """
        for neighbour in self.neighbours:
            if node is neighbour:
                self.neighbours.remove(node)

def read_graph(d1, d2):
    """
    This method reads the input and returns the graph in the form of a matrix
    :param d1: rows in the board
    :param d2: columns in the board
    :return: matrix representing the board
    """
    graph = []

    for _ in range(d1):
        row = input().strip().split(' ')
        graph.append(row)

    return graph

def read_input():
    """
    This method reads the input and returns the rows, columns and graph representing the board.
    :return: rows, columns and matrix representing the board
    """
    dimensions = input().strip().split(' ')
    d1 = int(dimensions[0])
    d2 = int(dimensions[1])

    graph = read_graph(d1, d2)

    return d1, d2, graph

def generate_nodes(nodes, graph):
    """
    This method creates an instance of class Node for every empty block
    :param nodes: dictionary where {key: value} is of the form {nodeId: node}
    :param graph: matrix representing the board
    :return: number of empty blocks on the board
    """
    vacant = 0
    for i in range(len(graph)):
        row = graph[i]
        for j in range(len(row)):
            if graph[i][j] == '0':
                nodes[str(i) + ',' + str(j)] = Node()
                vacant += 1

    return vacant

def generate_neighbours(nodes, graph):
    """
    This method finds the neighbours(nodes representing adjacent empty blocks) of the current node
    :param nodes: dictionary where {key: value} is of the form {nodeId: node}
    :param graph: matrix representing the board
    :return: None
    """
    for i in range(len(graph)):
        row = graph[i]
        for j in range(len(row)):
            if graph[i][j] == '0' and (i + j) % 2 == 0:
                add_neighbours(graph, nodes, i, j)

def add_neighbours(graph, nodes, i, j):
    """

    :param nodes: dictionary where {key: value} is of the form {nodeId: node}
    :param graph: matrix representing the board
    :param i: row of node in board
    :param j: column of node in board
    :return: None
    """
    row = len(graph)
    col = len(graph[0])

    if i - 1 >= 0 and graph[i - 1][j] == '0':
        nodes[(str(i) + ',' + str(j))].add_neighbour(nodes[(str(i - 1) + ',' + str(j))])

    if i + 1 < row and graph[i + 1][j] == '0':
        nodes[(str(i) + ',' + str(j))].add_neighbour(nodes[(str(i + 1) + ',' + str(j))])

    if j - 1 >= 0 and graph[i][j - 1] == '0':
        nodes[(str(i) + ',' + str(j))].add_neighbour(nodes[(str(i) + ',' + str(j - 1))])

    if j + 1 < col and graph[i][j + 1] == '0':
        nodes[(str(i) + ',' + str(j))].add_neighbour(nodes[(str(i) + ',' + str(j + 1))])

def generate_source(graph, nodes):
    """
    This method creates a source node which has a directed edge to all
    the black empty blocks on the board.
    :param nodes: dictionary where {key: value} is of the form {nodeId: node}
    :param graph: matrix representing the board
    :return: source node
    """
    source = Node()

    for i in range(len(graph)):
        row = graph[i]
        for j in range(len(row)):
            if graph[i][j] == '0' and (i + j) % 2 == 0:
                source.add_neighbour(nodes[str(i) + ',' + str(j)])

    return source

def generate_sink(graph, nodes):
    """
    This method creates a sink node which has directed edges coming in
    from all the white vacant blocks on the board
    :param nodes: dictionary where {key: value} is of the form {nodeId: node}
    :param graph: matrix representing the board
    :return: sink node
    """

    sink = Node()

    for i in range(len(graph)):
        row = graph[i]
        for j in range(len(row)):
            if graph[i][j] == '0' and (i + j) % 2 == 1:
                nodes[str(i) + ',' + str(j)].add_neighbour(sink)

    return sink

def find_paths(source, sink):
    """
    This method finds the number of paths from source to sink following Edmunds Karp algorithm.
    :param source: source of network flow
    :param sink: sink of network flow
    :return: number of paths
    """
    path = 0
    while bfs(source, sink):
        path += 1

    return path

def bfs(source, sink):
    """
    This method finds a path from source to sink using BFS algorithm and generates back edges when the path is found.
    :param source: start node
    :param sink: finish node
    :return: True if path found, else False
    """
    visited = set()
    fringe = [source]
    source.parent = None

    while fringe:

        node = fringe.pop(0)

        if node is sink:
            while node.parent is not None:
                parent = node.parent

                node.add_neighbour(parent)
                parent.remove_neighbour(node)
                node = parent

            return True

        for neighbour in node.get_neighbours():

            if neighbour not in visited:
                visited.add(node)
                fringe.append(neighbour)
                neighbour.parent = node

    return False

def main():
    """
    This is the main method. It reads input and computes to decide if it is possible to cover all of
    the empty squares on the chess board by non-overlapping dominos
    :return: None
    """

    d1, d2, graph = read_input()

    nodes = {}

    vacant = generate_nodes(nodes, graph)

    if vacant % 2 == 1:
        print('NO')

    else:
        generate_neighbours(nodes, graph)

        source = generate_source(graph, nodes)
        sink = generate_sink(graph, nodes)

        path = find_paths(source, sink)

        if vacant == path * 2:
            print('YES')
        else:
            print('NO')

if __name__ == '__main__':
    main()
