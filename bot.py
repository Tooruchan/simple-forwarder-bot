#-*- coding:utf-8 -*-

import telebot
import json
import os

if os.path.exists('./config.json'):
    if os.path.getsize('./config.json'):
        pass
    else:
        with open('./config.json','w') as write_default:
            default_config = dict(admin=[0],blacklist=[0],token='')
            json.dump(default_config,write_default)
            write_default.close()
else:
    with open('./config.json','w') as write_default:
        default_config = dict(admin=[0],blacklist=[0],token='')
        json.dump(default_config,write_default)
        write_default.close()

with open('./config.json','r+') as config_file:
    config = json.load(config_file)
    print('配置文件读取完成!内容如下:'+str(config))
    blacklist = config['blacklist']
    admin = config['admin']
    token = config['token']

bot = telebot.TeleBot(token)
while(1):
    try:
        @bot.message_handler(commands = ['start'])
        def welcome(message):
            bot.reply_to(message,'这是 @tooru_chan 制作的频道投稿机器人，直接向本机器人发送你要投稿的消息即可，但是spam将会被本机器人拉进黑名单。')

        @bot.message_handler(commands = ['help'])
        def help(message):
            bot.reply_to(message,'这是 @tooru_chan 制作的频道投稿机器人，直接向本机器人发送你要投稿的消息即可，但是spam将会被本机器人拉进黑名单。')

        @bot.message_handler(commands = ['info'])
        def show_info(message):
            if message.chat.username is None:
                bot.reply_to(message,'您的名字:'+message.chat.first_name+'\n您的姓氏:'+message.chat.last_name+'\n您的ID:'+str(message.chat.id))
            else:
                bot.reply_to(message,'您的username: @'+message.chat.username+'\n您的名字:'+message.chat.first_name+'\n您的姓氏:'+message.chat.last_name+'\n您的ID:'+str(message.chat.id))

        @bot.message_handler(commands = ['ban'])
        def ban_user(message):
            if message.chat.id in admin:
                try:
                    user_id = message.text.split()[1]
                    if int(user_id) in blacklist or int(user_id) in admin:
                        raise ValueError
                except IndexError:
                    bot.reply_to(message,'将用户加入到黑名单的过程出错了')
                except ValueError:
                    bot.reply_to(message,'当前用户已位于黑名单中!')
                else:
                    blacklist.append(int(user_id))
                    with open('./config.json','w+') as write_config:
                        now_config = dict(blacklist=blacklist,admin=admin,token=token)
                        json.dump(now_config,write_config)
                        now_config.close()
                        bot.reply_to(message,'已经将用户'+user_id+'加入本机器人的黑名单中。')
            else:
                pass

        @bot.message_handler(commands = ['unban'])
        def unban_user(message):
            if message.chat.id in admin:
                try:
                    user_id = message.text.split()[1]
                    id_index = blacklist.index(int(user_id))
                except IndexError:
                    bot.reply_to(message,'指令格式不正确。')
                except ValueError:
                    bot.reply_to(message,'当前用户并不在黑名单中!')
                else:
                    blacklist.pop(id_index)
                    with open('./config.json','w+') as write_config:
                        now_config = dict(blacklist=blacklist,admin=admin,token=token)
                        json.dump(now_config,write_config)
                        now_config.close()
                        bot.reply_to(message+'已经将用户'+user_id+'从黑名单中删去')   
            else:
                pass        
        @bot.message_handler(commands =['reply'])
        def reply_to_messages(message):
            if message.chat.id in admin:
                try:
                    user_id = message.text.split()[1]
                    text = message.text.split()[2]
                except IndexError:
                    bot.reply_to(message,'消息格式错误')
                else:
                    bot.send_message(int(user_id),'回复:\n'+text,parse_mode='Markdown')
                    bot.reply_to(message,'消息已经成功被转发。')
            else:
                pass
        @bot.message_handler(content_types=['text','audio','photo','sticker'])
        def check(message):
            if message.chat.type in ['group','channel','supergroup']:
                pass
            else:
                if message.chat.id in blacklist:
                    bot.reply_to(message,'你已经被本机器人拉黑，请勿再发送消息。')
                else:
                    if message.chat.id in admin:
                        pass
                    else:
                        for i in range(0,len(admin)):
                            bot.send_message(admin[i],'消息来自:ID:`'+str(message.chat.id)+ '`\n ['+message.chat.first_name+'](tg://user?id='+str(message.chat.id)+')\n'+'/reply' ,parse_mode='Markdown')
                            bot.forward_message(admin[i],message.chat.id,message.message_id)
                            bot.reply_to(message,'这条消息已经成功被转发了。')
                            # print(str(message.text))
        bot.polling()
    except KeyboardInterrupt:
        quit()
    except Exception as e:
        print(str(e))
