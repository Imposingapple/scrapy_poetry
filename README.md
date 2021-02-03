# scrapy_poetry
### 项目介绍

本项目使用**scrapy框架**对**古诗文网**进行爬虫，获取古诗文网推荐页**不同分类**（例如：怀古，爱情，友情等）的所有**词**的**标题、作者、注释、创作背景**。我对爬取的数据做了处理，目测**去除了所有奇怪的符号、序号和空格**，保持每首词格式的统一，这里总共收录2178首词，其中1302首包括创作背景。

此外，本项目提供了将不同分类的词整理到一起（不按分类）的代码和整理好的数据，示例可以 参考下图：

![示例](https://github.com/Imposingapple/scrapy_poetry/blob/main/img/example.png)

**非常欢迎大家的使用，喜欢的朋友点个star哈！**


----------------------------------------------------------------------------------------------------------
### 使用方法

要预测任何一个分类的诗词（例如：爱情）：

1. 打开list_spider.py，将文件最开始的start_requests函数中，'爱情'相应的url注释去掉，并给其他分类的url加上注释
2. 将list_spider.py文件最后的yield中的'topic'键的值改成'爱情'
3. 打开terminal切换到根目录，输入：scrapy crawl list -O ./data/爱情.json



要将你获取的各个分类的json整合到一起（使得一首诗词只出现一次，并且'topic'是所有该诗词标签的list）：

直接运行./data/merge_topics.py


----------------------------------------------------------------------------------------------------------
### 备注：

1. 本项目的代码和跑完代码后得到的json**只包括词**，主要是宋词，不是宋朝的词也有。该项目可以简单修改为爬取古诗文网不同分类的所有诗词（很简单，把判断标题是不是词牌的判断去掉就好），因为本人的需要，只爬取了宋词。
2. 我爬取的时候**没有爬翻译和赏析**，是因为这两者都是更带有阅读者的主观色彩，从西方阐释学的角度，或许是诗词的一种“衍生义”，个人目前做的NLP项目中，我想了想好像并没有哪里需要。
3. 古诗文网的译文、注释和创作背景如果有'展开阅读全文'的，都是用javascript加载的，这里如果不用cookie的话经常会出现顺着js给出的id去get这个url时返回'未登录'的情况，这里我是自己注册登陆后，将我自己的cookie写进header去get相应的url，如果我的cookie不行的话，请自行注册登陆，并把你们的cookie写到list_spider.py中get_notes()函数里的header里。
4. 如果要修改本项目的代码，非常建议先自学一下scrapy，直接看官网教程即可。
5. 如果有同时在做诗歌NLP的同志，欢迎加微信交流，我的微信：ImposingApple


