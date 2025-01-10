from quart import Quart, render_template, request, jsonify
from utils.helper import cocobox

app = Quart(__name__)

@app.route('/', methods=['GET', 'POST'])
async def index():
    if request.method == 'POST':
        video_urls = (await request.get_json())['video_urls']
        response = await cocobox(video_urls)
        return jsonify(
            response
        )
    return await render_template('index.html')

if __name__ == '__main__':
    app.run(port=5002)