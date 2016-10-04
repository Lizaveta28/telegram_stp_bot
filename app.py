import config
import telebot
from decorators.request import request_process
from routers.main_router import text_router, inline_router

tb = telebot.TeleBot(config.token)


@tb.message_handler(content_types=["text"])
@request_process()
def retrieve_by_fio(message, user):
    text_router(message, user, tb)
    
    
@tb.callback_query_handler(func=lambda call: True)
@request_process()
def query_text(query, user):
    inline_router(query, user, tb)
    

if __name__ == '__main__':
    tb.polling(none_stop=True)