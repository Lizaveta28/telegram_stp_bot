from apps.simple_user.functions import initial, show_sections_from_text, to_main_menu, show_sections_inline, \
    show_types_inline, comment_add, save_request, type_select_dialog, comment_add_dialog, show_my_requests, \
    print_request, send_to_chat, select_chat


class Router:
    @staticmethod
    def router_text(message, user, tb):
        if message.text.startswith('/r'):
            print_request(message, user, tb)
        elif user.state == 'initial':
            initial(message, user, tb)
        elif message.text == 'Отключиться от чата':
            to_main_menu(message, user, tb)
        elif user.state == 'chatting':
            send_to_chat(message, user, tb)
        elif user.state == 'message_enter':
            comment_add(message, user, tb)
        elif message.text == 'Создать заявку':
            show_sections_from_text(message, user, tb)
        elif message.text == 'В главное меню':
            to_main_menu(message, user, tb)
        elif message.text == 'Мои заявки':
            show_my_requests(message, user, tb)

    @staticmethod
    def route_inline(call, user, tb):
        if call.data.startswith('start_chat'):
            select_chat(call, user, tb)
        if call.data.startswith('show_requests'):
            pass
        if user.state == 'section_select':
            if call.data == 'section_change':
                show_sections_from_text(call, user, tb)
            else:
                show_sections_inline(call, user, tb)
        elif user.state == 'type_select':
            if call.data == 'section_change':
                show_sections_from_text(call, user, tb)
            elif call.data == 'type_change':
                type_select_dialog(call, user, tb)
            else:
                show_types_inline(call, user, tb)
        elif user.state == 'request_confirm':
            if call.data == 'save_request':
                save_request(call, user, tb)
            elif call.data == 'section_change':
                show_sections_from_text(call, user, tb)
            elif call.data == 'type_change':
                type_select_dialog(call, user, tb)
            elif call.data == 'comment_change':
                comment_add_dialog(call, user, tb)
