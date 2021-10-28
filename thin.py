# -*- coding: UTF-8 -*-
import os
import re
import json

data = {}
with open ('./RefreshingData.json',"r",encoding='utf-8') as f:
    thdata=json.load(f)
for i in range(len(thdata)):
    ids = thdata[i]['id']
    data[ids] = {}
    data[ids]['totalreply'] =thdata[i]['totalreply']
    data[ids]['title'] =thdata[i]['title']
    data[ids]['lastedit'] =thdata[i]['lastedit']
    data[ids]['category'] =thdata[i]['category']
    data[ids]['active'] =thdata[i]['active']

with open('./RefreshingData.json',"w",encoding='utf-8') as f:
    f.write(json.dumps(data,indent=2,ensure_ascii=False))
# def all_files_path(rootDir):
#     for root, dirs, files in os.walk(rootDir):     # 分别代表根目录、文件夹、文件
#         for file in files:                         # 遍历文件
#             file_path = os.path.join(root, file)   # 获取文件绝对路径
#             filepaths.append(file_path)            # 将文件路径添加进列表
#         for dir in dirs:                           # 遍历目录下的子目录
#             dir_path = os.path.join(root, dir)     # 获取子目录路径
#             all_files_path(dir_path)               # 递归调用
# def getkwfile(flist, keyword):
#     res = []
#     for ff in flist:
#         if keyword in ff.split('\\')[-1]:   # 切分出文件名来再判断，可以缩短判断时间
#             res.append(ff)
#     return res

# if __name__ == "__main__":
#     dirpath = '/home/riko/S1PlainTextBackup/'
#     filepaths = []                                 # 初始化列表用来
#     all_files_path(dirpath)
#     filepath2 = getkwfile(filepaths, 'md')
#     for filepath in filepath2:
#         with open (filepath, 'r',encoding='UTF-8') as f:
#             content = f.read()
#             contentstring = re.sub(r'\n{4,}','\n\n\n',str(content))
#         with open (filepath, 'w',encoding='UTF-8') as f:
#             f.write(contentstring)
