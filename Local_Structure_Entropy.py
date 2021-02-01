"""
实现局部结构熵挖掘社区的算法
输入为，start: 图的起始点

"""

"""
代码中所涉及到的变量名的含义
vol1： 表示社区 1 的体积
g1： 表示社区 1 的割边数目
vol2： 表示社区 2 的体积
g2： 表示社区 2 的割边数目
vol3： 表示合并后的社区 3 的体积
g3： 表示合并后的社区 3 的割边数目
g12： 表示社区 1 和社区 2 之间的连边数目

"""
import pandas as pd
import math
import heapq


def ResolveGraphFile(graph_path):
    # 1. 读图的.txt文件，创建一个字典，用于存储图的邻接表
    # -----------------在下方填充代码完成功能------------
    adj_table = {}
    f = open(graph_path)
    for line in f:
        l = line.split()
        u = l[0]
        v = l[1]
        if u not in adj_table.keys():
            adj_table.update({u: {v: 1}})
        else:
            if v not in adj_table[u].keys():
                adj_table[u].update({v: 1})
            else:
                adj_table[u][v] += 1

        if v not in adj_table.keys():
            adj_table.update({v: {u: 1}})
        else:
            if u not in adj_table[v].keys():
                adj_table[v].update({u: 1})
            else:
                adj_table[v][u] += 1
    f.close()
    return adj_table
    # ***************** separate line******************


def Local_Structure_Entropy(graph_path, start, k=20):
    # 调用函数将存储图的文件解析成用字典存的邻接表，用adjacency_table表示图的邻接表，注意 Homophyly 应为带权图
    adjacency_table = ResolveGraphFile(graph_path)
    # 用字典存储每个节点的度数，key是节点ID，value是该节点的度数
    degree = {}
    # 存储所有度数的和
    m = 0
    # 计算每个节点的度数，以及所有节点度数之和
    for node in adjacency_table.keys():
        degree[node] = 0
        for neighbor, deg in adjacency_table[node].items():
            m += deg
            degree[node] += deg

    community = [start]  # 存储社区节点的列表
    neighbors = {}  # 当前社区的邻居字典集合

    vol1, g1 = 0.0, 0.0
    vol2, g2 = 0.0, 0.0
    vol3, g3 = 0.0, 0.0
    g12 = 0.0

    # 计算当前社区的邻居字典集合以及当前社区的体积与割边
    for neighbor, deg in adjacency_table[start].items():
        neighbors.update({neighbor: deg})
        vol1 += deg
        g1 += deg
    delta = 0.0

    # 2. 初始化，计算合并前后的结构熵的变化值delta
    # -----------------在下方填充代码完成功能------------
    def Delta(n):
        vol_n = degree[n]
        g_n = degree[n]
        E = 0
        for u in community:
            for v in adjacency_table[u].keys():
                if v == n:
                    E += 1
        vol1n = vol1 + vol_n
        d = 1 / m * ((vol1 - g1) * math.log(vol1n / vol1, 2) + (vol_n - g_n) * math.log(vol1n / vol_n,
                                                                                        2) - 2 * E * math.log(m / vol1n,
                                                                                                              2))
        return (d, n)

    heap = []
    for neighbor in adjacency_table[start].keys():
        heapq.heappush(heap, Delta(neighbor))
    item = heapq.heappop(heap)

    community_1 = community
    community_2 = [item[1]]

    # 更新社区列表于community_3
    community_3 = community_1
    community_3 += community_2

    com2Neighbors = {}
    # 计算community_2的邻居字典集合以及当前社区的体积与割边
    for neighbor, deg in adjacency_table[item[1]].items():
        com2Neighbors.update({neighbor: deg})
        vol2 += deg
        g2 += deg

    # 更新当前社区邻居集合于community_3
    com3Neighbors = neighbors
    com3Neighbors.update(com2Neighbors)
    for v in community_3:
        if v in com3Neighbors.keys():
            del com3Neighbors[v]

    # 更新社区体积和割边于community_3
    for v in community_3:
        for neighbor, deg in adjacency_table[v].items():
            vol3 += deg
            if neighbor not in community_3:
                g3 += deg

    # 将community_3各项指标赋给community
    community = community_3
    neighbors = com3Neighbors
    vol1 = vol3
    g1 = g3
    delta = item[0]

    # ***************** separate line******************

    # 当社区的大小小于参数 k 时 并且 delta 小于 0 ，也就是说结构熵仍然在减小，
    # 否则循环继续执行。
    while len(community) < k and delta < 0.0:
        # 3. 合并delta最大的两个社区，以及更新相关的数据结构，包括社区列表，社区体积大小，
        # 割边数目，邻居集合等
        # 4. 继续尝试将社区的邻居加入到社区之中，并记下结构熵减小最大的邻居
        # 每一次合并都是将一个单点加入已有的社区
        # -----------------在下方填充代码完成功能------------
        heap = []
        for neighbor in neighbors.keys():
            heapq.heappush(heap, Delta(neighbor))
        item = heapq.heappop(heap)
        community_1 = community
        community_2 = [item[1]]

        # 更新社区列表于community_3
        community_3 = community_1
        community_3 += community_2

        com2Neighbors = {}
        # 计算community_2的邻居字典集合以及当前社区的体积与割边
        for neighbor, deg in adjacency_table[item[1]].items():
            com2Neighbors.update({neighbor: deg})
            vol2 += deg
            g2 += deg

        # 更新当前社区邻居集合于community_3
        com3Neighbors = neighbors
        com3Neighbors.update(com2Neighbors)
        for v in community_3:
            if v in com3Neighbors.keys():
                del com3Neighbors[v]

        # 更新社区体积和割边于community_3
        for v in community_3:
            for neighbor, deg in adjacency_table[v].items():
                vol3 += deg
                if neighbor not in community_3:
                    g3 += deg

        # 将community_3各项指标赋给community
        community = community_3
        neighbors = com3Neighbors
        vol1 = vol3
        g1 = g3
        delta = item[0]

    # ***************** separate line******************
    return community


if __name__ == "__main__":
    file_name = "Homophyly.txt"  # 图的文件名
    start = '3'
    print(Local_Structure_Entropy(file_name, start))
