from dishka import Provider, Scope, provide_all

from app.api.v1.commands.ping import Ping


class FastAPICommandProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        Ping,
    )
