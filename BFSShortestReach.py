#!/bin/python3

from collections import deque

class Solution:
    def bfs(n, m, edges, s):
        # Cria um dicionário para representar o grafo, onde cada nó tem uma lista de vizinhos
        graph = {i: [] for i in range(1, n+1)}
        # Adiciona as arestas ao grafo, não direcionado
        for i in edges:
            u, v = i
            graph[u].append(v)
            graph[v].append(u)
        queue = deque()
        # Vetor de distâncias, não visitado
        distance = [-1] * (n+1)
        distance[s] = 0
        # Coloca o nó inicial na fila
        queue.append(s)
        
        # Enquanto houver elementos na fila
        while queue:
            node = queue.popleft()  # Remove o próximo nó da fila
            for neighbor in graph[node]:
                # Se o vizinho ainda não foi visitado
                if distance[neighbor] == -1:
                    # Atualiza a distância do vizinho
                    distance[neighbor] = distance[node] + 6
                    # Adiciona o vizinho na fila para visitar depois
                    queue.append(neighbor)
        # Remove a posição 0 (não usada, pois os nós começam em 1)
        distance.remove(0)
        # Retorna as distâncias a partir do nó inicial
        return distance[1:]