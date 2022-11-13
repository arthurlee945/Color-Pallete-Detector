from collections import defaultdict
import numpy as np


class KMeansCluster:
    def __init__(self, data, K):
        self.k = K
        self.points = [point(d, K) for d in data]

    def make_k_mapping(self, points):
        point_dict = defaultdict(list)
        for p in points:
            point_dict[p.k] = point_dict[p] + [p.data]
        return point_dict

    def calc_k_means(self, point_dict):
        return [np.mean(point_dict[k], axis=0) for k in range(self.k)]

    def update_k(self, points, means):
        for p in points:
            dist = [np.linalg.norm(means[k] - p.data) for k in range(self.k)]
            p.k = np.argmin(dist)

    def fit(self, points, epoch=10):
        for e in range(epoch):
            point_dict = self.make_k_mapping(self.points)
            means = self.calc_k_means(point_dict)
            self.update_k(point_dict, means)
        return means, points

    def evaluate(self, points):
        point_dict = self.make_k_mapping(points)
        means = self.calc_k_means(point_dict)
        dists = [np.linalg.norm(means[p.k] - p.data) for p in points]
        return np.mean(dists)


class point:
    def __init__(self, data, K=5):
        self.data = data
        self.k = np.random.randint(0, K)
