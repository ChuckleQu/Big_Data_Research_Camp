import networkx as nx
import matplotlib.pyplot as plt
from Local_Structure_Entropy import Local_Structure_Entropy, ResolveGraphFile

graph_path = 'Homophyly.txt'  # 输入存储图的文件路径

# 将局部结构熵的结果储存在community中
community = Local_Structure_Entropy(graph_path, '3')
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

nx.draw_networkx_nodes(G, pos=position, nodelist=community, node_color='red', node_size=800)

# plt.savefig("result.png")
plt.show()
