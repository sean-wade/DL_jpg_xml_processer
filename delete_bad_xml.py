import os


root = 'JPEGImages/'


with open('moreJ.txt', 'r') as f:
    for l in f.readlines():
        os.remove((root+l).strip('\n'))
