'''
用于绘制结构化数据的曲线，不管是mmdetection，或是detectron2、yolo的loss都可以绘制，需要自己定义分隔符（一般是逗号、空格、冒号等），以及表头自己写一下
'''

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def extract_log(log_file,new_log_file,key_word,filter_word=['nan']):
    with open(log_file, 'r') as f:
        with open(new_log_file, 'w') as train_log:
            for line in f:
                for filt in filter_word:
                    if filt in line:
                        break
                else:
                    if key_word in line:
                        train_log.write(line.lstrip())
    f.close()
    train_log.close()

    
def plot_key(log, key_length, key_idx, sep = ',', skiprows = 0, label = 'loss', plot_every = 1, figsize=(20, 12)):
    names = [str(x) for x in range(key_length)]
    result = pd.read_csv(log, skiprows=skiprows, sep = sep, names=names, engine='python')
    loss_list = result[str(key_idx)].str.split(':').str.get(1).str.split(' ').str.get(1)
    y = np.array([float(i) for i in loss_list.values])
    length = int(len(y)/plot_every)
    x = [i*20*plot_every for i in range(0, length)]
    y = [np.mean(y[plot_every * i : plot_every * (i+1)]) for i in range(length)]
    print(len(y), len(y), x[:5], y[:5])

    fig = plt.figure(figsize=figsize, dpi=80)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x, y, label=label)
    plt.grid()
    ax.legend()
    ax.set_title('The %s curves'%label)
    ax.set_xlabel('iters')
    ax.set_ylabel(label)
    if label == 'loss':
        plt.ylim(np.min(y), 1)
    #fig.savefig("./mean_loss.png")
    plt.show()
    
    
extract_log('20191219_055537.log','log_loss.txt','loss_rpn_cls')
names = ['info', 'eta1', 'eta2', 'time', 'data_time', 'memory', 'loss_rpn_cls', 'loss_rpn_bbox', 'loss_cls', 'acc', 'loss_bbox', 'loss']

for i in range(3, len(names)):
    plot_key('log_loss.txt', key_length=len(names), key_idx=i, label = names[i], plot_every=1, figsize=(8,4))
