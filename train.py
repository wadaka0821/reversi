from main import game
import main
import copy
import numpy as np
import csv
from network import Network

class Train():
    def __init__(self):
        self.num = 50
        self.generation = 1
        self.models_1 = [Network() for i in range(self.num)]
        self.models_2 = [Network() for i in range(self.num)]
        self.parents = list()
        self.alpha = 0.02

    def vs(self):
        model_temp = list()
        for i in range(self.num):
            result = game(self.models_1[i], self.models_2[i], info=[self.generation, i+1])
            if result:
                model_temp.append(copy.deepcopy(self.models_1[i]))
            else:
                model_temp.append(copy.deepcopy(self.models_2[i]))

        self.resset()

        for i in range(self.num):
            index1, index2 = np.random.randint(0, self.num), np.random.randint(0, self.num)
            a_1 = np.random.rand()

            self.models_1.append(Network())
            self.models_1[-1].w_1 = model_temp[index1].w_1*a_1 + model_temp[index2].w_1*(1.-a_1)
            for j in range(len(self.models_1[-1].w_1)):
                if np.random.rand() < self.alpha:
                    self.models_1[-1].w_1[j] = np.random.normal(0, 1)
   
            self.models_1[-1].w_2 = model_temp[index1].w_2*a_1 + model_temp[index2].w_2*(1.-a_1)
            for j in range(len(self.models_1[-1].w_2)):
                if np.random.rand() < self.alpha:
                    self.models_1[-1].w_2[j] = np.random.normal(0, 1)

            self.models_1[-1].w_3 = model_temp[index1].w_3*a_1 + model_temp[index2].w_3*(1.-a_1)
            for j in range(len(self.models_1[-1].w_3)):
                if np.random.rand() < self.alpha:
                    self.models_1[-1].w_3[j] = np.random.normal(0, 1)

            #self.models_1[-1].w_3 = model_temp[index1].w_3*a_1 + model_temp[index2].w_3*(1.-a_1)

            index1, index2 = np.random.randint(0, self.num), np.random.randint(0, self.num)
            a_1 = np.random.rand()

            self.models_2.append(Network())
            self.models_2[-1].w_1 = model_temp[index1].w_1*a_1 + model_temp[index2].w_1*(1.-a_1)
            for j in range(len(self.models_1[-1].w_1)):
                if np.random.rand() < self.alpha:
                    self.models_2[-1].w_1[j] = np.random.normal(0, 1)
   
            self.models_2[-1].w_2 = model_temp[index1].w_2*a_1 + model_temp[index2].w_2*(1.-a_1)
            for j in range(len(self.models_1[-1].w_2)):
                if np.random.rand() < self.alpha:
                    self.models_2[-1].w_2[j] = np.random.normal(0, 1)

            self.models_2[-1].w_3 = model_temp[index1].w_3*a_1 + model_temp[index2].w_3*(1.-a_1)
            for j in range(len(self.models_1[-1].w_3)):
                if np.random.rand() < self.alpha:
                    self.models_2[-1].w_3[j] = np.random.normal(0, 1)
            #self.models_2[-1].w_3 = model_temp[index1].w_3*a_1 + model_temp[index2].w_3*(1.-a_1)

    def resset(self):
        for i in range(self.num):
            del self.models_1[0]
            del self.models_2[0]

    def train(self, max_gen):
        while self.generation <= max_gen:
            self.vs()
            self.generation += 1

    def save(self, index, filename, model=1):
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.models_1[index].w_1)
            writer.writerows(self.models_1[index].w_2)
            writer.writerows(self.models_1[index].w_3)

if __name__ == '__main__':
    t = Train()
    save_list = [10, 30, 50, 75, 100, 125, 150]
    for i in save_list:
        t.train(i)
        t.save(0, 'params_rand/params_rand('+str(i)+').csv')
