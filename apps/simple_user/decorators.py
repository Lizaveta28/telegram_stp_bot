from apps.simple_user.state_machine import UserStateMachine
import functools


def is_user_active(**kwargs):
    def wrapper(tele_func):
        @functools.wraps(tele_func)
        def arguments_wrapper(*args, **kwargs):
            user = args[1]
            tb = args[2]
            if user and user.is_active:
                sm = UserStateMachine(data={'chat_id': user.telegram_chat_id,
                                            'tb': tb,
                                            'state': user.state,
                                            'user_id': user.id})
                obj = tele_func(*args, **kwargs, sm=sm)
            else:
                if user and not user.is_active:
                    tb.send_message(args[0].chat.id, "Кажется, ваш аккаунт деактивирован.")
                obj = None
            return obj
        return arguments_wrapper
    return wrapper
