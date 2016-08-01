# ibot
为命令行火车票查询器[iquery](https://github.com/wwj718/ibot)添加自然语言交互界面

---

![](http://oav6fgfj1.bkt.clouddn.com/ibot13761852.png)

ps：采用[asciinema](https://github.com/asciinema/asciinema)制作了[演示视频](https://asciinema.org/a/69utp9gpwal1y85lyv01kbhe2):

[![asciicast](https://asciinema.org/a/69utp9gpwal1y85lyv01kbhe2.png)](https://asciinema.org/a/69utp9gpwal1y85lyv01kbhe2)





# 安装
pip3 install ibot

在~/.ibot.yml里填写bosonnlp的token信息

# 使用
```
ibot 2016年8月十一号 南京到北京的车票
ibot 明天从南京到北京的车票
ibot 这周六从南京去北京出差，帮我看下车票
ibot 下周五离开南京去北京 查下车票
ibot 查一下上海去北京的车票，下周六
```

![](http://oav6fgfj1.bkt.clouddn.com/ibot13761852.png)

# 进展中
*  增加语音解析功能（基本完成）

# todo
*  把自然语言解析器抽象成通用工具
*  采用snownlp/TextBlob来解析自然语言
