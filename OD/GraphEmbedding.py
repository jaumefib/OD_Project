# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv

import csv
import numpy as np
from sklearn.decomposition import TruncatedSVD


class GraphEmbedding(object):
    nodeAdjacency = {}
    nodeLabel = {}
    nodes = {}

    result = None

    def __init__(self):
        with open('musae_facebook_edges.csv', newline='',encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='"')
            next(reader, None)
            for row in reader:
                origin = int(row[0].split(",")[0])
                target = int(row[0].split(",")[1])
                self.nodes[origin] = 1
                self.nodes[target] = 1
                if origin in self.nodeAdjacency:
                    listAux = self.nodeAdjacency[origin]
                    listAux.append(target)
                    self.nodeAdjacency[origin] = listAux
                else:
                    listAux = [target]
                    self.nodeAdjacency[origin] = listAux
                if target in self.nodeAdjacency:
                    listAux = self.nodeAdjacency[target]
                    listAux.append(origin)
                    self.nodeAdjacency[target] = listAux
                else:
                    listAux = [origin]
                    self.nodeAdjacency[target] = listAux

        with open('musae_facebook_target.csv', newline='',encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter='\n', quotechar='"')
            next(reader, None)
            for row in reader:
                origin = int(row[0].split(",")[0])
                label = row[0].split(",")[2]
                self.nodeLabel[origin] = label

        toFactorize = np.zeros(shape=(len(self.nodes), len(self.nodes)))

        for key in sorted(self.nodeAdjacency):
            for val in self.nodeAdjacency[key]:
                toFactorize[key][val] = 1

        svd = TruncatedSVD(n_components=500, n_iter=1, random_state=42)
        svd.fit(toFactorize)
        self.result = svd.transform(toFactorize)

    def getNearest(self, index):

        def find_nearest(matrix, array, originalIdx):
            auxDict = {}
            for idx, elem in enumerate(matrix):
                if idx != originalIdx:
                    dist = np.linalg.norm(elem - array)
                    auxDict[idx] = dist
            return auxDict

        nearestNodes = find_nearest(self.result, self.result[index], index)

        print(self.nodeLabel[index])
        iter=0
        for w in sorted(nearestNodes, key=nearestNodes.get, reverse=False):
            print(self.nodeLabel[w])
            iter=iter+1
            if iter==20:
                break;
