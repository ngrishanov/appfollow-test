from unittest import mock
import pathlib

from pypika import PostgreSQLQuery as Query, Order

from appfollow_test.storage.db import db, posts


resources = pathlib.Path(__file__).parent / 'resources'


def get_hn_page_mock(filename):
    def func_mock():
        with open(resources / filename) as f:
            return f.read()

    return func_mock


async def test_parser():
    from appfollow_test.hn_parser import parse_hn, start_db

    await start_db()

    with mock.patch(
        'appfollow_test.hn_parser._get_hn_page',
        mock.Mock(side_effect=get_hn_page_mock('hn1.html')),
    ):
        await parse_hn()

    post_list = await db.fetch(
        Query.from_(posts)
        .select(
            posts.id,
            posts.title,
            posts.url,
            posts.created,
        )
        .orderby(posts.id, order=Order.asc)
    )

    assert len(post_list) == 30

    assert post_list[0]['id'] == 21858305
    assert post_list[0]['title'] == 'Croydon Shut Down'
    assert post_list[0]['url'] == 'https://www.networkrail.co.uk/running-the-railway/our-regions/southern/disruption-at-victoria-and-london-bridge/'  # noqa


async def test_parser_multiple_updates():
    from appfollow_test.hn_parser import parse_hn, start_db

    await start_db()

    with mock.patch(
        'appfollow_test.hn_parser._get_hn_page',
        mock.Mock(side_effect=get_hn_page_mock('hn1.html')),
    ):
        await parse_hn()

    with mock.patch(
        'appfollow_test.hn_parser._get_hn_page',
        mock.Mock(side_effect=get_hn_page_mock('hn2.html')),
    ):
        await parse_hn()

    post_list = await db.fetch(
        Query.from_(posts)
        .select(
            posts.id,
            posts.title,
            posts.url,
            posts.created,
        )
        .orderby(posts.id, order=Order.asc)
    )

    assert len(post_list) == 31

    assert post_list[0]['id'] == 111
    assert post_list[0]['title'] == 'Test.com'
    assert post_list[0]['url'] == 'https://test.com'
