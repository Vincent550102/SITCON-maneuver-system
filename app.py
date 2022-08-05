from telegram.ext import Filters, Updater, CommandHandler, CallbackQueryHandler, MessageHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from database.database import Database
from dotenv import load_dotenv
import os
from text import *
import json
import prettytable

load_dotenv()

with open('config.json', 'rb') as (jsonfile):
    config = json.load(jsonfile)


class TelegramBot():
    def __init__(self):
        TGBOT_TOKEN = os.getenv("TGBOT_TOKEN")
        self.updater = Updater(token=TGBOT_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.support_status = config['support_status']
        self.usernames = config['usernames']
        self.username2nickname = config['username2nickname']
        self.admin = config['admin']
        self.database = Database()
        self.dispatcher.add_handler(CommandHandler('help', self.help))
        self.dispatcher.add_handler(CommandHandler('chstatus', self.chstatus))
        self.dispatcher.add_handler(CommandHandler('status', self.status))
        self.dispatcher.add_handler(
            CommandHandler('superinit', self.superinit))
        self.updater.dispatcher.add_handler(
            CallbackQueryHandler(self.chstatus_cb))

    def help(self, update, context):
        update.message.reply_text(text=help_text)

    def chstatus(self, update, context):
        if update.message.from_user.username not in self.usernames:
            update.message.reply_text(
                text='請聯絡管理員 @Vincent550102 加上你的 username')
            return
        update.message.reply_text(
            text=get_status_text, reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f'{support_status}', callback_data=f'{update.message.from_user.username}:{support_status}'
                        ) for support_status in self.support_status
                    ]
                ]
            )
        )

    def chstatus_cb(self, update, context):
        cbusername, cbdata = update.callback_query.data.split(":")
        prev_status = self.database.get_status_by_username(cbusername)
        self.database.update_status_by_username(cbusername, cbdata)
        update.callback_query.message.reply_text(
            text=change_status_text.format(cbusername, prev_status, cbdata))

    def status(self, update, context):
        table = prettytable.PrettyTable(['暱稱', '狀態'])
        table.align['暱稱'] = 'l'
        table.align['狀態'] = 'l'

        all_status = self.database.get_all_status()
        for status in all_status:
            if status[0] not in self.username2nickname:
                update.message.reply_text(
                    text=f'請 {status[0]} 聯絡管理員 @Vincent550102 加上你的 nickname')
            table.add_row([self.username2nickname[status[0]], status[1]])
        update.message.reply_text(
            f'<pre>{table}</pre>', parse_mode=ParseMode.HTML)

    def superinit(self, update, context):
        if update.message.from_user.username in self.admin:
            self.database.init_status()
            update.message.reply_text(text='初始化完成')
        else:
            update.message.reply_text(text='權限不足')

    def run(self):
        self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    telegrambot = TelegramBot()
    telegrambot.run()
