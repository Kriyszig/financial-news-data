import os
import string

path = './ReutersNews106521'

def readContent(relPath):
    if(relPath.find('.DS') > -1):
        return
    files = os.listdir(relPath)
    for f in files:
        if(f.find('.tar') > -1 or f.find('.DS') > -1):
            continue
        pwf = open(relPath + '/' + f, 'r')
        lines = pwf.readlines()
        col1 = f[0: f.find('-id')]
        if(len(lines) < 1):
            continue
        col2 = lines[2][3: lines[2].find('\n')].replace(',', '')
        col3 = lines[0][3: lines[0].find('\n')].replace(',', '')

        if(len(lines) < 7):
            continue
        lines.append('\n')
        limit = lines[7: ].index('\n')
        data = ''
        for i in range(7, 7 + limit):
            data = data + str(lines[i].replace('\n', ' '))
        pwf.close()
        exclude = set(string.punctuation)
        data = ''.join(ch for ch in data if ch not in exclude)

        with open('./news.csv', 'a') as newsFile:
            print('{},{},{},{}'.format(col1, col2, col3, data), file = newsFile)


files = os.listdir(path)
for i in files:
    readContent(path + '/' + i)