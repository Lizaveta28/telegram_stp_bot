def get_user_exclude_fields(prefix=""):
    exclude = '%sadditional_data', '%shas_messages_after_notification', '%sstate', '%stelegram_chat_id', '%stelegram_user_id'
    return [text % prefix for text in exclude]