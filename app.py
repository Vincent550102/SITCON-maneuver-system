from telegram.ext import Filters, Updater, CommandHandler, CallbackQueryHandler, MessageHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode

from dotenv import load_dotenv
import os
from text import *
import json
import prettytable


load_dotenv()

with open('config.json') as (jsonfile):
    config = json.load(jsonfile)


class TelegramBot():
    def __init__(self):
        TGBOT_TOKEN = os.getenv("TGBOT_TOKEN")
        self.updater = Updater(token=TGBOT_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.support_status = ['閒置中', '守門中', 'ogg']
        self.usernames = config['usernames']
        self.username2nickname = config['username2nickname']
        # self.dispatcher.add_handler(
        #     MessageHandler(
        #         Filters.document,
        #         self.trigger))
        # self.updater.dispatcher.add_handler(
        #     CallbackQueryHandler(self.start_convert))
        self.dispatcher.add_handler(CommandHandler('help', self.help))
        self.dispatcher.add_handler(CommandHandler('chstatus', self.chstatus))
        self.dispatcher.add_handler(CommandHandler('status', self.status))
        self.updater.dispatcher.add_handler(
            CallbackQueryHandler(self.chstatus_cb))
        self.updater.start_polling()
        self.updater.idle()

    def help(self, update, context):
        update.message.reply_text(text=help_text)

    def chstatus(self, update, context):
        # print(dir(update))
        # print(dir(context.bot.getChatMember(update.message.chat_id)))
        # print(context.bot.getChatMember(update.message.chat_id, update.message.from_user.id))
        # print(dir(update.message.from_user))
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
        # print(dir(update))
        update.callback_query.message.reply_text(
            f"讀到 {cbdata} 是從 {cbusername} 點的👍")
        # print(update.chat_member)
        # print(context.bot.username)
        # bot.getChatMember(update.message.chat_id)
        # update.message.reply_text(text=help_text)

    def status(self, update, context):
        table = prettytable.PrettyTable(['暱稱', '狀態'])
        table.align['暱稱'] = 'l'
        table.align['狀態'] = 'l'

        status_msg = status_msg_text
        tmp_sta = {
            "Vincent550102": "閒置中",
            "yc97463": "約會中"
        }
        for username in self.usernames:
            table.add_row([self.username2nickname[username],
                          tmp_sta[username]])
        # print(status_msg)
        update.message.reply_text(
            f'<pre>{table}</pre>', parse_mode=ParseMode.HTML)
    # def trigger(self, update, context):
    #     # writing to a custom file
    #     update.message.reply_text(text=recieve_text)
    #     file_name = update.message.document.file_name
    #     with open(f"temporary/{file_name}", 'wb') as f:
    #         context.bot.get_file(update.message.document).download(out=f)
    #     update.message.reply_text(text=convert_type_text, reply_markup=InlineKeyboardMarkup(
    #         [
    #             [
    #                 InlineKeyboardButton(
    #                     f'{support_format}', callback_data=f'{file_name}:{support_format}'
    #                 ) for support_format in self.support_formats
    #             ]
    #         ]
    #     )
    #     )

    # def start_convert(self, update, context):
    #     cbdata = update.callback_query.data
    #     file_name = cbdata.split(':')[0]
    #     convert_format = cbdata.split(':')[1]
    #     update.callback_query.message.reply_text(
    #         text=converting_text.format(convert_format))
    #     # create job
    #     job = self.convert.create_job(convert_format)
    #     # upload file
    #     self.convert.upload_file(job, file_name)
    #     # export file
    #     self.convert.export_file(job, file_name)

    #     doc_file = open(f"finished/{file_name}", "rb")
    #     update.callback_query.message.reply_document(
    #         quote="owo",
    #         document=doc_file,
    #         filename=f"{file_name}.{convert_format}",
    #     )


if __name__ == "__main__":
    telegrambot = TelegramBot()
    # telegrambot.run()
