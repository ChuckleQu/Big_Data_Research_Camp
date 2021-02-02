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
import math
import heapq
import itertools

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


def Global_Structure_Entropy(graph_path):
    # 调用函数将存储图的文件解析成用字典存的邻接表，用adjacency_table表示图的邻接表，注意 Homophyly 应为带权图
    adjacency_table = ResolveGraphFile(graph_path)
    # 用字典存储每个节点的度数，key是节点ID，value是该节点的度数
    degree = {}
    # 存储所有度数的和
    m = 0
    # community = [[community_1], [community_2], ...]
    community = []  # 存储社区节点的列表
    # 计算每个节点的度数，以及所有节点度数之和；并构建社区节点列表
    for node in adjacency_table.keys():
        degree[node] = 0
        community.append([node])
        for neighbor, deg in adjacency_table[node].items():
            m += deg
            degree[node] += deg

    # 计算当前社区的邻居字典集合以及当前社区的体积与割边
    def Vol_g(com):
        vol = 0
        g = 0
        for node in com:
            for neighbor, deg in adjacency_table[node].items():
                vol += deg
                if neighbor not in com:
                    g += deg
        return vol, g

    def G_12(com1, com2):
        g_12 = 0
        for node in com1:
            for neighbor in adjacency_table[node].keys():
                if neighbor in com2:
                    g_12 += 1
        return g_12
    delta = 0.0

    # 2. 初始化，计算合并前后的结构熵的变化值delta
    # -----------------在下方填充代码完成功能------------
    def Delta(com1, com2):
        vol_1, g_1 = Vol_g(com1)
        vol_2, g_2 = Vol_g(com2)
        g_12 = G_12(com1, com2)
        vol_12 = vol_1 + vol_2
        d = 1 / m * ((vol_1 - g_1) * math.log(vol_12 / vol_1, 2) + (vol_2 - g_2) * math.log(vol_12 / vol_2, 2) - 2 * g_12
                     * math.log(m / vol_12, 2))
        return (d, com1, com2)

    heap = []
    allCombinations = list(itertools.combinations(community, 2))
    for combination in allCombinations:
        com_1 = combination[0]
        com_2 = combination[1]
        heapq.heappush(heap, Delta(com_1, com_2))
    item = heapq.heappop(heap)

    community_1 = item[1]
    community_2 = item[2]

    # 合并community_1和community_2于community_3
    community_3 = community_1
    community_3 += community_2

    # 更新community
    community.remove(community_1)
    community.remove(community_2)
    community.append(community_3)
    delta = item[0]

    # ***************** separate line******************
    # 当delta 小于 0 ，也就是说结构熵仍然在减小，
    # 否则循环继续执行。
    while delta < 0.0:
        # 3. 合并delta最大的两个社区，以及更新相关的数据结构，包括社区列表，社区体积大小，
        # 割边数目，邻居集合等
        # 4. 继续尝试将社区的邻居加入到社区之中，并记下结构熵减小最大的邻居
        # -----------------在下方填充代码完成功能------------
        heap = []
        allCombinations = list(itertools.combinations(community, 2))
        for combination in allCombinations:
            com_1 = combination[0]
            com_2 = combination[1]
            heapq.heappush(heap, Delta(com_1, com_2))
        item = heapq.heappop(heap)

        community_1 = item[1]
        community_2 = item[2]

        # 合并community_1和community_2于community_3
        community_3 = community_1
        community_3 += community_2

        # 更新community
        community.remove(community_1)
        community.remove(community_2)
        community.append(community_3)
        delta = item[0]

    # ***************** separate line******************
    return community


if __name__ == "__main__":
    file_name = "test.txt"  # 图的文件名
    print(Global_Structure_Entropy(file_name))
