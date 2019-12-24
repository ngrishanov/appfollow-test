from sanic import response
from sanic import Sanic

app = Sanic()


@app.route('/posts', methods=['GET'])
async def get_posts(request):
    return response.json({
        'success': True,
    })


app.run(host='0.0.0.0', port=8000)
