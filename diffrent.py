import os


D1 = 'JPEGImages/'
D2 = 'Annotations/'



def printDiff(dir1, dir2):
    file1_ls = os.listdir(dir1)	

    for i,f in enumerate(file1_ls):
        file1_ls[i]=file1_ls[i][:-3]

    #print(file1_ls)
    with open(dir2[:-1]+'_more.txt', 'a') as txt:
        for a,b,c in os.walk(dir2):
            for f in c:
                if f[:-3] not in file1_ls:
                    txt.write(f+'\n')
                    print(dir2 + ' has more: ', f)


printDiff(D1, D2)
printDiff(D2, D1)
