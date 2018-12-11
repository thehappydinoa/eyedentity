from asyncio import sleep
from os import remove
from uuid import uuid4

from sanic import Sanic, response
from sanic_compress import Compress

from .s3 import ObjectList, get_images, upload_image
from .wordclouds import generate_wordcloud

wordclouds = ObjectList()

app = Sanic()
Compress(app)
app.static("/", "./dist")


@app.route("/")
async def index_path(request):
    return await response.file("dist/index.html")


@app.route("/status")
async def status_path(request):
    return await response.text("OK")


@app.route("/add_sentences", methods=["POST"])
def add_sentences_path(request):
    key = str(uuid4())[:8] + ".png"
    wordcloud = generate_wordcloud(request.json.get("sentences"))
    file = "wordclouds/" + key
    wordcloud.to_file(file)
    upload_image(file, key)
    remove(file)
    return response.json({"key": key})


@app.route("/wordclouds")
def wordclouds_path(request):
    return response.json({"wordclouds": wordclouds.return_objects()})


async def update_list(object_list=wordclouds):
    while True:
        await sleep(10)
        object_list.update()

app.add_task(update_list())
