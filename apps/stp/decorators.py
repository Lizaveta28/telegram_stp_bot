from apps.stp.state_machine import StpStateMachine
from models.models import Stp
import functools


def is_stp_active(**kwargs):
    def wrapper(tele_func):
        @functools.wraps(tele_func)
        def arguments_wrapper(*args, **kwargs):
            user = args[1]
            tb = args[2]
            if user and user.is_active and Stp.get(user=user).is_active:
                sm = StpStateMachine(data={'chat_id': user.telegram_chat_id,
                                           'tb': tb,
                                           'state': user.state,
                                           'user_id': user.id})
                obj = tele_func(*args, **kwargs, sm=sm)
            else:
                if user and not user.is_active:
                    tb.send_message(args[0].chat.id, "Кажется, ваш аккаунт деактивирован.")
                elif user.is_active and not Stp.get(user=user).is_active:
                    tb.send_message(args[0].chat.id,
                                    "Кажется вы больше не являетесь членом СТП.")
                obj = None
            return obj

        return arguments_wrapper

    return wrapper
