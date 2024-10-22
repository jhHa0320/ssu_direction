# astar.py

import heapq
import random




# 건물 내부의 그래프를 나타내는 클래스
class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, cost):
        self.edges.setdefault(from_node, []).append((to_node, cost))

# A* 알고리즘을 사용하여 최단 경로를 찾는 함수
def astar(graph, start, goal):
    # 시작 노드부터의 거리를 나타내는 딕셔너리
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0

    # 시작 노드부터의 예상 거리를 나타내는 딕셔너리
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = heuristic(start, goal)

    open_set = [(f_score[start], start)]
    closed_set = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        closed_set.add(current)

        for neighbor, cost in graph.edges.get(current, []):
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # 경로를 찾을 수 없는 경우

# 건물 내부의 그래프를 생성하는 함수
def create_graph():
    graph = Graph()

    # 각 층별로 호실을 무작위로 배치하여 노드를 설정합니다.
    for floor in range(1, 13):
        for room_number in range(101, 274):
            # 무작위로 호실의 위치를 결정합니다. (예: 1층 101호부터 12층 273호까지)
            x = random.randint(0, 1000)  # 예시: 0부터 1000 사이의 임의의 값
            y = random.randint(0, 1000)  # 예시: 0부터 1000 사이의 임의의 값
            graph.add_node((floor, room_number), (x, y))  # 각 노드에 위치 정보를 포함시킵니다.

    # 인접한 호실 간의 이동 비용을 정의하여 엣지를 추가합니다.
    for floor in range(1, 12):
        for room_number in range(101, 274):
            # 인접한 호실과의 이동 비용은 무작위로 설정합니다. (예: 1 또는 2)
            cost = random.randint(1, 2)  # 예시: 1 또는 2
            graph.add_edge((floor, room_number), (floor + 1, room_number), cost)

    return graph


# 예상 거리(휴리스틱)를 계산하는 함수
def heuristic(node, goal):
    # 간단히 맨해튼 거리를 사용하겠습니다.
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# 건물 내부의 그래프를 생성하는 함수
def create_graph():
    graph = Graph()

    # 건물 내부의 노드들을 추가
    for floor in range(1, 13):
        for room_number in range(101, 274):
            graph.add_node((floor, room_number))

    # 인접한 호실 간의 이동 비용을 정의하여 엣지 추가
    for floor in range(1, 12):
        for room_number in range(101, 274):
            graph.add_edge((floor, room_number), (floor + 1, room_number), 1)

    return graph

# 건물 내부의 그래프 생성
building_graph = create_graph()

# 예시: 출발지와 목적지를 지정하여 최단 경로 찾기
start_node = (1, 101)  # 예시 출발지
goal_node = (5, 220)   # 예시 목적지

shortest_path = astar(building_graph, start_node, goal_node)
if shortest_path:
    print("Shortest path found:", shortest_path)
else:
    print("Path not found")
