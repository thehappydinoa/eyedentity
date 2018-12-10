from uuid import uuid4

from sanic import Sanic, response

from .s3 import get_images, upload_image
from .wordclouds import generate_wordcloud

app = Sanic()

app.static("/", "./dist")


@app.route("/")
async def index(request):
    return await response.file("dist/index.html")


@app.route("/add_sentences", methods=["POST"])
def create_user(request):
    key = "_".join([request.json.get("username"), str(uuid4())[0:4]]) + ".png"
    wordcloud = generate_wordcloud(request.json.get("sentences"))
    wordcloud.to_file("wordclouds/" + key)
    upload_image(key)
    return response.json({"key": key})


@app.route("/wordclouds")
def wordclouds(request):
    return response.json({"wordclouds": get_images()})
