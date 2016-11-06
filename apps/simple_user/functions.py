from apps.simple_user.decorators import is_user_active
from models.models import Section, Type


@is_user_active()
def initial(message, user, tb, sm):
    sm.greet()
    sm.main_menu()


@is_user_active()
def show_sections_from_text(message, user, tb, sm):
    sm.select_section()


@is_user_active()
def show_sections_inline(call, user, tb, sm):
    data = call.data
    data = data.split(' ')
    try:
        if data[0] == 'section_prev' or data[0] == 'section_next':
            data = {'page': int(data[1]), 'selected_section': data[2] if len(data) > 2 else None,
                    'message_id': call.message.message_id}
            sm._show_sections(None, custom_data=data)
        elif data[0] == 'section_up':
            section = Section.get(id=int(data[1]))
            if section:
                data = {
                    'selected_section':
                        section.parent_section if section.parent_section is None else section.parent_section.id,
                    'message_id': call.message.message_id}
                sm._show_sections(None, custom_data=data)
            else:
                tb.send_message(sm.chat, "Данная категория не является вложенной.")
        elif data[0] == 'section_select':
            section = Section.get(id=int(data[1]))
            if Section.select().where(Section.parent_section == section.id).count():
                data = {'selected_section': section.id,
                        'message_id': call.message.message_id}
                sm._show_sections(None, custom_data=data)
            else:
                sm.save_selected_section(int(data[1]), call.message.message_id)
                # tb.send_message(sm.chat, "Test")
                sm.select_type()
    except Exception as e:
        print(e)


@is_user_active()
def show_types_inline(call, user, tb, sm):
    data = call.data
    data = data.split(' ')
    try:
        if data[0] == 'type_prev' or data[0] == 'type_next':
            data = {'page': int(data[1]), 'selected_type': data[2] if len(data) > 2 else None,
                    'message_id': call.message.message_id}
            sm._show_types(None, custom_data=data)
        elif data[0] == 'type_up':
            ac_type = Type.get(id=int(data[1]))
            if ac_type:
                data = {
                    'selected_type':
                        ac_type.parent_type if ac_type.parent_type is None else ac_type.parent_type.id,
                    'message_id': call.message.message_id}
                sm._show_types(None, custom_data=data)
            else:
                tb.send_message(sm.chat, "Данная категория не является вложенной.")
        elif data[0] == 'type_select':
            ac_type = Type.get(id=int(data[1]))
            if Type.select().where(Type.parent_type == ac_type.id).count():
                data = {'selected_type': ac_type.id,
                        'message_id': call.message.message_id}
                sm._show_types(None, custom_data=data)
            else:
                sm.save_selected_type(int(data[1]), call.message.message_id)
                sel_type = Type.get(id=int(data[1]))
                if sel_type.comment_required:
                    sm.add_comment()
                else:
                    sm.confirm_request()
    except Exception as e:
        print(e)


@is_user_active()
def comment_add(message, user, tb, sm):
    sm._save_comment(message.text)
    sm.confirm_request()


@is_user_active()
def to_main_menu(message, user, tb, sm):
    sm.main_menu()


@is_user_active()
def save_request(call, user, tb, sm):
    sm.send_request(message_id=call.message.message_id, user=user)
    sm.main_menu()


@is_user_active()
def comment_add_dialog(call, user, tb, sm):
    sm.add_comment()


@is_user_active()
def type_select_dialog(call, user, tb, sm):
    sm.select_type()


@is_user_active()
def show_my_requests(message, user, tb, sm):
    sm.show_requests(user_id=user)


@is_user_active()
def print_request(message, user, tb, sm):
    sm.show_request(message.text[2:], user)


@is_user_active()
def send_to_chat(message, user, tb, sm):
    sm.send_to_chat(message.text, user)


@is_user_active()
def select_chat(call, user, tb, sm):
    chat = call.data.split(' ')[1]
    sm.select_chat(user=user, chat=chat, message=call.message.message_id)

@is_user_active()
def show_request_history(message, user, tb, sm):
    request = user.additional_data.get('chat')
    sm._show_request_history(request)

@is_user_active()
def show_request_history_next(call, user, tb, sm):
    request = user.additional_data.get('chat')
    page = call.data.split(' ')[1]
    sm._show_request_history(request, int(page))

@is_user_active()
def confirm_end_request(message, user, tb, sm):
    sm._confirm_end(user)

@is_user_active()
def end_request(call, user, tb, sm):
    sm.end_request(message=call.message.message_id)
    sm.main_menu()


@is_user_active()
def keep_request(call, user, tb, sm):
    sm._keep_request(message=call.message.message_id)


@is_user_active()
def end_request_inline(call, user, tb, sm):
    sm._end_request(None, custom_data={'message': call.message.message_id, 'request': int(call.data.split(' ')[1])})
    sm.main_menu()


@is_user_active()
def confirm_end_request_inline(call, user, tb, sm):
    sm._confirm_end(user, message=call.message.message_id, request=int(call.data.split(' ')[1]))