from apps.stp.decorators import is_stp_active


@is_stp_active()
def initial(message, user, tb, sm):
    sm.greet()
    sm.main_menu()


@is_stp_active()
def to_main_menu(message, user, tb, sm):
    sm.main_menu()


@is_stp_active()
def show_requests_list(message, user, tb, sm):
    sm.requests_show(user=user)


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
    sm.start_chat(request=int(data[1]), user=user)


@is_stp_active()
def send_to_chat_text(message, user, tb, sm):
    sm.send_to_chat_text(user, message)