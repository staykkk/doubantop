import requests,xlwt   #导入相关库，xlwt库用来写入到excel
from lxml import etree
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}
workbook=xlwt.Workbook(encoding='utf-8')
worksheet=workbook.add_sheet('书单1',cell_overwrite_ok=True)
worksheet1=workbook.add_sheet("书单2",cell_overwrite_ok=True)
worksheet2=workbook.add_sheet('评分9以上书单',cell_overwrite_ok=True)
worksheet.write(0,0,'书名')
worksheet.write(0,1,'作者')
worksheet.write(0,2,'评分')
worksheet.write(0,3,'评价人数')
worksheet2.write(0,0,'书名')
worksheet2.write(0,1,'作者')
worksheet2.write(0,2,'评分')
worksheet2.write(0,3,'评价人数')
worksheet1.write(0,0,'书名')
worksheet1.write(0,1,'作者')
worksheet1.write(0,2,'评分')
worksheet1.write(0,3,'评价人数')
list=[]  #空的列表 用来存放爬取到的所有书籍信息
row =1   #excel列表从第一行开始存入数据
list1=[]
list2=[]
def parse_url(url): #定义函数用来解析网页获取书籍信息
    res=requests.get(url,headers=headers).text
    html=etree.HTML(res)
    divs=html.xpath('//div[@class="doulist-item"]')
    for div in divs:
        dushu = {}
        title = div.xpath('.//div[@class="title"]/a/text()')
        if title:
            dushu['title'] = div.xpath('.//div[@class="title"]/a/text()')[0].strip()
        else:
            pass
        auth = div.xpath('.//div[@class="abstract"]/text()')
        if auth:
            dushu['auth'] = div.xpath('.//div[@class="abstract"]/text()')[0].strip()
        else:
            pass
        rating=div.xpath('.//div[@class="rating"]/span[2]/text()')
        if rating:
            dushu['rating']=div.xpath('.//div[@class="rating"]/span[2]/text()')[0].strip()
        else:
            pass
        comments=div.xpath('.//div[@class="rating"]/span[3]/text()')
        if comments:
            dushu['comments']=div.xpath('.//div[@class="rating"]/span[3]/text()')[0].strip()
        else :
            pass
        if dushu:
            dushu = dushu
            list.append(dushu)
def write_to_excel(list): #函数用来将数据写入到excel文件
    global row
    for lis in list:
        lie=0
        for k, v in lis.items():
            worksheet.write(row, lie, v)
            lie += 1
        row += 1

if __name__ == '__main__':
    for i in range(0, 21):
        print('开始爬取第{}页'.format(i+1))
        url = 'https://www.douban.com/doulist/45298673/?start={}'.format(i * 25)
        parse_url(url)
    print('爬取完毕一共{}本书籍 开始存入书单1文件'.format(len(list)))
    write_to_excel(list)
    for j in range(0,19):
        print('开始爬取第{}页'.format(k + 1))
        url = 'https://www.douban.com/doulist/49300014/?start={}'.format(j* 25)
    print('爬取完毕一共{}本书籍 开始存入书单2文件'.format(len(list1)))
    write_to_excel(list1)
    for k in range(0, 32):
        print('开始爬取第{}页'.format(k + 1))
        url = 'https://www.douban.com/doulist/1264675/?start={}'.format(k * 25)
    print('爬取完毕一共{}本书籍 开始存入评分9以上书单文件'.format(len(list2)))
    write_to_excel(list2)
    workbook.save('豆瓣读书top.xls')#数据全部存放后 保存到该文件里
    print('已全部存入表格当中，表格名称为：豆瓣读书top.xls')
