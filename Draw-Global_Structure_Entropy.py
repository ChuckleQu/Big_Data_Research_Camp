import networkx as nx
import matplotlib.pyplot as plt
from Global_Structure_Entropy import Global_Structure_Entropy, ResolveGraphFile
import random

graph_path = 'Homophyly.txt'  # 输入存储图的文件路径

# 将局部结构熵的结果储存在community中
community = Global_Structure_Entropy(graph_path)
# 将Homophyly的邻接表储存在adjacency_table中
adjacency_table = ResolveGraphFile(graph_path)

edges = []

for node in adjacency_table:
    for neighbor in adjacency_table[node]:
        if int(node) < int(neighbor):
            edges.append((node, neighbor))

G = nx.Graph(directed=False)
G.add_edges_from(edges)
position = nx.spring_layout(G)
plt.figure(figsize=(30, 20))
nx.draw(G, pos=position, with_labels=False)

nx.draw_networkx_nodes(G, pos=position, nodelist=G.nodes(), node_size=300)


def randomColor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color


for i in range(len(community)):
    nx.draw_networkx_nodes(G, pos=position, nodelist=community[i], node_color=randomColor(), node_size=800)


plt.savefig("result.png")
plt.show()
