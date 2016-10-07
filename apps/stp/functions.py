from apps.stp.decorators import is_stp_active

@is_stp_active()
def initial(message, user, tb, sm):
    sm.greet()
    sm.main_menu()