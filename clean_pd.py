import os
import string
import pandas as pd

path = './ReutersNews106521'
df = pd.DataFrame(columns=['Firm', 'Time Stamp', 'Headlines', 'Priority Report'])

files = os.listdir(path)
for i in files:
    relPath = path + '/' + i
    if(relPath.find('.DS') > -1):
        continue
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

        dfi = []
        dfi.append(col1)
        dfi.append(col2)
        dfi.append(col3)
        # dfi.append(data)
        print(dfi)
        dfc = pd.DataFrame([].append(dfi), columns=['Firm', 'Time Stamp', 'Headlines', 'Priority Report'])
        print(dfc)
        lis = [df, dfc]
        df = pd.concat(lis, ignore_index = True)
        print(df)

df.to_csv('newspd.csv', sep='\t', encoding='utf-8')