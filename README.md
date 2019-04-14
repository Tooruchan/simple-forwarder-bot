# Telegram Simple Forwarder Bot
一个简单的用于频道投稿与方便+86用户私聊的Telegram机器人
## 怎么部署
1. 在 [@botfather](https://t.me/botfather) 处申请一个bot的API Token
2. 在服务器上执行下列命令（请先安装git)
```
git clone https://github.com/Tooruchan/simple-forwarder-bot
pip install python-telegram-bot --upgrade
```
3. 打开config.json,将其中的Token字符串内容修改为你从BotFather获取到的Token,在admin里填入你的id(即用 [@userinfobot](https://t.me/userinfobot) 等bot获取到的id)
4. 使用 `python3 main.py` 运行bot  
** 切记，必须使用 Python 3 运行，否则一定报错。 **
5. 使用即可

## 使用开源协议
MIT

## 运行中的实例
[@tooru_post_bot](https://t.me/tooru_post_bot)
