from gensim.models import word2vec
import numpy as np

sentences = word2vec.LineSentence('./data/nyc_jrlm_sentence.txt')
model = word2vec.Word2Vec(sentences, sg=0)

vec_dict = {}
for item in model.wv.vocab:
    vec_dict[item] = model.wv.get_vector(item)

def pairwise_distance(vector_a, vector_b):
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    sim = num / denom
    return 1.0 - sim

# 根据user和location进行一个top-k推荐，返回待推荐地点list
def RecTop(w, k, user, location):
    vec_user = model.wv.get_vector(user)
    vec_location = model.wv.get_vector(location)
    vec_agg = w*vec_user + (1-w)*vec_location
    score_dict = {}
    for item in model.wv.vocab:
        if item[0]=='l':
            vec_item = vec_dict[item]
            score = pairwise_distance(vec_agg, vec_item)
            score_dict[item] = score
    result = [x for x, v in sorted(score_dict.items(), key=lambda item: item[1])[:k]]
    return result
