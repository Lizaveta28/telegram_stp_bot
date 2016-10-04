from apps.simple_user.state_machine import UserStateMachine
from apps.simple_user.router import Router as SimpleuserRouter


def text_router(message, user, tb):
    if user.state in UserStateMachine.states:
        SimpleuserRouter.router_text(message, user, tb)


def inline_router(call, user, tb):
    if user.state in UserStateMachine.states:
        SimpleuserRouter.route_inline(call, user, tb)