#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import re
#解析博文HTML，获取博文时间、标题标签
from bs4 import BeautifulSoup
#解决中文编码问题
import codecs

mdPath = './test_md/'
htmlPath = './test_html/'
outPath = './test_out/'
"""
mdPath = './md/'
htmlPath = './html/'
outPath = './hexo_md/'
"""
mdPosts = os.listdir(mdPath)

for postName in mdPosts:
    if postName.endswith('.md'):
        #备份工具得到的文件名像这样：21049457.md，对当前文件夹中.md文件进行操作
        #获取文件名中8位数字，存于prefix中，用于匹配和它对应的HTML文件
        #然后从HTML文件中挖出博文发布时间，保存在timeStamp中
        prefix = postName.split('.')[0]
        print("processing file id: %s" %prefix)
        html = open(htmlPath + prefix + '.html', 'r')
        soup = BeautifulSoup(html)
        tag = soup.find_all('span', class_='time')
        timeStamp = tag[0].string.strip()
        print timeStamp

        #从HTML中获取博客标题，用于重命名.md文件
        title = soup.h1
        newFileName = title.string.strip()
        print newFileName

        #弃用！
        #.md文件中第一行大致长这样：#  [ Objective-C常用宏定义 ](/ichenwin/article/details/52813659)
        #方括号中就是博文名，下面这段代码负责从.md文件第一行获取文章名
        # mdFile = codecs.open(mdPath + postName, "r", 'utf-8')
        # contents = mdFile.readlines()
        # firstLine = contents.pop(0)
        # print "firstline:" + firstLine
        # newFileName = re.compile('\[([^]]+)\]').findall(firstLine)[0]
        # mdFile.close()

        #从HTML中获取博客tags
        tags = []
        tagsTag = soup.find('span', class_='artic-tag-box')
        if tagsTag:
            for tag in tagsTag.find_all('a'):
                tags.append(tag['data-track-click'].split('"')[-2])
        tags = ', '.join(tags)
        print(tags)

        #将.md中博文读入contents，往contents插入Hexo头部
        #然后写回.md文件
        mdFile = codecs.open(mdPath + postName, "r", 'utf-8')
        contents = mdFile.readlines()
        mdFile.close()
        contents.insert(0, "---\n")
        contents.insert(0, u"category: ACM\n")
        contents.insert(0, "tags: %s\n" %tags)
        contents.insert(0, "date: " + timeStamp + "\n")
        contents.insert(0, "title: " + newFileName + "\n")

        mdFile = codecs.open(outPath + postName, "w", 'utf-8')
        newContents = "".join(contents)
        mdFile.write(newContents)
        mdFile.close()

        html.close()

        #重命名.md文件
        #os.rename(os.path.join(mdPath, postName), os.path.join(mdPath, newFileName + ".md"))

"""
--------------------- 
作者：iChenwin 
来源：CSDN 
原文：https://blog.csdn.net/ichenwin/article/details/72851524 
版权声明：本文为博主原创文章，转载请附上博文链接！
"""
