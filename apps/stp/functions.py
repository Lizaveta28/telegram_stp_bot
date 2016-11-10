from apps.stp.decorators import is_stp_active
from models.models import Stp


@is_stp_active()
def initial(message, user, tb, sm):
    sm.greet()
    sm.main_menu()


@is_stp_active()
def to_main_menu(message, user, tb, sm):
    sm.main_menu()


@is_stp_active()
def show_requests_list(message, user, tb, sm):
    custom_data = {'user': user, 'page': 0}
    sm._show_requests(None, custom_data={'user': user, 'page': 0})


@is_stp_active()
def show_requests_list_next(call, user, tb, sm):
    page = int(call.data.split(' ')[1])
    sm._show_requests(None, custom_data={'user': user, 'page': page})


@is_stp_active()
def print_request(message, user, tb, sm):
    sm.show_request(message.text[2:], user)


@is_stp_active()
def start_chat(call, user, tb, sm):
    data = call.data.split(' ')
    sm.start_chat(request=int(data[1]), user=user, message=call.message.message_id)


@is_stp_active()
def send_to_chat_text(message, user, tb, sm):
    sm.send_to_chat_text(user, message)


@is_stp_active()
def take_request(call, user, tb, sm):
    data = call.data.split(' ')
    sm.take_request(request=int(data[1]), user=user, call=call)


@is_stp_active()
def drop_request(call, user, tb, sm):
    data = call.data.split(' ')
    sm.drop_request(user=user, request=int(data[1]), call=call)


@is_stp_active()
def drop_request_choice(call, user, tb, decision, sm):
    data = call.data.split(' ')
    sm.drop_request_finally(call.message.message_id, int(data[1]), user, decision)
    sm.main_menu()

@is_stp_active()
def drop_request_comment(call, user, tb, sm):
    sm.drop_request_comment(user=user, request_id=call.data.split(' ')[1])

@is_stp_active()
def drop_request_with_comment(message, user, tb, sm):
    sm.drop_request_finally(message, None, user, 1, comment=message.text)
    sm.main_menu()

@is_stp_active()
def show_active_requests(message, user, tb, sm):
    sm._show_requests(None, custom_data={'user': user, 'page': 0, 'stp': Stp.get(user=user).id})

@is_stp_active()
def show_request_history(message, user, tb, sm):
    request = user.additional_data.get('chat')
    sm._show_request_history(request)


@is_stp_active()
def show_request_history_next(call, user, tb, sm):
    request = user.additional_data.get('chat')
    page = call.data.split(' ')[1]
    sm._show_request_history(request, int(page))