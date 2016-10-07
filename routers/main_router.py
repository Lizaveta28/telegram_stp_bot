from apps.simple_user.state_machine import UserStateMachine
from apps.stp.state_machine import StpStateMachine
from apps.simple_user.router import Router as SimpleUserRouter
from apps.stp.router import Router as StpRouter


def text_router(message, user, tb):
    if user.state in UserStateMachine.states:
        SimpleUserRouter.router_text(message, user, tb)
    elif user.state in StpStateMachine.states:
        StpRouter.router_text(message, user, tb)


def inline_router(call, user, tb):
    if user.state in UserStateMachine.states:
        SimpleUserRouter.route_inline(call, user, tb)
    elif user.state in StpStateMachine.states:
        StpRouter.route_inline(call, user, tb)