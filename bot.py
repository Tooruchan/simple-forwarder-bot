# -*- coding:utf-8 -*-

import telebot
from telebot import types
import json
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
if os.path.exists('./config.json'):
    if os.path.getsize('./config.json'):
        pass
    else:
        with open('./config.json', 'w') as write_default:
            default_config = dict(admin=[0], blacklist=[0], token='')
            json.dump(default_config, write_default)
            write_default.close()
else:
    with open('./config.json', 'w') as write_default:
        default_config = dict(admin=[0], blacklist=[0], token='')
        json.dump(default_config, write_default)
        write_default.close()

with open('./config.json', 'r+') as config_file:
    config = json.load(config_file)
    print('配置文件读取完成!内容如下:\n' + str(config))
    blacklist = config['blacklist']
    admin = config['admin']
    token = config['token']

bot = telebot.TeleBot(token)
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("投稿",callback_data=f"post"),InlineKeyboardButton("私聊",callback_data=f"message"))
    return markup
    @bot.callback_query_handler(func=lambda call:True)
    def callback_query(call):
        if call_data == '投稿':
            pass

try:
    chat_id = ''
    @bot.message_handler(commands=['start'])
    def welcome(message):
        bot.send_message(
            message.chat.id,
            '这是 @tooru_chan 制作的频道投稿机器人，直接向本机器人发送你要投稿的消息即可，但是spam将会被本机器人拉进黑名单。\n注意在没有提示转发成功的消息之前，管理员是看不见你的话的。')

    @bot.message_handler(commands=['help'])
    def help(message):
        bot.reply_to(
            message,
            '这是 @tooru_chan 制作的频道投稿机器人，直接向本机器人发送你要投稿的消息即可，但是spam将会被本机器人拉进黑名单。\n注意在没有提示转发成功的消息之前，管理员是看不见你的话的。')

    @bot.message_handler(commands=['info'])
    def show_info(message):
        if message.chat.username is None and message.chat.last_name is None:
            bot.reply_to(
                message, '您的名字:' + message.chat.first_name + '\n您的ID:' + str(
                    message.chat.id))
        elif message.chat.last_name is None:
            bot.reply_to(
                message, '您的username: @' + message.chat.username + '\n您的名字:' +
                message.chat.first_name + '\n您的ID:' + str(message.chat.id))
        elif message.chat.username is None:
            bot.reply_to(
                message, '您的名字:' + message.chat.first_name + '\n您的姓氏:' +
                message.chat.last_name + '\n您的ID:' + str(message.chat.id))
        else:
            bot.reply_to(
                message, '您的username: @' + message.chat.username + '\n您的名字:' +
                message.chat.first_name + '\n您的姓氏:' + message.chat.last_name +
                '\n您的ID:' + str(message.chat.id))

    @bot.message_handler(commands=['ban'])
    def ban_user(message):
        if message.chat.id in admin:
            try:
                user_id = message.text.split()[1]
                if int(user_id) in blacklist or int(user_id) in admin:
                    raise ValueError
                elif user_id.isdigit():
                    pass
                else:
                    raise IndexError
            except IndexError:
                bot.reply_to(message, '指令格式不正确。\n用法:/ban [用户ID]')
            except ValueError:
                bot.reply_to(message, '当前用户已位于黑名单中!')
            else:
                blacklist.append(int(user_id))
                with open('./config.json', 'w+') as write_config:
                    now_config = dict(
                        blacklist=blacklist, admin=admin, token=token)
                    json.dump(now_config, write_config)
                    write_config.close()
                    bot.reply_to(message,
                                '已经将用户 ' + str(user_id) + ' 加入本机器人的黑名单中。')
        else:
            pass

    @bot.message_handler(commands=['unban'])
    def unban_user(message):
        if message.chat.id in admin:
            try:
                user_id = message.text.split()[1]
                id_index = blacklist.index(int(user_id))
                if user_id.isdigit():
                    pass
                else:
                    raise IndexError
            except IndexError:
                bot.reply_to(message, '指令格式不正确。\n用法:/unban [用户ID]')
            except ValueError:
                bot.reply_to(message, '当前用户并不在黑名单中!')
            else:
                blacklist.pop(id_index)
                with open('./config.json', 'w+') as write_config:
                    now_config = dict(
                        blacklist=blacklist, admin=admin, token=token)
                    json.dump(now_config, write_config)
                    write_config.close()
                    bot.reply_to(message, '已经将用户 ' + str(user_id) + ' 从黑名单中删去。')
        else:
            pass

    @bot.message_handler(commands=['reply'])
    def reply_to_messages(message):
        global chat_id
        if message.chat.id in admin:
            try:
                user_id = message.text.split()[1]
                if user_id.isdigit():
                    pass
                else:
                    raise IndexError
            except IndexError:
                bot.reply_to(message, '消息格式错误，\n 指令用法:/reply [要切换到的会话用户ID]')
            else:
                if user_id == chat_id:
                    pass
                else:
                    if chat_id:
                        bot.send_message(int(chat_id),'管理员已经断开与您的会话。')
                    chat_id = user_id
                    bot.send_message(
                        int(user_id), '管理员已切换会话至您。', parse_mode='Markdown')
                    bot.reply_to(message, '切换会话成功,当前会话为:ID:[' + str(chat_id) + '](tg://user?id=' + str(
                                chat_id) + ')\n', parse_mode='Markdown')
                
        else:
            pass

    @bot.message_handler(commands=['cancel'])
    def cancel_current_chat(message):
        global chat_id
        if message.chat.id in admin:
            if chat_id:
                bot.send_message(int(chat_id),'管理员已经断开与您的会话。')
                chat_id = ''
                bot.reply_to(message,'已退出当前会话。')
            else:
                bot.reply_to(message,'当前并没有会话，不如用 /reply 命令手动切换一个？')

    @bot.message_handler(content_types=[
        'text', 'audio', 'photo', 'sticker', 'document', 'video', 'video_note',
        'voice'
    ])
    def check(message):
        global chat_id
        if message.chat.type in ['group', 'channel', 'supergroup']:
            pass
        else:
            if message.chat.id in blacklist:
                bot.reply_to(message, '你已经被本机器人拉黑。')
            else:
                if message.chat.id in admin:
                    if not chat_id:
                        bot.send_message(message.chat.id,'当前并没有会话，不如用 /reply 命令手动切换一个？')
                    else:
                        if message.text is None:
                            bot.send_message(message.chat.id,'请不要发送除了文本之外的内容!')
                        bot.send_message(int(chat_id),'回复:\n'+message.text)
                        bot.send_message(message.chat.id,'回复成功')
                else:
                    if not chat_id:
                        bot.send_message(message.chat.id,'管理员当前并没有会话，正在为您切换...')
                        chat_id = str(message.chat.id)
                        for i in range(0, len(admin)):
                            bot.send_message(admin[i],'已自动连接到用户 `'+ chat_id +'` 的会话上。',
                            parse_mode='Markdown')
                            bot.send_message(
                                admin[i],
                                '消息来自:ID:`' + str(message.chat.id) + '`\n [' +
                                message.chat.first_name + '](tg://user?id=' + str(
                                    message.chat.id) + ')\n' + '/reply',
                                parse_mode='Markdown')
                            bot.forward_message(admin[i], message.chat.id,
                                                message.message_id)
                        bot.reply_to(message, '这条消息已经成功被转发了。')
                    else:
                        bot.send_message(message.chat.id,'管理员当前正在会话中，请等待管理员看到您的消息。在没有提示已成功转发的时候是看不见您的消息的。')
                        for i in range(0, len(admin)):
                            bot.send_message(
                                admin[i],
                                '消息来自:ID:`' + str(message.chat.id) + '`\n [' +
                                message.chat.first_name + '](tg://user?id=' + str(
                                    message.chat.id) + ')\n' + '/reply',
                                parse_mode='Markdown')
                            bot.forward_message(admin[i], message.chat.id,
                                                message.message_id)
                        bot.reply_to(message, '这条消息已经成功被转发了。')
                    # print(str(message.text))
    bot.polling(none_stop=True)
except KeyboardInterrupt:
    quit()
except Exception as e:
    print(str(e))
    
