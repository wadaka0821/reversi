from main import game
import main
import copy
import numpy as np
import csv
from network import Network

class Train():
    def __init__(self):
        self.num = 10
        self.generation = 0
        self.models_1 = [Network() for i in range(self.num)]
        self.models_2 = [Network() for i in range(self.num)]
        self.parents = list()

    def vs(self):
        model_temp = list()
        for i in range(self.num):
            result = game(self.models_1[i], self.models_2[i])
            if result == 0:
                model_temp.append(copy.deepcopy(self.models_1[i]))
            else:
                model_temp.append(copy.deepcopy(self.models_2[i]))

        self.resset()

        for i in range(self.num):
            index1, index2 = np.random.randint(0, self.num), np.random.randint(0, self.num)
            a_1 = np.random.rand()

            self.models_1.append(Network())
            self.models_1[-1].w_1 = model_temp[index1].w_1*a_1 + model_temp[index2].w_1*(1.-a_1)
            self.models_1[-1].w_2 = model_temp[index1].w_2*a_1 + model_temp[index2].w_2*(1.-a_1)

            index1, index2 = np.random.randint(0, self.num), np.random.randint(0, self.num)
            a_1 = np.random.rand()

            self.models_2.append(Network())
            self.models_2[-1].w_1 = model_temp[index1].w_1*a_1 + model_temp[index2].w_1*(1.-a_1)
            self.models_2[-1].w_2 = model_temp[index1].w_2*a_1 + model_temp[index2].w_2*(1.-a_1)

    def resset(self):
        for i in range(self.num):
            del self.models_1[0]
            del self.models_2[0]

    def train(self, max_gen):
        while self.generation <= max_gen:
            self.vs()
            self.generation += 1

    def save(self, index, model=1):
        with open('parameters.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.models_1[index].w_1)
            writer.writerows(self.models_1[index].w_2)

if __name__ == '__main__':
    t = Train()
    t.train(10)
    t.save(0)
