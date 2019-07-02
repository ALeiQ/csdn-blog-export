#!/usr/bin/env python2
# coding=utf-8

from bs4 import BeautifulSoup
import urllib2
import codecs
import re
import sys, getopt
# https://github.com/aaronsw/html2text
import html2text

# responsible for printing
class PrintLayer(object):
    """docstring for PrintLayer"""
    def __init__(self, arg):
        super(PrintLayer, self).__init__()
        self.arg = arg

    @staticmethod
    def printTotalPageNum(page):
        print "Total Page Number: " + str(page)

    @staticmethod
    def printWorkingPage(page):
        print "Work in Page " + str(page)

    @staticmethod
    def printWorkingArticle(article):
        print "Work in " + str(article)

    @staticmethod
    def printWorkingPhase(phase):
        if phase == 'getting-link':
            print "Phase 1: Getting the link"
        elif phase == 'export':
            print "Phase 2: Exporting"

    @staticmethod
    def printArticleCount(count):
        print 'Count of Articles: ' + str(count)

    @staticmethod
    def printOver():
        print 'All the posts has been downloaded. If there is any problem, feel free to file issues in https://github.com/gaocegege/csdn-blog-export/issues'


class Analyzer(object):
    """docstring for Analyzer"""
    def __init__(self):
        super(Analyzer, self).__init__()
    
    # get the page of the blog by url
    def get(self, url):
        headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
        req = urllib2.Request(url, headers=headers)
        print(url);
        html_doc = urllib2.urlopen(req).read()
        return html_doc

    # get the detail of the article
    def getContent(self, soup):
        return soup.find(id='mainBox').find('main')
        

class Exporter(Analyzer):
    """docstring for Exporter"""
    def __init__(self):
        super(Exporter, self).__init__()

    # get the title of the article
    def getTitleBox(self, detail):
        return detail.find(class_='article-header-box')

    def getTitleOnly(self, detail):
        return detail.find(class_='article-header-box').h1

    # get the content of the article
    def getArticleContent(self, detail):
        return detail.find('article')

    # export as markdown
    def export2markdown(self, f, detail):
        # if you need, open this line to get article_title for .md
        # f.write(html2text.html2text(self.getTitleOnly(detail).prettify()))
        f.write(html2text.html2text(self.getArticleContent(detail).prettify()))

    # export as html
    def export2html(self, f, detail):
        f.write(self.getTitleBox(detail).prettify())
        f.write(self.getArticleContent(detail).prettify())

    # export
    def export(self, link, filename, form):
        html_doc = self.get(link)
        soup = BeautifulSoup(html_doc)
        # detail = self.getContent(soup).find(class_='blog-content-box')
        if form == 'markdown':
            f = codecs.open(filename + '.md', 'w', encoding='utf-8')
            # self.export2markdown(f, detail)
            self.export2markdown(f, soup)
            f.close()
            return
        elif form == 'html':
            f = codecs.open(filename + '.html', 'w', encoding='utf-8')
            # self.export2html(f, detail)
            self.export2html(f, soup)
            f.close()
            return

    def run(self, link, f, form):
        self.export(link, f, form)
        

class Parser(Analyzer):
    """docstring for parser"""
    def __init__(self):
        super(Parser, self).__init__()
        self.article_list = []
        self.page = -1
        self.username = ""

    # get the articles' link
    def parse(self, html_doc):
        soup = BeautifulSoup(html_doc)
        res = self.getContent(soup).find(class_='article-list').find_all(class_='article-item-box')
        i = 0
        for ele in res:
            article_href = ele.find(class_='content').find('a', href=True)['href']
            if (article_href.strip().split('/')[3] != self.username): continue # expect other user's article, like ADS
            self.article_list.append(article_href)

    # get the page of the blog
    # may have a bug, because of the encoding
    def getPageNum(self, html_doc):
        soup = BeautifulSoup(html_doc)
        self.page = 1
        # papelist if a typo written by csdn front-end programmers?
        pattern = re.compile(r"var listTotal = (.*?);$", re.MULTILINE | re.DOTALL)
        script = soup.find('script', text=pattern)
        # if there is only a little posts in one blog, the papelist element doesn't even exist
        if script == None:
        	print "Page is 1"
        	return 1
        # get the page from text
        strpage = pattern.search(script.text).group(1).strip(' ')
        # compute pageNum by listTotal (20 per page)
        self.page = (int(strpage) + 19) / 20
        return self.page

    def getRealUserName(self, html_doc):
        soup = BeautifulSoup(html_doc)
        # papelist if a typo written by csdn front-end programmers?
        pattern = re.compile(r'var username = "(.*?)";$', re.MULTILINE | re.DOTALL)
        script = soup.find('script', text=pattern)
        # if there is only a little posts in one blog, the papelist element doesn't even exist
        if script == None:
        	print "Not Found username"
        	return None
        # get the username from text
        self.username = pattern.search(script.text).group(1).strip(' ')
        return self.username

    # get all the link
    def getAllArticleLink(self, url):
    	# get the num of the page
        self.getPageNum(self.get(url))
        PrintLayer.printTotalPageNum(self.page)
        # iterate all the pages
        for i in range(1, self.page + 1):
            PrintLayer.printWorkingPage(i)
            self.parse(self.get(url + '/article/list/' + str(i)))

    # export the article
    def export(self, form):
        PrintLayer.printArticleCount(len(self.article_list))
        for link in self.article_list:
            PrintLayer.printWorkingArticle(link)
            exporter = Exporter()
            exporter.run(link, link.split('/')[-1], form)

    # the page given
    def run(self, url, page=-1, form='markdown'):
        self.page = -1
        self.article_list = []
        self.getRealUserName(self.get(url))
        PrintLayer.printWorkingPhase('getting-link')
        if page == -1:
            self.getAllArticleLink(url)
        else:
            if page <= self.getPageNum(self.get(url)):
                self.parse(self.get(url + '/article/list/' + str(page)))
            else:
                print 'page overflow:-/'
                sys.exit(2)
        PrintLayer.printWorkingPhase('export')
        self.export(form)
        PrintLayer.printOver()
    

def main(argv):
    page = -1
    directory = '-1'
    username = 'default'
    form = 'markdown'
    try:
        opts, args = getopt.getopt(argv,"hu:f:p:o:")
    except Exception, e:
        print 'main.py -u <username> [-f <format>] [-p <page>] [-o <outputDirectory>]'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -u <username> [-f <format>] [-p <page>] [-o <outputDirectory>]'
            sys.exit()
        elif opt == '-u':
            username = arg
        elif opt == '-p':
            page = int(arg)
        elif opt == '-o':
            directory = arg
        elif opt == '-f':
            form = arg

    if username == 'default':
        print 'Err: Username err'
        sys.exit(2)
    if form != 'markdown' and form != 'html':
        print 'Err: format err'
        sys.exit(2)

    url = 'http://blog.csdn.net/' + username
    parser = Parser()
    parser.run(url, page, form)

if __name__ == "__main__":
   main(sys.argv[1:])
