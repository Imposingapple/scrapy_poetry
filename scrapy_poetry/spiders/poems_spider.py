import scrapy
import re
import requests
from lxml import etree

class QuotesSpider(scrapy.Spider):
    name = "poems"

    def start_requests(self):
        urls = [
            'https://so.gushiwen.cn/shiwenv_1443f4f57a9d.aspx',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_poems)

    def parse_poems(self, response):
        my_poem = response.css('div.main3 div.left div.sons')[0]
        my_yishang = response.css('div.main3 div.left')
        zhushi_block = None
        background_block = None
        blocks = my_yishang.css('div.contyishang').getall()
        for i in range(len(blocks)):
            if "创作背景" in blocks[i]:
                background_block = blocks[i]
            if "注释" in blocks[i]:
                zhushi_block = blocks[i]

        def process_text(str):
            str = remove_tags(str.strip())
            str = remove_chinese_space(str)
            str = ''.join(str.split())
            return str

        def remove_tags(str):
            reg = re.compile('<[^>]*>')
            return ''.join(reg.sub('', str).strip().split()).strip('创作背景')

        def remove_chinese_space(str):
            reg = '[ 　]*'
            return re.sub(reg, '', str)

        def get_note_id(str_list):
            str = ''.join(str_list)
            id = re.findall(r"fanyiShow\(.+?\)", str)[0].split('\'')[1]
            return id

        def get_notes():
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
                'Cookie': "login=flase; Hm_lvt_9007fab6814e892d3020a64454da5a55=1612059150,1612148583,1612157633,1612163867; codeyzgswso=22d635072dd3029c; gsw2017user=540751%7c435FF88BA10A9DA831CF6CC54D30218C; login=flase; wxopenid=defoaltid; gswZhanghao=13701970825; gswPhone=13701970825; Hm_lpvt_9007fab6814e892d3020a64454da5a55=1612165231"
            }
            if zhushi_block is None:
                return '', '无注释'
            elif "展开阅读" not in zhushi_block:
                notes_list = zhushi_block.split('注释')[-1].split('<br>')
                notes = []
                for note in notes_list:
                    reg = re.compile('<[^>]*>')
                    note = reg.sub('', note).strip()
                    if len(note) == 0:
                        continue
                    if '注释' in note:
                        note = note.strip('注释').strip()
                    notes.append(note)
                return '', notes
            else:
                # id = get_note_id(my_yishang.css("div.contyishang div a").getall())
                id = get_note_id([zhushi_block])
                url = "https://so.gushiwen.cn/nocdn/ajaxfanyi.aspx?id={}".format(id)
                response = requests.get(url, headers=headers)
                html = etree.HTML(response.text)
                if "未登录" in response.text:
                    my_text = "未登录"
                else:
                    my_text = html.xpath('//div[@class="contyishang"]/p[last()]/text()')
                return url, my_text

        def get_background_id(background_block):
            id = re.findall(r"shangxiShow\(.+?\)", background_block)[0].split('\'')[1]
            # print("id: ",id)
            return id

        def get_background():
            background = ''

            if background_block is None:
                return ''
            elif "展开阅读" in background_block:
                id = get_background_id(background_block)
                url = "https://so.gushiwen.cn/nocdn/ajaxshangxi.aspx?id={}".format(id)
                response = requests.get(url)
                html = etree.HTML(response.text)
                # print("######################################################")
                # print("url: ",url)
                # print("html: ", html)
                # print("response.text: ",response.text)
                background_text = html.xpath('//div[@class="contyishang"]/p/text()')
                background = process_text(''.join(background_text))
                return background
            else:
                background = process_text(''.join(background_block))
                return background

        def extract_with_css(query):
            print(re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", my_poem.css(query).get(default='').strip()))
            return re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", my_poem.css(query).get(default='').strip())

        def get_paragragh():
            if len(my_poem.css('div.contson p').getall()) == 0:
                paragraphs = my_poem.css('div.contson::text').getall()
            else:
                paragraphs = my_poem.css('div.contson p::text').getall()

            new_paragraphs = []
            for p in paragraphs:
                new_paragraphs.append(remove_chinese_space(p))  # 去除中文全角空格
            paragraph = '\t'.join(new_paragraphs)
            return re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", paragraph.strip())

        yield {
            'title': extract_with_css('div.cont h1::text'),
            'author': extract_with_css('p.source a::text'),
            'paragraphs': get_paragragh(),
            # 'notes_url: ': get_notes()[0],
            'notes': get_notes()[1],
            'background': get_background(),
        }
