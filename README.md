# Telegram Simple Forwarder Bot
一个简单的用于频道投稿与方便+86用户私聊的Telegram机器人
## 怎么部署
1. 在 [@botfather](https://t.me/botfather) 处申请一个bot的API Token
2. 在服务器上执行下列命令（请先安装git)
```
git clone https://github.com/Tooruchan/simple-forwarder-bot
pip3 install PyTelegramBotAPI==2.2.3
pip3 install telebot
```
3. 打开config.json,将其中的Token字符串内容修改为你从BotFather获取到的Token,在admin这个list里加入你的id(即用@userinfobot等bot获取到的id)
4. 使用 `python3 bot.py` 运行bot
5. 打开你在BotFather申请到的bot的聊天界面（需要使用一次/start）

## 使用开源协议
MIT

## 运行中的实例
[@tooru_post_bot](https://t.me/tooru_post_bot)
