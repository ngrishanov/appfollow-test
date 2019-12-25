import pathlib


resources = pathlib.Path(__file__).parent / 'resources'


def get_hn_page_mock(filename):
    def func_mock():
        with open(resources / filename) as f:
            return f.read()

    return func_mock
