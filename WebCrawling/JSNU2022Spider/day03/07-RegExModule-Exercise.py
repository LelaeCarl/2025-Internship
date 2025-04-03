import requests, re, os

# 模拟请求头信息
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

# 定义标题列表
titleList = []

'''1.搜索小说'''
def searchNovel(novel):
    # 1.1 定义请求地址
    searchURL = "http://www.xbiqugu.la/modules/article/waps.php"
    # 1.2 定义Post参数
    params = {
        "searchkey": novel
    }
    # 1.3 通过requests库发送请求
    searchResp = requests.post(url=searchURL,
                               data=params,
                               headers=headers)
    # 1.4 设置响应编码格式
    searchResp.encoding = "utf-8"
    # 1.5 获取小说搜索结果页面
    searchHtml = searchResp.text
    # 1.6 使用正则提取内容
    pattern = re.compile(
        "[a-z]{4}:\/\/[a-z]{3}\.[a-z]{7}\.[a-z]{2}\/\d+\/"
    )
    # 1.7 使用findall函数查找
    fd = pattern.findall(searchHtml)
    # 1.8 获取目录
    getHtml(fd[0])

'''2.读取小说目录并作内容'''
def getHtml(novelUrl):
    # http://www.xbiqugu.la/9/9419/
    # 2.1 发送请求
    mlResp = requests.get(url=novelUrl, headers=headers)
    # 2.2 设置编码
    mlResp.encoding = "utf-8"
    # 2.3 解析目录数据
    getMLData(mlResp.text)

'''3.清洗目录'''
def getMLData(html):
    # http://www.xbiqugu.la/9/9419/4177365.html
    # 3.1 查找需要的内容
    pattern = re.compile(
        r"\/\d+\/\d+\/\d+\.html")
    mlList = pattern.findall(html)
    # 3.2 循环获取每个章节地址
    for href in mlList:
        # 3.4 分析章节链接提取出内容
        getSection(href)

'''4.获取章节详情'''
def getSection(href):
    # http://www.xbiqugu.la
    url = "http://www.xbiqugu.la" + href
    sectionResp = requests.get(url=url, headers=headers)
    # 4.3 设置编码
    sectionResp.encoding = "utf-8"
    getSectionData(sectionResp.text)

'''5.章节清洗提取'''
def getSectionData(htmlL):
    # 5.1 正则查找标题
    pattern = re.compile(
        r"[a-z]{4}:\/\/[a-z]{3}\.[a-z]{7}\.[a-z]{2}\/\d+\/"
    )

    # 5.2 正则查找内容
    sea = pattern.search(htmlL)
    # 5.3 将标题添加至列表
    titleList.append(sea.group())
    nbsp_pattern = re.compile(
        r"[&nbsp;]{4}[\u4E00-\u9FA5、！!？“”，。]+"
    )

    # 5.4 将匹配结果变成章节内容
    content = []
    for line in htmlL:
        # 5.5 去除空格
        line = str(line).replace("bsp;", "")
        # 5.6 添加至章节
        content.append(line)
    # 5.7 写入章节
    saveData(content, sea.group())

'''6.保存结果'''
def saveData(content, title):
    # 6.1 创建文件
    file = open("%s.txt" % title, 'w', encoding="utf-8")
    file.write(content)
    file.close()
    print("写完了>>>", title)

if __name__ == "__main__":
    # 1.输入小说名字
    novel = input("请输入你想搜索的小说名字:")
    # 2.判断是否存在对应目录
    if novel not in os.listdir():
        os.mkdir(novel)
    # 3. 进入路径目录
    os.chdir(novel)
    # 4.调用
    searchNovel(novel)
    # getSection("/9/9419/4177365.html")
