from apps.stp.functions import initial, to_main_menu, show_requests_list, show_requests_list_next, \
    print_request, start_chat, send_to_chat_text, take_request, drop_request, drop_request_choice, \
    drop_request_comment, drop_request_with_comment, show_active_requests


class Router:
    @staticmethod
    def router_text(message, user, tb):
        if user.state == 'stp_initial':
            initial(message, user, tb)
        elif message.text == "В главное меню":
            to_main_menu(message, user, tb)
        elif user.state == 'stp_request_drop_comment':
            drop_request_with_comment(message, user, tb)
        elif message.text == "Список запросов":
            show_requests_list(message, user, tb)
        elif message.text == "Мои активные запросы":
            show_active_requests(message, user, tb)
        elif message.text.startswith('/r'):
            print_request(message, user, tb)
        elif message.text == "Отключиться от чата":
            to_main_menu(message, user, tb)
        elif user.state == 'stp_chatting':
            send_to_chat_text(message, user, tb)

    @staticmethod
    def route_inline(call, user, tb):
        if user.state == 'stp_request_drop':
            if call.data.startswith('stp_request_drop_yes'):
                drop_request_choice(call, user, tb, 1)
            elif call.data.startswith("stp_request_drop_no"):
                drop_request_choice(call, user, tb, 1)
            elif call.data.startswith("stp_request_drop_comment"):
                drop_request_comment(call, user, tb)
        else:
            if call.data.startswith('stp_request_show'):
                show_requests_list_next(call, user, tb)
            elif call.data.startswith('stp_request_take_and_chat') or call.data.startswith('stp_request_chat'):
                start_chat(call, user, tb)
            elif call.data.startswith('stp_request_take'):
                take_request(call, user, tb)
            elif call.data.startswith('stp_request_dismiss_request'):
                drop_request(call, user, tb)