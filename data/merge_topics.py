"""
    本文件将‘宋词-按主题分类’的词进行整理组合
    同一首词只会出现一次，'topic'属性将是这首词所有相关的topic的列表
    同时我们将'notes'属性中的拼音注解给删去，例如：我(wo)：xxx --> 我：xxx
"""

import os
import json
import re

path_to_jsonfiles = '宋词-按主题分类'
ci_dict = {}
title_list = []
n_background = 0
for file in os.listdir(path_to_jsonfiles):
    full_filename = "%s/%s" % (path_to_jsonfiles, file)
    print(full_filename)
    with open(full_filename,'r',encoding='utf-8') as fi:
        l = json.load(fi)
        for ci in l:
            if ci['title'] not in title_list:
                title_list.append(ci['title'])
                ci_new = ci
                new_note = []
                ci_new['topic'] = [ci_new['topic']]
                for note in ci_new['notes']:
                    reg = re.compile('[（(].*[）)]')
                    new_note.append(reg.sub('', note).strip())

                ci_new['notes'] = new_note
                ci_dict[ci['title']] = ci_new
                if len(ci['background']) >= 1:
                    n_background += 1
            else:
                ci_dict[ci['title']]['topic'].append(ci['topic'])


ci_list = list(ci_dict.values())
print("宋词总数：", len(ci_list))
print("含创作背景的宋词数：", n_background)
jsObj = json.dumps(ci_list, indent=4, ensure_ascii=False)  # indent参数是换行和缩进
fileObject = open('宋词-主题，注释，背景.json', 'w', encoding='utf-8')
fileObject.write(jsObj)
fileObject.close()  # 最终写入的json文件格式: