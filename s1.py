# -*- coding: UTF-8 -*-
#!/usr/bin/env/ python3
import requests
from bs4 import BeautifulSoup
import re
import time
import sys
import io
import os
import json
import math
import asyncio,aiohttp

sys.excepthook = lambda *args: exit(1)
# def remov(path):
#     path=path.encode('utf-8')
#     if(os.path.exists(path)):
#         os.remove(path)
def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    path=path.encode('utf-8')
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False

def parse_html(html):
    # soup = BeautifulSoup(html,from_encoding="utf-8",features="lxml")
    soup = BeautifulSoup(html, 'html.parser')
    namelist = soup.find_all(name="div", attrs={"class":"pi"})
    # replylist = soup.find_all(name="td", attrs={"class":"t_f"})
    replylist = soup.find_all(name='div', attrs={"class":"pcb"})
    # next_page = soup.find('a', attrs={'class': 'nxt'})
    # if next_page:
    #     return soupname, souptime, next_page['herf']
    title = soup.find_all(name='span',attrs={"id":"thread_subject"})
    total_page = int((re.findall(r'<span title="共 (\d+) 页">', str(soup)) + [1])[0])
    titles = re.sub(r'<.+?>','',str(title))
    titles = re.sub(r'[\]\[]','',titles)
    titles = re.sub(r'\|','｜',titles)
    titles = re.sub(r'/','／',titles)
    titles = re.sub(r'\\','＼',titles)
    titles = re.sub(r':','：',titles)
    titles = re.sub(r'\*','＊',titles)
    titles = re.sub(r'\?','？',titles)
    titles = re.sub(r'"','＂',titles)
    titles = re.sub(r'<','＜',titles)
    titles = re.sub(r'>','＞',titles)
    titles = re.sub(r'\.\.\.','…',titles)
    titles = '['+titles+']'
    return namelist,replylist,total_page,titles
# \d{4}-\d{1}-\d{1}\s\d{2}\:\d{2}

def addtimestamp(filedir,lasttimestamp):
    with open(filedir, 'r+',encoding='UTF-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('> ## **本文件最后更新于'+lasttimestamp+'** \n\n'+content)

def get_FileSize(filePath):

    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024 * 1024)

    return round(fsize, 2)

def FormatStr(namelist, replylist,totalreply):
    nametime = []
    replys = []
    times = []
    output= ''
    replynumber = []
    lastreply = totalreply
    for i in namelist:
        i = i = re.sub(r'[\r\n]',' ',str(i))
        nametime.append(re.sub(r'<.+?>','',i))
    names = nametime[::2]
    timestamp = nametime[1::2]
    for i in timestamp:
        i = re.sub(r'[\r\n]',' ',str(i))
        i = re.sub(r'电梯直达','1#',i)
        j = re.search(r'\d+[\S\s]+发表于\s\d+-\d+-\d+\s\d+:\d+',i)
        k = re.search(r'\d+',i)
        #k = re.search(r'\d+', k.group(0))
        #正则搜索返回的是正则match object
        times.append(j.group(0))
        replynumber.append(int(k.group(0)))
    for i in replylist:
        i = re.sub(r'\r','\n',str(i))
        # i = re.sub(r'\n\n','\n',i)
        i = re.sub(r'<blockquote>','[[[[blockquote]]]]',i)
        i = re.sub(r'</blockquote>','[[[[/blockquote]]]]',i)
        # i = re.sub(r'</blockquote>','\n',i)
        i = re.sub(r'<strong>','[[[[strong]]]]',i)
        i = re.sub(r'</strong>','[[[[/strong]]]]',i)
        # i = re.sub(r'</strong>','** ',i)
        i = re.sub(r'<span class=\"icon_ring vm\">','﹍﹍﹍\n\n',str(i))
        i = re.sub(r'<td class="x.1">','|',i)
        i = re.sub(r'\n</td>','',i)
        i = re.sub(r'</td>\n','',i)
        i = re.sub(r'<div class="modact">(.+?)</div>','\n\n *\\1* \n\n',i)
        i = re.sub(r'<a href="http(.+?)" target="_blank">(.+?)</a>','[\\2](http\\1)',i)
        i = re.sub(r'<img alt=\".*?\" border=\"\d+?\" smilieid=\"\d+?\" src=\"','[[[[img src="',i)
        i = re.sub(r'"/>','"/)',i)
        i = re.sub(r'<img .*?file="','[[[[img src="',i)
        i = re.sub(r'jpg".+\)','jpg" referrerpolicy="no-referrer"]]]]',i)
        i = re.sub(r'png".+\)','png" referrerpolicy="no-referrer"]]]]',i)
        i = re.sub(r'gif".+\)','gif" referrerpolicy="no-referrer"]]]]',i)
        i = re.sub(r'jpeg".+\)','jpeg" referrerpolicy="no-referrer"]]]]',i)
        i = re.sub(r'webp".+\)','webp" referrerpolicy="no-referrer"]]]]',i)
        i = re.sub(r'tif".+\)','tif" referrerpolicy="no-referrer"]]]]',i)
        i = re.sub(r'<.+?>','',i)
        i = re.sub(r'\n(.*?)\|(.*?)\|(.*?)\n','\n|\\1|\\2|\\3|\n',i)
        i = re.sub(r'收起\n理由','|昵称|战斗力|理由|\n|----|---|---|',i)
        i = re.sub(r'\|\n+?\|','|\n|',i)
        i = re.sub(r'\[\[\[\[','<',i)
        i = re.sub(r'\]\]\]\]','>',i)
        i = re.sub(r'\[(.+?发表于.+?\d)\]\((http.+?)\)','<a href="http\\2" target="_blank">\\1</a>',i)
        replys.append(i)
    for i in range(len(replylist)):
        if(lastreply < replynumber[i]):
            output = output + '\n\n*****\n\n' +'#### '+str(names[i]) + '\n##### '+str(times[i]) + '\n'+str(replys[i] ) +'\n'
    output = re.sub(r'\r','\n',output)
    output = re.sub(r'\n{4,}','\n\n\n', output)
    lastreply = replynumber[-1]
    return output,lastreply

