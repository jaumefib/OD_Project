
import csv
import numpy as np
from sklearn.decomposition import TruncatedSVD
import random


class GraphEmbedding(object):
    nodeAdjacency = {}
    nodeLabel = {}
    nodes = {}

    result = None

    def __init__(self):
        with open('musae_facebook_edges.csv', newline='', encoding="utf8") as csvfile:
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


        for origin in self.nodes:
            if origin in self.nodeAdjacency:
                listAux = self.nodeAdjacency[origin]
                listAux.append(origin)
                self.nodeAdjacency[origin] = listAux
            else:
                listAux = [origin]
                self.nodeAdjacency[origin] = listAux


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

        svd = TruncatedSVD(n_components=500, n_iter=10, random_state=42)
        svd.fit(toFactorize)
        self.result = svd.transform(toFactorize)

    def doWeHaveIt(self, page_name):
        for i in self.nodeLabel:
            if page_name in self.nodeLabel[i]:
                print("Did you mean the page " + self.nodeLabel[i] + " ?")
                correct_answer = False
                while not correct_answer:
                    is_the_one = str(input("'y' for yes, 'n' for no: "))
                    if is_the_one == "y":
                        return i
                    elif is_the_one == 'n':
                        correct_answer = True
                    else:
                        print("Sorry the answer didn't match the available options.")
                        print("Try again.")

        print("Sorry we don't have any " + page_name + " page.")
        print("Do you want a random page or try again?")
        option = input("'r' for random, 't' for try again: ")
        if option == "r":
            return random.randint(0, len(self.nodeLabel))
        else:
            return -1

    def getNearest(self, index):

        def find_nearest(matrix, array, originalIdx):
            auxDict = {}
            for idx, elem in enumerate(matrix):
                if idx != originalIdx:
                    dist = np.linalg.norm(elem - array)
                    auxDict[idx] = dist
            return auxDict

        nearestNodes = find_nearest(self.result, self.result[index], index)
        self.printResults(index, nearestNodes)

    def printResults(self, index, results):
        print("If you like the " + self.nodeLabel[index] + " page.")
        print("Maybe you will also like:")

        i = 0
        for w in sorted(results, key=results.get, reverse=False):
            print("    " + str(i) + ". " + self.nodeLabel[w] + " - " + str(np.linalg.norm(self.result[w]-self.result[index])))
            i = i+1
            if i == 20:
                break
