import os

# How many folds to generate
Ks = 5
filepath = './JPEGImages/'

for i in range(Ks):
    os.makedirs('ImageSets/Main_%d'%(i+1), exist_ok=True)
total_files = os.listdir(filepath)


def generate_txts(file_list, k = 0):
    '''
    根据 file_list 生成 train.txt 和 val.txt
    k表示val中%K取余的第几个
    '''
    ftrain = open('ImageSets/Main_%d/train.txt'%(k+1), 'w')
    fval = open('ImageSets/Main_%d/val.txt'%(k+1), 'w')
    
    for i,f in enumerate(file_list):
        name = f[:-4] + '\n'
        if i % Ks == k:
            print(i, f)
            fval.write(name)
        else:
            ftrain.write(name)
    ftrain.close()
    fval.close()
    

for j in range(Ks):
    generate_txts(total_files, j)
    print("- - "* 50)
