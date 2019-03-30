#-*- coding:utf-8 -*-
import json
import logging
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = None
dispatcher = None
config = dict()
Blacklist = []
Token = None
admin = None


def load_config():
    global config, Token, Blacklist, admin
    with open('config.json', encoding='utf-8') as f:
        config = json.load(f)
    Token = config['token']
    admin = config['admin']
    Blacklist = config['Blacklist']


def write_config():
    global config, Token, Blacklist, admin
    config['Blacklist'] = Blacklist
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)


def change_session(user):
    userid = user.id
    username = user.first_name
    return [[
        InlineKeyboardButton(
            '切换会话至' + username, callback_data='csession_' + str(userid))
    ]]


def change_session_id(user):
    return [[
        InlineKeyboardButton(
            '切换会话至' + str(user), callback_data='csession_' + str(user))
    ]]


def disconnect(user):
    return [[
        InlineKeyboardButton(
            '断开 ' + user + ' 的会话', callback_data='disconnect')
    ]]


def read_text_message(bot, update):
    global Blacklist, admin, session
    load_config()
    msg = update.message
    user = msg.from_user.id
    chat = msg.chat_id
    if user in Blacklist:
        bot.send_message(chat_id=chat, text='你不受欢迎。')
    elif user == admin:
        if msg.reply_to_message:
            reply_to = msg.reply_to_message.forward_from.id
        elif session:
            reply_to = int(session)
        bot.forward_message(reply_to, user, msg.message_id)
        bot.send_message(
            user, '回复至`' + session + '`成功。', parse_mode='Markdown')
    else:
        msg_fwded = bot.forward_message(admin, chat, msg.message_id)
        bot.send_message(user, '发送成功。', reply_to_message=msg.message_id)
        try:
            privacy_id = msg_fwded.forward_from_chat.id
        except AttributeError:
            bot.send_message(
                admin, '消息来自用户:\n`' + str(user) + '`', parse_mode='Markdown')
        else:
            if privacy_id == -1001228946795:
                bot.send_message(
                    admin,
                    '消息来自开启了转发策略的用户:\n`' + str(user) + '`',
                    reply_markup=InlineKeyboardMarkup(
                        change_session(msg.from_user)),
                    parse_mode='Markdown')


def answer_session(bot, update):
    global Blacklist, admin, session
    message = update.callback_query.message.message_id
    chat = update.callback_query.message.chat.id
    callback = update.callback_query
    callback_id = callback.id
    data = callback.data
    paras = data.split('_')
    if paras[0] == 'csession':
        session = paras[-1]
        bot.answer_callback_query(callback_id, '已经切换会话至用户ID号:' + session)
        bot.edit_message_text(
            '消息来自开启了转发策略的用户:\n`' + str(session) + '`',
            chat,
            message,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(disconnect(session)))
    elif data == 'disconnect':
        bot.answer_callback_query(callback_id, '已经断开用户ID号:' + session + '的会话')
        bot.edit_message_text(
            '消息来自开启了转发策略的用户:\n`' + str(session) + '`',
            chat,
            message,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(change_session_id(session)))
        session = 0


def ban_user(bot, update):
    global Blacklist, admin, session
    msg = update.message
    cmd = update.message.text
    user = update.message.from_user.id
    if user == admin:
        try:
            para = int(cmd.split()[1])
        except IndexError:
            if msg.reply_to_message:
                para = msg.reply_to_message.forward_from.id
                if para in Blacklist:
                    bot.send_message(
                        user,
                        '用户`' + str(para) + '`已位于黑名单中',
                        parse_mode='Markdown')
                elif para == admin:
                    bot.send_message(
                        user, 'Permission Denied.', parse_mode='Markdown')
                else:
                    try:
                        bot.send_message(
                            user,
                            '用户`' + str(para) + '`已经被封禁',
                            parse_mode='Markdown')
                    except TelegramError:
                        pass
                    finally:
                        Blacklist.append(para)
                        write_config()
            else:
                bot.send_message(chat_id=user, text='请指定要封禁用户的ID号!')
        except ValueError:
            bot.send_message(chat_id=user, text='请输入合法的数字!')
        else:
            if para in Blacklist:
                bot.send_message(
                    user,
                    '用户`' + str(para) + '`已位于黑名单中',
                    parse_mode='Markdown')
            elif para == admin:
                bot.send_message(
                    user, 'Permission Denied.', parse_mode='Markdown')
            else:
                try:
                    bot.send_message(
                        user,
                        '用户`' + str(para) + '`已经被封禁',
                        parse_mode='Markdown')
                except TelegramError:
                    pass
                finally:
                    Blacklist.append(para)
                    write_config()


def unban_user(bot, update):
    global Blacklist, admin
    cmd = update.message.text
    user = update.message.from_user.id
    if user == admin:
        try:
            para = int(cmd.split()[1])
        except IndexError:
            bot.send_message(chat_id=user, text='请指定要封禁用户的ID号!')
        except ValueError:
            bot.send_message(chat_id=user, text='请输入合法的数字!')
        else:
            if para in Blacklist:
                try:
                    bot.send_message(
                        user,
                        '用户`' + str(para) + '`已经解除封禁',
                        parse_mode='Markdown')
                except TelegramError:
                    pass
                Blacklist.remove(para)
                write_config()
            else:
                bot.send_message(
                    user,
                    '用户`' + str(para) + '`并不在黑名单里！',
                    parse_mode='Markdown')


def main():
    global dispatcher, updater, Token, Blacklist, admin
    load_config()
    updater = Updater(Token)
    dispatcher = updater.dispatcher
    fwd_text_handler = MessageHandler(Filters.all & (~Filters.command),
                                      read_text_message)
    ban_user_handler = CommandHandler('ban', ban_user)
    unban_user_handler = CommandHandler('unban', unban_user)
    callback_query_handler = CallbackQueryHandler(answer_session)
    dispatcher.add_handler(callback_query_handler)
    dispatcher.add_handler(fwd_text_handler)
    dispatcher.add_handler(ban_user_handler)
    dispatcher.add_handler(unban_user_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
