import json
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
import re

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?">(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?">(.*?)</a>.*?star">(.*?)</p>'
                        +'.*?releasetime">(.*?)</p>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
         '排名':item[0],
         '图像':item[1],
         '标题':item[2],
         '演员':item[3],
         '上映时间':item[4]
        }

def write_to_file(content):
    with open('最受期待榜.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+ '\n')
        f.close()




def main(offset):
    url = 'http://maoyan.com/board/6?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(i*10)
    # pool = Pool()#这是设立的进程池,极大的加快了文件运行的速度
    # pool.map(main,[i*10 for i in range(10)])