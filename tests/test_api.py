from unittest import mock

from tests.utils import get_hn_page_mock


async def test_posts(test_cli):
    from appfollow_test.hn_parser import parse_hn

    with mock.patch(
        'appfollow_test.hn_parser._get_hn_page',
        mock.Mock(side_effect=get_hn_page_mock('hn1.html')),
    ):
        await parse_hn()

    resp = await test_cli.get('/posts?limit=3&offset=1&order=title&direction=desc')

    assert resp.status == 200

    resp_json = await resp.json()
    result = resp_json['result']

    assert len(result) == 3

    assert result[0]['id'] == 21874523
    assert result[0]['title'] == 'What it\'s like to bootstrap a business before it can financially support you'
    assert result[0]['url'] == 'https://www.indiehackers.com/post/whats-it-like-to-bootstrap-a-business-before-it-can-financially-support-you-3472417e29'  # noqa


async def test_posts_invalid_params(test_cli):
    resp = await test_cli.get('/posts?limit=-1&offset=aaa&order=xyz&direction=yes')

    assert resp.status == 400

    resp_json = await resp.json()

    assert resp_json['errors'] == [
        {'field': 'limit', 'code': 'too_small', 'param': 1},
        {'field': 'offset', 'code': 'invalid_value'},
        {'field': 'order', 'code': 'not_allowed', 'param': ['id', 'title', 'url', 'created']},
        {'field': 'direction', 'code': 'not_allowed', 'param': ['asc', 'desc']}
    ]
