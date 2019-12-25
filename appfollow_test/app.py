from sanic import response
from sanic import Sanic
from pypika import PostgreSQLQuery as Query, Order

from appfollow_test.storage.db import db, posts
from appfollow_test.utils import validate_args

app = Sanic()


@app.listener('before_server_start')
async def before_server_start(app, loop):
    del app, loop

    await db.start()


@app.listener('after_server_stop')
async def after_server_stop(app, loop):
    del app, loop
    await db.close()


@app.route('/posts', methods=['GET'])
@validate_args({
    'limit': {'type': 'int', 'min': 1, 'max': 100},
    'offset': {'type': 'int', 'min': 0, 'max': 100},
    'order': {'type': 'str', 'allowed_values': ['id', 'title', 'url', 'created']},
    'direction': {'type': 'str', 'allowed_values': ['asc', 'desc']},
})
async def get_posts(request):
    limit = int(request.args.get('limit', '10'))
    offset = int(request.args.get('offset', '0'))
    order = request.args.get('order')
    direction = request.args.get('direction', 'asc')

    q = (
        Query.from_(posts)
        .select(
            posts.id,
            posts.title,
            posts.url,
            posts.created,
        )
        .limit(limit)
        .offset(offset)
    )

    if order:
        q = q.orderby(order, order=Order[direction])

    result = await db.fetch(q)

    return response.json({
        'success': True,
        'result': result,
    })
