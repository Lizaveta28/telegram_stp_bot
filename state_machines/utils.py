from telebot import types
import smtplib
import config
from email.mime.text import MIMEText
from email.header import Header


def get_fio(person):
    return person['staff_surname'] + ' ' + person['staff_name'] + ' ' + person['staff_lastname']


def get_button(text):
    return types.KeyboardButton(text)


def get_button_inline(text, data):
    return types.InlineKeyboardButton(text=text, callback_data=data)


def generate_custom_keyboard(keyboard_class, buttons):
    # buttons = [[row_1_button_1, row_1_button_2],[row_2..]]
    if keyboard_class == types.ReplyKeyboardMarkup:
        markup = keyboard_class(resize_keyboard=True
        )
    else:
        markup = keyboard_class()
    for row in buttons:
        markup.row(*row)
    return markup


def send_email(header, text, recipients):
    if config.IS_PROD:
        recipients.append('nkotov@sdvor.com')
    else:
        recipients = ['nkotov@sdvor.com']
    with smtplib.SMTP(host=config.EMAIL_HOST, port=config.EMAIL_PORT) as s:
        msg = MIMEText(text, 'html', _charset='utf-8')
        msg['Subject'] = Header(header, "utf-8")
        s.sendmail(config.EMAIL_FROM, recipients, msg=msg.as_string())
