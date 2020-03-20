from bs4 import BeautifulSoup as bs
import requests
import xlwt

workbook = xlwt.Workbook(encoding='utf-8') ## 创建一个workbook并且设置编码
worksheet = workbook.add_sheet('DouBanMovieTop250')#创建一个表格
worksheet.write(0,0,'电影排名')
worksheet.write(0,1,'电影名称')
worksheet.write(0,2,'别名')
worksheet.write(0,3,'导演')
worksheet.write(0,4,'评分')
worksheet.write(0,5,'简评')
row=1


def main(page):
    url='https://movie.douban.com/top250?start='+str(25*page)#网页url
    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    }
    print('第',page,'页')
    html=RequestsDouBanMovies(url,header)
    soup = bs(html,'html.parser')#利用bs库对html文件进行收集
    lists=soup.find('ol',class_="grid_view").find_all('div',class_='item')
    #print(lists)

    global row
    for each in lists:
        each_Movie_index=each.find('em' ,class_="").string
       # print(each_Movie_index)
        each_Movie_name=each.find('span' , class_='title').string 
        each_Movie_othername=(each.find('span', class_='other').string).replace('/','')
        each_Movie_director=each.find('p',class_='').get_text().split()[1]
        each_Movie_Score=each.find('span',class_='rating_num').string
        if each.find('span',class_='inq'):#只有本项记录存在空记录的情况
            each_Movie_Evaluate=each.find('span',class_='inq').string
        else:
            each_Movie_Evaluate='NULL'

        #将各项信息填入表格
        worksheet.write(row,0,each_Movie_index)
        worksheet.write(row,1,each_Movie_name)
        worksheet.write(row,2,each_Movie_othername)
        worksheet.write(row,3,each_Movie_director)
        worksheet.write(row,4,each_Movie_Score)
        worksheet.write(row,5,each_Movie_Evaluate)

        row=row+1

    print('读取完成')


def RequestsDouBanMovies(url,header):#用requests库获取网页信息
    try:
        data=requests.get(url,headers=header)
        if data.status_code==200:
            return data.text
    except requests.RequestException:
        return None



if __name__ == '__main__':
	for i in range(0,10):
		main(i)
	workbook.save('./result.xls')
    