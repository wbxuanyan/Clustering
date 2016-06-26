# encoding:utf-8
from random import randint
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
dic = {}
f = open("D:\\pycharm edu\\series3.txt", "r")   # 打开存储用户活跃度序列的文件
diction = {}
user = {}

# 读取文本数据并将每个用户的活跃度序列按序保存到字典中              测试500个数据 分为3类
for i in range(800):
    a = f.read(528)
    num0 = a[0:192]      # 只截取前四天的数据
    num1 = num0.replace(' ', '')
    num2 = list(num1)
    liveness = [float(v) for v in num2]
    user[i+1] = liveness               # 将处理后的用户活跃度保存到user字典中
f.close()
print user


class DTW:                    # 定义DTW类，实现DTW算法
    series1 = []              # 定义两个活跃度序列，便于比较他们的相似度
    series2 = []

    def __init__(self):
        DTW.similarity()

    @classmethod
    def similarity(cls):      # 相似度的计算，调用两个函数
        for n in range(1, 96, 1):
            m = 1
            while True:
                dic[(n, m)] = min(cls.dtw(n-1, m), cls.dtw(n, m-1), cls.dtw(n-1, m-1)+cls.dis(n, m)) + cls.dis(n, m)
                m += 1
                if m == 96:
                    break
            if n == 95 and m == 96:
                lj_dis = dic[(n, m-1)]
                return lj_dis          # 返回一个累计距离，也就是序列相似度

    @staticmethod
    def dtw(n, m, lj_dis=0):
        if n == m == 0:
            return abs(DTW.series1[0] - DTW.series2[0])
        elif m == 0 and n > 0:
            for ii in range(0, n+1, 1):
                lj_dis += abs(DTW.series1[ii] - DTW.series2[0])
        elif n == 0 and m > 0:
            for iii in range(0, m+1, 1):
                lj_dis += abs(DTW.series1[0] - DTW.series2[iii])
        if n > 0 and m > 0:
                return dic[(n, m)]
        return lj_dis

    @staticmethod
    def dis(n, m):
        return abs(DTW.series1[n] - DTW.series2[m])   # 计算对应点的欧氏距离

for everyone in range(1, 800, 1):                   # 计算每两个不同的用户之间的相似度并用字典diction保存起来
    another = everyone + 1
    DTW.series2 = user[everyone]
    for another in range(another, 801, 1):
        DTW.series1 = user[another]
        diction[(everyone, another)] = DTW.similarity()
        diction[(another, everyone)] = diction[(everyone, another)]


# 计算每一类中的均值,也就是新的聚类中心，返回一个由三个48维均值组成的的列表
def means():
    meanslist = []
    global cluster1
    global cluster2
    global cluster3
    global cluster4
    # global cluster5
    for clusters in [cluster1, cluster2, cluster3, cluster4]:
        g = []
        for b in range(96):
            d = 0
            for c in clusters:
                d += user[c][b]
            e = d/len(clusters)
            g.append(e)
        meanslist.append(g)
    return meanslist


# 产生初始质心
initial = []  # 产生三个列表形式的初始质心
first = randint(1, 800)
print first
initial.append(user[first])  # 第一个随机初始质心
for h in range(3):            # 产生共三个初始质心
    sum1 = 0
    dd1 = []
    for j in range(1, 801, 1):
        dd2 = []
        for init in initial:
            DTW.series1 = init
            DTW.series2 = user[j]
            dd0 = DTW.similarity()     # 每个用户与质心的距离
            dd2.append(dd0)            # 添加到一个列表中
        ddmin = min(dd2)               # 选择最近距离
        dd1.append(ddmin)
        sum1 += ddmin                  # 将所有用户距离所有质心中的最近距离依次加起来
    k = randint(1, sum1)               # 生成一个随机数
    for cluster in dd1:
        k -= cluster                         # 依次减去每个用户的最近距离
        if k <= 0:
            nextone = dd1.index(cluster) + 1
            print nextone                 # 得到下一个初始质心的具体序列
            initial.append(user[nextone])
            break
cluster_center = initial


