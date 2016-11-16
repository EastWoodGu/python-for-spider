 #!/usr/bin/python
 # -*- coding: utf-8 -*- #
# 豆瓣电影top250
import requests,sys,re,MySQLdb,time 
reload(sys)
sys.setdefaultencoding('utf-8')
print '正在从豆瓣电影Top250抓取数据......'
# --------------------------创建列表用于存放数据-----------------------------#
nameList=[]
linkList=[]
scoreList=[]
directorList=[]
playList=[]
yearList=[]
countryList=[]
commentList=[]
criticList=[]
#---------------------------------爬取模块------------------------------------#
def topMovie():
    for page in range(10):
        url='https://movie.douban.com/top250?start='+str(page*25)
        print '正在爬取第---'+str(page+1)+'---页......'
        html=requests.get(url)
        html.raise_for_status()
        try:
            contents=html.text # 返回网页内容，是字符串的形式
            # ---------------------------------匹配电影中文名------------------------------------#
            name=re.compile(r'<span class="title">(.*)</span>')
            names=re.findall(name,contents)
            for movieName in names:
                if movieName.find('/')==-1:
                    nameList.append(movieName)
            # ---------------------------------匹配电影链接------------------------------------#
            link=re.compile(r'a href="(.*)" class=""')
            links=re.findall(link,contents)
            for movieLink in links:
                linkList.append(movieLink)
            # ---------------------------------匹配电影评分------------------------------------#
            score=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
            scores=re.findall(score,contents)
            for movieScore in scores:
                scoreList.append(movieScore)
            # ---------------------------------匹配导演------------------------------------#
            director=re.compile(ur'导演: (.*)&nbsp;&nbsp;&nbsp;')
            directors=re.findall(director,contents)
            for movieDirector in directors:
                directorList.append(movieDirector)
            # ---------------------------------匹配主演------------------------------------#
            play=re.compile(u'主(.*?)<br>')
            plays=re.findall(play,contents)
            for moviePlay in plays:
                playList.append(moviePlay.strip(ur'演: '))
            # ---------------------------------匹配年份------------------------------------#
            year=re.compile(r'(\d\d\d\d)&nbsp;/&nbsp;')
            years=re.findall(year,contents)
            for movieyear in years:
                yearList.append(movieyear)
            # ---------------------------------匹配国家------------------------------------#
            country=re.compile(ur'&nbsp;/&nbsp;(.*)&nbsp;/&nbsp;')
            countries=re.findall(country,contents)
            for movieCountry in countries:
                countryList.append(movieCountry)
            # ---------------------------------匹配评价人数------------------------------------#
            commentor=re.compile(ur'<span>(.*)人评价</span>')
            commentors=re.findall(commentor,contents)
            for movieCommentor in commentors:
                commentList.append(movieCommentor)
            # ---------------------------------匹配简评------------------------------------#
            critic=re.compile(r'<span class="inq">(.*)</span>')
            critics=re.findall(critic,contents)
            for movieCritic in critics:
                criticList.append(movieCritic)

        except Exception as e:
            print e
    print '爬取完毕！'
    # ---------------------------------个别部分修改-----------------------------------#
    # 需要在第84部《大闹天空》不能通过上面的方法筛选，需要在83后加入加入数据
    yearList.insert(83, '1961(上集) / 1964(下集) / 1978(全本) / 2004(纪念版)')
    playList.insert(38,'...') # 某些电影没有主演和评论，这里用...代替
    playList.insert(233,'...')
    criticList.insert(134,'...')
    criticList.insert(156,'...')
    criticList.insert(176,'...')
    criticList.insert(180,'...')
    criticList.insert(196,'...')
    criticList.insert(230,'...')
    criticList.insert(232,'...')
    return nameList,linkList,scoreList,directorList,playList,yearList,countryList,commentList,criticList
# ---------------------------------储存到数据库-----------------------------------#
def save_to_MySQL():
    print 'MySQL数据库存储中......'
    try:
        conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="mysql", db="test", charset="utf8")
        cursor = conn.cursor()
        print "数据库连接成功"
        cursor.execute('Drop table if EXISTS MovieTop250') # 如果表存在就删除
        time.sleep(3)
        cursor.execute('''create table if not EXISTS MovieTop250(
                           编号 int not NULL auto_increment PRIMARY KEY ,
                           电影名称 VARCHAR (200),
                           链接 VARCHAR (200),
                           导演 VARCHAR (200),
                           主演 VARCHAR (200),
                           年份 VARCHAR (200),
                           国家 VARCHAR (200),
                           评价人数 VARCHAR (200),
                           简评 VARCHAR (200),
                           评分 VARCHAR (20))''')
        for i in range(250):
            sql='insert into MovieTop250(电影名称,链接,导演,主演,年份,国家,评价人数,简评,评分)' \
                ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            param=(nameList[i],linkList[i],directorList[i],playList[i],yearList[i],
                   countryList[i],commentList[i],criticList[i],scoreList[i])
            cursor.execute(sql,param)
            conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print e
    print 'MySQL数据库存储结束！'

# -------------------------------------主模块--------------------------------------#
if __name__=="__main__": # 相当于c语言中的main()函数
    try:
        topMovie()
        save_to_MySQL()
    except Exception as e:
        print e