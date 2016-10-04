import functools
from models.models import User


def request_process(**kwargs):
    def wrapper(tele_func):
        @functools.wraps(tele_func)
        def arguments_wrapper(*args, **kwargs):
            try:
                user = User.get(telegram_user_id=args[0].from_user.id)
                if user.username != args[0].from_user.username:
                    user.username = args[0].from_user.username
                    user.save()
            except Exception as e:
                user = User.create(username=args[0].from_user.username,
                                   telegram_chat_id=args[0].chat.id,
                                   # phone=args[0].contact.phone_number,
                                   telegram_user_id=args[0].from_user.id
                                   )

            obj = tele_func(*args, **kwargs, user=user)
            return obj
        return arguments_wrapper
    return wrapper