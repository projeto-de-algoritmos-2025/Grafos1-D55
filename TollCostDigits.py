#!/bin/python3

import sys
import itertools as it

num_nodes, num_edges = input().strip().split(' ')
num_nodes, num_edges = [int(num_nodes), int(num_edges)]
conns = []
for edge_index in range(num_edges):
    node_x, node_y, toll = input().strip().split(' ')
    node_x, node_y, toll = [int(node_x), int(node_y), int(toll)]
    # Converte para índices baseados em 0 e usa apenas o dígito do pedágio
    conns.append([node_x-1, node_y-1, toll%10])
total_nodes = num_nodes
total_conns = num_edges

# Constrói grafo bidirecional com custos invertidos para calcular diferenças
graph_paths = {node:[] for node in range(total_nodes)}
for conn in conns:
    graph_paths[conn[0]].append((conn[1], conn[2]))
    # Aresta reversa com custo invertido permite calcular (A-B) e (B-A)
    graph_paths[conn[1]].append((conn[0], (10-conn[2])%10))   
    
unvisited_nodes = set([node for node in range(total_nodes)])
# Para cada nó, armazena os possíveis dígitos de soma de pedágios do nó inicial
toll_sums_from_zero = {node:set() for node in range(total_nodes)}
comb_cache = {}
final_output = [0 for digit in range(10)]

# Calcula todas as diferenças possíveis entre dois conjuntos de dígitos
def combine_set_pair(comb):
    result = [0 for digit in range(10)]
    for toll1 in comb[0]:
        for toll2 in comb[1]:
            result[(toll1-toll2)%10] = 1
    return result

# Processa cada componente conexa separadamente
while len(unvisited_nodes) > 0:
    subgraph_nodes = set()
    start_node = unvisited_nodes.pop()
    subgraph_nodes.add(start_node)
    current_iteration_list = []
    for neighbor in graph_paths[start_node]:
        if neighbor[1] not in toll_sums_from_zero[neighbor[0]]:
            toll_sums_from_zero[neighbor[0]].add(neighbor[1])
            current_iteration_list.append(neighbor)
            
    
    # BFS para encontrar todos os custos de pedágio possíveis
    next_iteration_list = []
    while len(current_iteration_list) > 0:
        for current_node in current_iteration_list:
            if current_node[0] in unvisited_nodes:
                unvisited_nodes.remove(current_node[0])
                subgraph_nodes.add(current_node[0])
            for neighbor in graph_paths[current_node[0]]:
                new_toll_digit = (current_node[1]+neighbor[1])%10
                if new_toll_digit not in toll_sums_from_zero[neighbor[0]]:
                    toll_sums_from_zero[neighbor[0]].add(new_toll_digit)
                    next_iteration_list.append((neighbor[0], new_toll_digit))
        current_iteration_list = next_iteration_list
        next_iteration_list = []
    
    # Agrupa nós por conjuntos idênticos de dígitos (otimização)
    subgraph_dict = {}
    for node in subgraph_nodes:
        frozen_set = frozenset(toll_sums_from_zero[node])
        if subgraph_dict.get(frozen_set) == None:
            subgraph_dict[frozen_set] = 1
        else:
            subgraph_dict[frozen_set] += 1

    # Calcula diferenças para todos os pares de nós
    for comb in it.product(subgraph_dict.keys(), repeat=2):
        if comb_cache.get(comb) == None:
            comb_cache[comb] = combine_set_pair(comb)
        multiplication_factor = subgraph_dict[comb[0]] * subgraph_dict[comb[1]]
        # Remove pares do nó consigo mesmo
        if comb[0] == comb[1]:
            multiplication_factor -= subgraph_dict[comb[0]]
        if multiplication_factor > 0:
            cached_result = comb_cache[comb]
            for digit in range(10):
                final_output[digit] += multiplication_factor * cached_result[digit]
    
for index, result in enumerate(final_output):
    print(result)  
