'''
@lanhuage: python
@Descripttion: 
@version: beta
@Author: xiaoshuyui
@Date: 2020-06-17 16:56:25
@LastEditors: xiaoshuyui
@LastEditTime: 2020-06-17 17:05:18
'''
import os

filePath = 'D:\\testALg\\Diy-musics\\novel\\static\\holmes\\'

txts = []
for root,dirs,files in os.walk(filePath):
    for f in files:
        # if re.match(r'.*\d.*', f):
        fullname = os.path.join(root, f)
        txts.append(fullname)

print(txts)

res = ""
for f in txts:

    with open(f,'r',encoding='utf-8',errors='ignore') as fil:
        cotent = fil.read()

        res = res + cotent

with open('D:\\testALg\\Diy-musics\\novel\\static\\h.txt','w',encoding='utf-8') as f:
    f.write(res)
