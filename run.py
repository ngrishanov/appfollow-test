import argparse
import os
import asyncio


class EnvDefault(argparse.Action):
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(
            default=default, required=required, **kwargs
        )

    def __call__(self, parser_, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'command',
        choices=[
            'run-http-server',
            'run-hn-parser',
        ],
        action=EnvDefault, envvar='ARG_COMMAND',
        help='Укажите команду для запуска (либо через переменную окружения ARG_COMMAND)',
    )

    args = parser.parse_args()

    if args.command == 'run-http-server':
        from appfollow_test.app import app
        app.run(host='0.0.0.0', port=8000)
    elif args.command == 'run-hn-parser':
        from appfollow_test.hn_parser import start

        loop = asyncio.get_event_loop()
        loop.run_until_complete(start())
    else:
        raise SystemError(f'Unknown command: {args.command!r}')
