import numpy as np
import csv

class Network():
    def __init__(self):
        self.w_1 = np.zeros((6, 10))
        self.w_2 = np.zeros((11, 1))
        #self.w_3 = np.zeros((21, 64))

        self.init_param(1)

    def init_param(self, sigma):
        
        for i in range(len(self.w_1)):
            for j in range(self.w_1.shape[1]):
                self.w_1[i][j] = np.random.normal(0, sigma)

        for i in range(len(self.w_2)):
            for j in range(self.w_2.shape[1]):
                self.w_2[i][j] = np.random.normal(0, sigma)
        '''
        for i in range(len(self.w_3)):
            for j in range(self.w_3.shape[1]):
                self.w_3[i][j] = np.random.normal(0, sigma)
        

        for i in range(len(self.w_1)):
            for j in range(self.w_1.shape[1]):
                self.w_1[i][j] = (np.random.rand()-0.5)*10

        for i in range(len(self.w_2)):
            for j in range(self.w_2.shape[1]):
                self.w_2[i][j] = (np.random.rand()-0.5)*10

        
        for i in range(len(self.w_3)):
            for j in range(self.w_3.shape[1]):
                self.w_3[i][j] = (np.random.rand()-0.5)*10
        '''

    def feedforward(self, x):
        x = np.append(x, 1.)

        a_1 = np.dot(self.w_1.T, x)
        z_1 = self.sigmoid(a_1)

        z_1 = np.append(z_1, 1.)
        a_2 = np.dot(self.w_2.T, z_1)
        '''
        z_2 = self.sigmoid(a_2)

        z_2 = np.append(z_2, 1.)
        a_3 = np.dot(self.w_3.T, z_2)
        '''

        return a_2

    def sigmoid(self, a):
        return 1. / (1. + np.exp(-a))

    def load(self, filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            size = self.w_1.shape
            for i in range(size[0]):
                buffer = next(reader)
                for j in range(size[1]):
                    self.w_1[i][j] = buffer[j]
            
            size = self.w_2.shape
            for i in range(size[0]):
                buffer = next(reader)
                for j in range(size[1]):
                    self.w_2[i][j] = buffer[j]

            '''
            size = self.w_3.shape
            for i in range(size[0]):
                buffer = next(reader)
                for j in range(size[1]):
                    self.w_3[i][j] = buffer[j]
            '''


if __name__ == '__main__':
    net = Network()

    field_height = 8
    field_width = 8
    #盤面の状態を保存（0:なし, -1:黒, 1:白）
    field = [[0 for i in range(field_width)] for j in range(field_height)]

    #盤面の初期設定
    field[3][3] = -1
    field[3][4] = 1
    field[4][3] = 1
    field[4][4] = -1

    print(net.w_1)
    print(net.w_2)

    print(net.feedforward(field))