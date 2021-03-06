from torch.utils.data import Dataset, DataLoader
import glob
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
import warnings
import random
import time
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

warnings.filterwarnings('ignore')

seed = 0
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False


def data_transforms(data):
    (a, b, c, d, e) = data.shape
    S = np.zeros((a, b - 1, c, d, e - 1))
    for i in range(0, b - 1):
        if i == 1:
            j = i + 1
        else:
            j = i
        S[:, i, :, :, 0] = data[:, j, :, :, 0]
    S = np.resize(S, (1, 65, 65))
    S = torch.tensor(S)
    S = S.float()
    return S



class my_dataset(Dataset):
    def __init__(self, store_path, split, data_transform=None):
        self.store_path = store_path
        self.split = split
        self.transforms = data_transform
        self.img_list = []
        self.label_list = []
        for file in glob.glob(self.store_path + '/' + split + '/000/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(0)
        for file in glob.glob(self.store_path + '/' + split + '/001/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(1)
        for file in glob.glob(self.store_path + '/' + split + '/002/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(2)
        for file in glob.glob(self.store_path + '/' + split + '/003/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(3)
        for file in glob.glob(self.store_path + '/' + split + '/004/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/004A/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/004B/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/004C/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/0004/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/0004A/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/0004B/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/0004C/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/1004/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/1004A/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/1004B/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/1004C/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/2004/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/2004A/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/2004B/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)
        for file in glob.glob(self.store_path + '/' + split + '/2004C/*.npy'):
            # print(file)
            cur_path = file.replace('\\', '/')
            self.img_list.append(cur_path)
            self.label_list.append(4)



    def __getitem__(self, item):
        data = np.load(self.img_list[item])
        data = data_transforms(data)
        label = self.label_list[item]
        return data, label

    def __len__(self):
        return len(self.img_list)


####################????????????????????????????????????CNN???####################
def define_model():
    class Net(torch.nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.conv3 = nn.Conv2d(1, 16, 3, stride=2)  # ?????????C3???3x3????????????2???????????????feature_map=16
            self.pool3 = nn.MaxPool2d(2, 2)  # 2x2?????????
            self.conv4 = nn.Conv2d(16, 32, 3)  # ?????????C4???3x3????????????1???????????????feature_map=32
            # ??????????????????
            self.fc1 = nn.Linear(32 * 14 * 14, 1200)
            self.fc15 = nn.Linear(1200, 84)
            self.fc2 = nn.Linear(84, 5)  # ???????????????1x5?????????

        def forward(self, x):
            # ???????????????relu?????????????????????????????????????????????
            x = self.pool3(torch.relu(self.conv3(x)))
            x = torch.relu(self.conv4(x))
            # ??????????????????relu??????????????????
            x = x.view(x.size(0), -1)
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc15(x))
            x = self.fc2(x)
            return x

    net = Net()
    return net


################?????????????????????CrossEntropyLoss???##################
def define_loss():
    Loss = nn.CrossEntropyLoss()
    return Loss


##############???????????????#############
def define_optimizer(learning_rate):
    optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate,
                                 betas=(0.9, 0.999),
                                 eps=1e-08,
                                 weight_decay=0,
                                 amsgrad=False)
    return optimizer



def acc(y_pred, y):
    t = 0
    (X, Y) = y_pred.shape
    for j in range(0, X):
        max = -999
        index = -1
        for i in range(0, Y):
           if y_pred[j, i] > max:
               max = y_pred[j, i]
               index = i
        if y[j] == index:
            t = t + 1
    return t


###################????????????#################
def train(loader, net, Loss, num, optimizer):
    print('start training:')
    sum_loss = 0
    i = 0
    t = 0
    j = 0
    for epoch in range(15):
        for x, y in loader:
            x = x.cuda(0)
            y = y.cuda(0)
            y_pred = net(x)  # ????????????????????????????????????x???????????????y
            loss = Loss(y_pred, y)  # ??????loss
            print("???{}???,CrossEntropyLoss??? {}".format(i + 1, loss.item()))
            i = i + 1
            optimizer.zero_grad()  # ??????????????????????????????optimizer?????????????????????????????????????????????
            loss.backward()  # ??????????????????????????????????????????loss?????????
            optimizer.step()  # ??????Optimizer???step??????????????????????????????
    for x, y in loader:
        x = x.cuda(0)
        y = y.cuda(0)
        y_pred = net(x)    # ????????????????????????????????????x???????????????y
        (X) = len(y)
        t = t + acc(y_pred, y)    #???????????????
        j = j + X         #???????????????
        loss = Loss(y_pred, y)  # ???????????????????????????
        sum_loss = sum_loss + loss   #????????????????????????
    print("????????????,CrossEntropyLoss??? {}".format(sum_loss / j))
    print("????????????????????????????????? {}".format(t / j))    #??????????????????????????????
    return net


###################????????????###################
def test(loader, net, Loss, num):
    sum_loss = 0
    i = 0
    t = 0
    for x, y in loader:
        y_pred = net(x)
        #print(y_pred)
        #print(y)
        loss = (Loss(y_pred, y))  # ??????loss
        sum_loss = sum_loss + loss
        t = t + acc(y_pred, y)   #???????????????
        i = i + 1           #???????????????
    print("????????????,CrossEntropyLoss??? {}".format(sum_loss / i))
    print("????????????????????????????????? {}".format(t / i))     #??????????????????????????????
    return 0


if __name__ == '__main__':
    start = time.time()
    #store_path = 'D:/rengongzhinengshiyan/????????????????????????/data'
    store_path = '.'
    split = 'Data1/train'
    train_dataset = my_dataset(store_path, split, data_transforms)
    num = 4        #batch_size
    dataset_loader = DataLoader(train_dataset, batch_size=num, shuffle=True, num_workers=1)  #?????????????????????
    net = define_model()
    net = net.cuda(0)
    Loss = define_loss()
    optimizer = define_optimizer(1e-4)
    Net1 = train(dataset_loader, net, Loss, num, optimizer)
    Net1.eval()
    Net1 = Net1.cpu()
    split = 'data/test'
    num = 1        #batch_size
    test_dataset = my_dataset(store_path, split, data_transforms)
    test_dataset_loader = DataLoader(test_dataset, batch_size=num, shuffle=True, num_workers=1)  #?????????????????????
    test(test_dataset_loader, Net1, Loss, num)
    end = time.time()
    Time = end - start
    print("??????????????? {} s".format(Time))