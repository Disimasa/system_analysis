# from task3.task3 import task as get_relations
from io import StringIO
import csv
import math


def get_relation_matrix(connections: list, nodes_number: int) -> list:
    matrix = [[0 for _ in range(5)] for _ in range(nodes_number)]

    for connection in connections:
        node = int(connection[0])
        next_node = int(connection[1])

        matrix[node - 1][0] += 1
        matrix[next_node - 1][1] += 1
        for next_connection in connections:
            if next_connection != connections:
                if next_node == int(next_connection[0]):
                    matrix[node - 1][2] += 1
                    matrix[int(next_connection[1]) - 1][3] += 1
                elif node == int(next_connection[0]):
                    matrix[next_node - 1][4] += 1
    for row in matrix:
        if row[4] > 0:
            row[4] -= 1

    return matrix


def task(csv_string):
    f = StringIO(csv_string)
    connections = list(csv.reader(f, delimiter=','))

    nodes_number = int(max(map(max, connections)))
    relation_matrix = get_relation_matrix(connections, nodes_number)

    entropy = 0
    for row in range(nodes_number):
        for col in range(5):
            if relation_matrix[row][col] != 0:
                entropy -= (relation_matrix[row][col] / (nodes_number - 1)) * math.log(relation_matrix[row][col] /
                                                                                       (nodes_number - 1), 2)
    return round(entropy, 2)


# with open('../task3/input_connections.csv') as file:
#     csvString = file.read()
#     result = task(csvString)
#     print(result)
