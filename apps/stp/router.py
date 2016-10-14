from apps.stp.functions import initial, to_main_menu, show_requests_list, show_requests_list_next,\
    print_request, start_chat, send_to_chat_text


class Router:
    @staticmethod
    def router_text(message, user, tb):
        if user.state == 'stp_initial':
            initial(message, user, tb)
        elif message.text == "В главное меню":
            to_main_menu(message, user, tb)
        elif message.text == "Список запросов":
            show_requests_list(message, user, tb)
        elif message.text.startswith('/r'):
            print_request(message, user, tb)
        elif message.text == "Отключиться от чата":
            to_main_menu(message, user, tb)
        elif user.state == 'stp_chatting':
            send_to_chat_text(message, user, tb)

    @staticmethod
    def route_inline(call, user, tb):
        if user.state == 'stp_requests_show':
            if call.data.startswith('stp_request_show'):
                show_requests_list_next(call, user, tb)
            if call.data.startswith('stp_request_take_and_chat'):
                start_chat(call, user, tb)