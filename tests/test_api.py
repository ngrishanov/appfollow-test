async def test_posts(test_cli):
    resp = await test_cli.get('/posts')

    assert resp.status == 200

    resp_json = await resp.json()

    assert resp_json['result']