cookie_str1 = os.getenv('S1_COOKIE')
cookie_str = repr(cookie_str1)[1:-1]
# #把cookie字符串处理成字典，以便接下来使用
cookies = {}
for line in cookie_str.split(';'):
    key, value = line.split('=', 1)
    cookies[key] = value
    # 设置请求头
headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
rootdir="./"           
with open(rootdir+'RefreshingData.json',"r",encoding='utf-8') as f:
    thdata=json.load(f)
async def UpdateThread(threaddict,headers,cookies):
    lastpage = threaddict['totalreply']//30
    async with aiohttp.ClientSession(headers=headers,cookies=cookies) as session:
        url = 'https://bbs.saraba1st.com/2b/thread-'+threaddict['id']+'-1-1.html'
        async with session.get(url,headers=headers,cookies=cookies) as response:
            result = await response.content.read()
        namelist, replylist,totalpage,newtitles= parse_html(result)
        if(thdata[threaddict['id']]['title'] =='待更新'):
            titles = newtitles
        #采取增量更新后仅第一次更新标题
        if((int(time.time()) - thdata[threaddict['id']]['lastedit']) > 1296000 or totalpage == 1):
            thdata[threaddict['id']]['active'] = False
            filedir = rootdir+thdata[threaddict['id']]['category']+'/'+str(threaddict['id'])+'【已归档】'+newtitles+'/'
            mkdir(filedir)
            with open((filedir+str(threaddict['id'])+'【已归档】.md').encode('utf-8'),'w',encoding='utf-8') as f:
                f.write('1')
        elif(totalpage >= lastpage):
            if(totalpage > 50):
                filedir = rootdir+thdata[threaddict['id']]['category']+'/'+str(threaddict['id'])+titles+'/'
                mkdir(filedir)
            else:
                filedir = rootdir+thdata[threaddict['id']]['category']+'/'
            #为了确保刚好有50页时能及时重新下载而不是直接跳至51页开始
            #startpage = (lastpage-1)//50*50+1
            ThreadContent = [' ']*50
            PageCount = 0
            # lastpages = '%02d' %math.ceil(lastpage/50)
            # remov(filedir+str(threaddict['id'])+titles+'-'+str(lastpages)+'.md')
            for thread in range(lastpage+1,totalpage+1):
                rurl = 'https://bbs.saraba1st.com/2b/thread-'+threaddict['id']+'-'+str(thread)+'-1.html'
                async with session.get(rurl,headers=headers,cookies=cookies) as response:
                    result = await response.content.read()
                namelist, replylist,totalpage,newtitles= parse_html(result)
                ThreadContent[PageCount],lastreply= FormatStr(namelist, replylist,threaddict['totalreply'])
                if(lastreply > threaddict['totalreply']):
                    PageCount = PageCount + 1
                    if(PageCount == 50 or thread == totalpage):
                        #lastsave=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()+28800))#把GithubAction服务器用的UTC时间转换为北京时间
                        #增量更新不再创建时间戳
                        pages = '%02d' %math.ceil(thread/50)
                        filename = str(threaddict['id'])+'-'+str(pages)+titles+'.md'
                        with open((filedir+filename).encode('utf-8'),'a',encoding='utf-8') as f:
                            f.writelines(ThreadContent)
                        ThreadContent = [' ']*50
                        PageCount = 0
                    thdata[threaddict['id']]['totalreply'] = lastreply
                    thdata[threaddict['id']]['lastedit'] = int(time.time())
                    thdata[threaddict['id']]['title'] = titles

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
    # # 浏览器登录后得到的cookie，也就是刚才复制的字符串
    '''
    下面的page为帖子号，默认从第一页开始下载
    '''
    tasks = []
    threaddicts = {}
    for tid in thdata.keys():
        if(thdata[tid]['active']):
            threaddicts[tid] = {}
            threaddicts[tid]['id'] = tid
            threaddicts[tid]['totalreply'] = int(thdata[tid]['totalreply'])
            threaddicts[tid]['title'] = thdata[tid]['title']
    for thread in threaddicts.keys():
        tasks.append(UpdateThread(threaddicts[thread],headers,cookies))
    asyncio.run(asyncio.gather(*tasks))
    with open(rootdir+'RefreshingData.json',"w",encoding='utf-8') as f:
        f.write(json.dumps(thdata,indent=2,ensure_ascii=False))