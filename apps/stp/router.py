from apps.stp.functions import initial


class Router:
    @staticmethod
    def router_text(message, user, tb):
        if user.state == 'stp_initial':
            initial(message, user, tb)

    @staticmethod
    def route_inline(call, user, tb):
        pass