# 聚类的核心迭代部分
di = {}
z = 1
run = 1
iter_count = 0            # 迭代次数
while run:               # 建立一个反复聚类的过程直至满足算法停止条件时
    iter_count += 1
    cluster1 = []
    cluster2 = []
    cluster3 = []
    cluster4 = []
    for q in range(1, 801, 1):
        list1 = []
        DTW.series2 = user[q]
        for r in cluster_center:
            DTW.series1 = r
            lj_di = DTW.similarity()
            list1.append(lj_di)        # 距离列表
        lj_min = min(list1)            # 选出最小距离
        if list1.index(lj_min) == 0:
            cluster1.append(q)
        elif list1.index(lj_min) == 1:
            cluster2.append(q)
        elif list1.index(lj_min) == 2:
            cluster3.append(q)
        elif list1.index(lj_min) == 3:
            cluster4.append(q)
    # 选出每次聚类结果中簇内相似度平均值最大的那个簇
    in_similar = []            # 每个类的簇内相似度构成的列表
    ab4 = []                   # 产生多个空簇时依次分给每个空簇的数所构成的列表
    for cluste in [cluster1, cluster2, cluster3, cluster4]:
        if cluste:            # 聚类不为空簇时
            in_sum = 0         # 每个簇内所有数的簇内相似度总和
            for qq in cluste:
                in_dis = 0      # 簇内每个数到其他数的距离总和
                for ww in cluste:
                    if qq != ww:
                        in_dis += diction[(qq, ww)]
                    else:
                        continue
                if len(cluste) == 1:   # 簇内只有一个用户
                    num_similar = 0
                    in_sum += num_similar
                else:
                    num_similar = in_dis/(len(cluste) - 1)  # 第一类的第一个数的簇内相似度
                    in_sum += num_similar
            ab1 = in_sum / len(cluste)   # 第一个类的簇内相似度的平均值
            in_similar.append(ab1)
        else:                  # 聚类为空簇时添加一个0
            in_similar.append(0)
    ab2 = max(in_similar)      # 选择最大的簇内相似度平均值
    ab3 = in_similar.index(ab2)  # 簇内相似度最大的类的索引
    if ab3 == 0:             # 簇内相似度平均值最大的max_cluster，出现空簇时选择其中的随机一个数作为空簇聚类中心
        max_cluster = cluster1
    elif ab3 == 1:
        max_cluster = cluster2
    elif ab3 == 2:
        max_cluster = cluster3
    elif ab3 == 3:
        max_cluster = cluster4

    # 当出现空簇时对于空簇的处理
    empty_index = 0            # 判断空簇是哪个簇
    for clust in [cluster1, cluster2, cluster3, cluster4]:
        if clust:       # 非空
            empty_index += 1
            continue
        else:          # 空簇时
            ppp = randint(0, len(max_cluster) - 1)
            if ppp in ab4:                             # 产生多个空簇时，避免赋给空簇的用户数字是一样的
                ppp = randint(0, len(max_cluster) - 1)
            else:
                ab4.append(ppp)
            empty_num = max_cluster[ppp]            # 赋给空簇的数
            for uu in [cluster1, cluster2, cluster3, cluster4]:
                if empty_num in uu:
                    uu.remove(empty_num)             # 删除已经赋给非空簇的即将赋给空簇的用户数字
            if empty_index == 0:
                cluster1 = [empty_num]
            if empty_index == 1:
                cluster2 = [empty_num]
            if empty_index == 2:
                cluster3 = [empty_num]
            if empty_index == 3:
                cluster4 = [empty_num]
            empty_index += 1
    print cluster1, cluster2, cluster3, cluster4

# 利用轮廓系数判断聚类效果
    ee = 0
    for clus in [cluster1, cluster2, cluster3, cluster4]:
        for qq in clus:
            in_sum0 = 0
            for ww in clus:
                if qq != ww:
                    in_sum0 += diction[(qq, ww)]
                else:
                    continue
            if len(clus) == 1:
                num_similar1 = 0
            else:
                num_similar1 = in_sum0/(len(clus) - 1)  # 第一类的第一个数的簇内相似度
            out_no = []                               # 第一类的第一个数的簇外不相似度列表
            for clu in [cluster1, cluster2, cluster3, cluster4]:
                if clu != clus:
                    cc = 0
                    for bb in clu:
                        cc += diction[(qq, bb)]
                    dd = cc/len(clu)                 # 该数关于另一簇的簇外不相似度
                    out_no.append(dd)
                else:
                    continue
            out_min = min(out_no)                    # 选择簇外不相似度的平均值的最小值
            num_max = max(out_min, num_similar1)     # 选择两者中的大的数
            lk = (out_min - num_similar1)/num_max    # 第一类的第一个数的轮廓系数
            ee += lk
    lk_result = ee/800
    print lk_result                                  # 该聚类结果的轮廓系数
    if lk_result > 0.35:
        run = 0                                       # 轮廓系数大于0.35时跳出循环
        print "这里跳出"
        break
    cluster_center = means()
    di[z] = cluster_center          # 每次计算的聚类中心存入di字典，z作为索引
    z += 1

# 计算相邻的聚类中心列表的相似度，如果三个相似度都小于等于3，聚类完成跳出循环
    u = 0
    if z > 2:
        for ff in range(4):
            v = 0
            DTW.series1 = di[z - 1][ff]
            DTW.series2 = di[z - 2][ff]
            v = DTW.similarity()
            if v <= 3:
                u += 1
                if u == 3:
                    run = 0
                    print "中心点很相似"
                    break
    if iter_count == 50:                     # 迭代次数达到50次时跳出循环
        break
print iter_count
print "finished"

# Clustering result visualization
# 做四个可视化的图表示结果
dicti = {'red':   ((0.0, 1.0, 0.0),    # 数字2 用红色代表
                   (1.0, 0.0, 0.0),
                   (1.0, 1.0, 0.0)),

         'green': ((0.0, 1.0, 1.0),   # 数字0用绿色代表
                   (0.0, 1.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 1.0, 0.0),   # 数字1用蓝色代表
                   (1.0, 1.0, 1.0),
                   (1.0, 0.0, 1.0))
         }
blue_red1 = LinearSegmentedColormap('BlueRed1', dicti)
count = 0
for cl in [cluster1, cluster2, cluster3, cluster4]:
    count += 1
    list2 = []
    for every in cl:
        list2.append(user[every])
    matrix0 = np.matrix(list2)                          # 生成矩阵，用色度图表示聚类结果中每个用户的活跃度
    fig = plt.figure(count, figsize=(20, 20), dpi=100, facecolor="white")
    ax = plt.subplot()
    plt.imshow(matrix0, cmap=blue_red1, interpolation='nearest')
    x_pos = np.arange(len(user[1]))
    ax.set_xticks(x_pos)
    y_pos = np.arange(len(list2))
    ax.set_yticks(y_pos)
    ax.set_ylabel('user number')
    ax.set_xlabel('time distribution')
    ax.yaxis.grid()
plt.show()
