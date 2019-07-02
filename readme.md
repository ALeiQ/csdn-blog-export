# CSDN 博客导出工具

一个用python2.7写的博客导出工具，导出为markdown或者html。

## 使用

### 依赖
	
	Python 2.7
		beautifulsoup4

此外，在导出markdown格式的时候使用了开源项目[html2text](https://github.com/aaronsw/html2text)

### 使用方法
	
	main.py -u <username> [-f <format>] [-p <page>] [-o <outputDirectory>]
		<format>： html | markdown，缺省为markdown
		<page>为导出特定页面的文章，缺省导出所有文章
		<outputDirectory>暂不可用

### 拓展：for hexo

以下为hexo日志用户提供
使用main.py抓取html、md文件之后，通过postprocess_for_hexo.py可转换成hexo日志格式的md文件

    python postprocess_for_hexo.py
    postprocess_for_hexo.py文件中，mdPath表示md文件目录，htmlPath为html文件目录，outPath为转换后hexo的md文件目录

### Example

如果想导出[http://blog.csdn.net/cecesjtu](http://blog.csdn.net/cecesjtu)的文章，格式为markdown，命令为：

	./main.py -u cecesjtu -f markdown
	or
	./main.py -u cecesjtu

格式为html，命令为：

	./main.py -u cecesjtu -f html

转换为hexo日志格式，命令为：

    python postprocess_for_hexo.py


## To Do

1. 导出到指定目录

## Licence

GPLv3
