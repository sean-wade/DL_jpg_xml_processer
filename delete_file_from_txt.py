import os

dir = 'JPG_ALL/'
txt = 'JPG_ALL_more.txt'

def delete_files(txt, dir):
    with open(txt, 'r') as t:
        lines = t.readlines()
    for f in lines:
        print(f)
        os.remove(dir + f.rstrip())
        
delete_files(txt, dir)

