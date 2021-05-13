# 进行推荐的hme算法部分，我们给定一个用户(uXXX)和地点(lXXX)，为用户推荐接下来可以访问的餐厅
# 为了计算更快，同时保持一个比较高的准确率，在这里取嵌入维度d=20
# 推荐流程：1.获得用户和该餐馆的庞加莱球嵌入坐标 2.计算聚合坐标 3.计算聚合坐标与其他所有餐馆的庞加莱球距离和地理距离 4.排名获取结果

import numpy as np
import pandas as pd
import math
from math import radians, cos, sin, asin, sqrt, fabs

df = pd.read_table('./data/nyc_hyper_20.txt', header=None, delim_whitespace=True)
df1 = df.iloc[:, 0]
df2 = np.array(df.iloc[:, 1:20])
vec_array = []      # 用户和地点的字符串集合
vec_dict = {}       # 用户：庞加莱坐标， 地点：庞加莱坐标
for (key, value) in zip(df1, df2):
    vec_dict[key] = value
for item in df1:
    vec_array.append(item)

# 读取餐馆的经纬度
df_geo = pd.read_csv('./data/rrs_resturant.csv')
df_geo = df_geo[['venueId', 'latitude', 'longitude']]

# 地点 经度 维度
loc_array = []
lat_array = []
long_array = []
for item1, item2, item3 in zip(df_geo['venueId'], df_geo['latitude'], df_geo['longitude']):
    loc_array.append(item1)
    lat_array.append(item2)
    long_array.append(item3)
index_dict = {}     # 存储地点对应的下标，方便快速查找
for i in range(len(loc_array)):
    index_dict[loc_array[i]] = i

# 计算庞加莱球距离
def DisPoincareBall(x1, x2):
    a = np.array(x1)
    b = np.array(x2)
    c = a - b
    l2norm_a = np.inner(a, a)
    l2norm_b = np.inner(b, b)
    l2norm_c = np.inner(c, c)
    x = 1 + 2 * l2norm_c / ((1 - l2norm_a) * (1 - l2norm_b))
    return np.log(x + math.sqrt(x * x - 1))

# 将庞加莱球坐标转换为克莱因坐标
def PoincareBall2Klein(x):
    l2norm = 0.0
    for item in x:
        l2norm += item * item
    klein = []
    for item in x:
        axis = 2 * item / (1 + l2norm)
        klein.append(axis)
    return np.array(klein)

# 在克莱因模型下计算爱因斯坦中值聚合坐标
def EisteinMidAggregation(w, x_u, x_lc):
    l2norm_u = 0.0
    l2norm_lc = 0.0
    for item in x_u:
        l2norm_u += item * item
    for item in x_lc:
        l2norm_lc += item * item
    lorentzFactor_u = 1 / math.sqrt(1 - l2norm_u)
    lorentzFactor_lc = 1 / math.sqrt(1 - l2norm_lc)
    klein_agg = []
    for (item_u, item_lc) in zip(x_u, x_lc):
        agg = w * lorentzFactor_u * item_u / (w * lorentzFactor_u + (1 - w) * lorentzFactor_lc) + (
                1 - w) * lorentzFactor_lc * item_lc / (w * lorentzFactor_u + (1 - w) * lorentzFactor_lc)
        klein_agg.append(agg)

    return np.array(klein_agg)

# 将克莱因坐标转换为庞加莱球坐标
def Klein2PoincareBall(x):
    l2norm = 0.0
    for item in x:
        l2norm += item * item
    poincare = []
    for item in x:
        axis = item / (1 + math.sqrt(1 - l2norm))
        poincare.append(axis)
    return np.array(poincare)

# 计算得分
def PoincareScore(geoDis, x1, x2):
    return ((1 + geoDis) ** 0.25) * DisPoincareBall(x1, x2)

# 输入用户和地点，计算聚合后的庞加莱坐标
def GetAggPoincare(w, user, location):
    poincare_u = vec_dict[user]
    poincare_l = vec_dict[location]
    klein_u = PoincareBall2Klein(poincare_u)
    klein_l = PoincareBall2Klein(poincare_l)
    klein_agg = EisteinMidAggregation(w, klein_u, klein_l)
    poincare_agg = Klein2PoincareBall(klein_agg)
    return poincare_agg

# 地理位置距离
def GeoDis(loc_1, loc_2):
    index_1 = index_dict[loc_1]
    index_2 = index_dict[loc_2]
    lon1 = long_array[index_1]
    lat1 = lat_array[index_1]
    lon2 = long_array[index_2]
    lat2 = lat_array[index_2]
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = fabs(lon2 - lon1)
    dlat = fabs(lat2 - lat1)
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

def RecTopK(w, k, user, location):
    if user not in vec_array:
        user = vec_array[1]
    if location not in vec_array:
        location = vec_array[0]
    scoreDict = {}
    poincare_agg = GetAggPoincare(w, user, location)
    for item in df1:
        if item[0] == 'l':
            poincare_loc = vec_dict[item]
            score = PoincareScore(GeoDis(item, location), poincare_loc, poincare_agg)
            scoreDict[item] = score
    result = [x for x, v in sorted(scoreDict.items(), key=lambda item: item[1])[:k]]
    return result
