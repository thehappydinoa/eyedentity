from asyncio import sleep
from os import remove
from uuid import uuid4

from sanic import Sanic, response
from sanic_compress import Compress

from .s3 import ObjectList, upload_image
from .wordclouds import generate_wordcloud

wordclouds = ObjectList()

app = Sanic()
Compress(app)
app.static("/", "./dist")


async def add_sentences(sentences, key):
    wordcloud = generate_wordcloud(sentences)
    file = "wordclouds/" + key
    wordcloud.to_file(file)
    upload_image(file, key)
    remove(file)


@app.route("/")
async def index_path(request):
    return await response.file("dist/index.html")


@app.route("/status")
async def status_path(request):
    return await response.text("OK")


@app.route("/add_sentences", methods=["POST"])
def add_sentences_path(request):
    sentences = request.json.get("sentences")
    key = str(uuid4())[:8] + ".png"
    app.add_task(add_sentences(sentences, key))
    return response.json({"key": key})


@app.route("/wordclouds")
def wordclouds_path(request):
    return response.json({"wordclouds": wordclouds.return_objects()})


async def update_list(object_list=wordclouds):
    while True:
        await sleep(10)
        object_list.update()

app.add_task(update_list())
