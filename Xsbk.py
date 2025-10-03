import requests
from lxml import etree
from urllib.parse import urljoin
import time
#小说首页地址例如url为:www.zhangsan.com
base_url = 'www.zhangsan.com'
#小说页地址例如url为:www.zhangsan.com//books/4395/.html
url = 'www.zhangsan.com//books/4395/1.html'

chapter_count = 0
while True:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        print(f"爬取第 {chapter_count + 1} 章: {url}")
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'

        e = etree.HTML(r.text)

        # 提取内容
        #小说banner位置
        info = ''.join(e.xpath(' '))
        #小说title位置
        title_list = e.xpath(' ')
        title = title_list[0] if title_list else "无标题"

        print(f"标题: {title}")

        # 保存到文件
        #在这里是保存小说的文档名称例如小说名为：张三李四
        with open('张三李四.txt', 'a', encoding='utf-8') as f:
            f.write(f"{title}\n\n{info}\n\n{'=' * 60}\n\n")

        # 获取下一页链接
        #小说next位置
        next_links = e.xpath(' ')
        if not next_links:
            print("没有下一页了")
            break

        next_url_rel = next_links[0]
        #url拼接判断例如小说下一章url为“www.zhangsan.com//books/4395/2.html”
        if next_url_rel == '/books/4395/' or next_url_rel == url:
            print("爬取完成")
            break

        # 拼接完整URL - 这里是关键修正
        url = urljoin(base_url, next_url_rel)

        chapter_count += 1
        time.sleep(1)

    except Exception as e:
        print(f"错误: {e}")
        break

print(f"完成! 共爬取 {chapter_count} 章")