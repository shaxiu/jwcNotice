# 导入包
import requests,bs4,json

#获取小程序云开发token
def access_token():
    APPID = 'APPID'  # 小程序ID
    APPSECRET = 'APPSECRET'  # 小程序秘钥
    WECHAT_URL = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + \
        APPID + '&secret=' + APPSECRET
    response = requests.get(WECHAT_URL)
    result = response.json()
    print(result)
    return result["access_token"]  # 将返回值解析获取access_token

#添加数据
def databaseAdd(access_token, temp_data):
    url = 'https://api.weixin.qq.com/tcb/databaseadd?access_token=' + access_token
    # print(temp_data)
    data = {
        "env": "lyy-production",
        "query":'''db.collection(\"weNjtech-jwcNotice\").add({
            data:[%s]
            })'''%temp_data
    }

    response = requests.post(url, data=json.dumps(data))
    result = response.json()
    print(result)  # 将返回值打印

#工具函数（处理链接标志）
def delFlag(temp_content):                                          
    # print(content)
    # print(content[0])
    href_link=temp_content.find('a')['href']
    href_link=href_link.split('/')
    temp='http://jwc.njtech.edu.cn'+'/'+href_link[-3]+'/'+href_link[-2]+'/'+href_link[-1]
    # print(temp)
    href_group.append(temp)
    href_num=href_link[-1].split('.')[0]
    return href_num

#爬取界面代码
def get_html(url):
    res = requests.get(url)  # 发送请求，获得网页数据
    res.encoding = 'utf-8'  # 改变编码格式
    web_content = res.text  # 获得网页内容
    soup = bs4.BeautifulSoup(web_content, 'html.parser')
    #获取标题，时间，内容
    title = soup.find_all('div', class_='title')[1].get_text()
    time = soup.find('div', class_='time').get_text()[-10:]
    content = str(soup.find('div', class_='v_news_content'))
    #格式化需要传送的html代码
    content=content.replace("\"","\\\"")
    content=content.replace('\n','').replace('\r','')
    href_link=url.split('/')
    id=href_num=href_link[-1].split('.')[0]
    temp_data={
        "_id":id,
        "title":title,
        "pubDate":time,
        "content":content
    }
    temp_data=json.dumps(temp_data)
    return temp_data

#main
res=requests.get('http://jwc.njtech.edu.cn/index/tzgg.htm')         #发送请求，获得网页数据
res.encoding = 'utf-8'                                              #改变编码格式
web_content=res.text                                                #获得网页内容
soup = bs4.BeautifulSoup(web_content,'html.parser')                 #造汤

filename='/root/script/weNjtech_jwcNotice.txt'
f = open(filename,"r")                                              #设置文件对象
temp_str = f.read()                                                      #将txt文件的所有内容读入到字符串temp_str中
f.close()                                                           #将文件关闭
latest_flag=temp_str                                                     #上次发送的最新通知号

href_flag=[]                                                        #标志号数组
tosend_content=[]                                                   #待发送内容
href_group=[]

#获取所需元素，加入数组
a=0                                                                 
for i in soup.find('div',class_='txt').children:
    if a == 2:
        content=i.select('li')
    a=a+1

for item in content:                                                #获取标志数组
    href_flag.append(delFlag(item))

for i, j in enumerate(href_flag):
    if int(j)>int(latest_flag):
        tosend_content.append(content[i])

# print(href_group)
if(tosend_content !=''):
    #获取token
    token = access_token()
    for i,j in enumerate(tosend_content):
        data=get_html(href_group[i])
        databaseAdd(token, data)
    print("success")

file=open(filename, 'w')
if tosend_content !='':
    latest_flag=href_flag[0]
    file.write(latest_flag)
    file.close()
