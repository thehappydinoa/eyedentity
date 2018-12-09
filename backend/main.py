import matplotlib
import numpy as np
from PIL import Image
from textblob import TextBlob
from wordcloud import STOPWORDS, WordCloud, get_single_color_func

from sanic import Sanic, response

matplotlib.use("TkAgg")


class PolarityColorFunc(object):
    def __init__(self, positive, neutral, negative):
        self.positive_func = get_single_color_func(positive)
        self.neutral_func = get_single_color_func(neutral)
        self.negative_func = get_single_color_func(negative)

    def get_color_func(self, word):
        analysis = TextBlob(word)
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            return self.positive_func
        if polarity < 0:
            return self.negative_func
        return self.neutral_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)


class AvatarWordCloud(WordCloud):
    def __init__(self, **kwargs):
        avatar_image = Image.open("avatar.png")
        avatar_mask = np.array(avatar_image)
        kwargs["mask"] = avatar_mask
        kwargs["mode"] = "RGBA"
        kwargs["background_color"] = (255, 0, 0, 0)  # "white"
        kwargs["color_func"] = PolarityColorFunc(
            "#7fbf7f", "#9999ff", "#ff8b94")  # ("green", "blue", "red")
        kwargs["width"], kwargs["height"] = avatar_image.size
        super(AvatarWordCloud, self).__init__(**kwargs)


def generate_wordcloud(text):
    if not isinstance(text, str):
        text = " ".join(text)
    wordcloud = AvatarWordCloud(
        contour_width=2, contour_color=(192, 192, 192, 85)).generate(text)
    return wordcloud.to_image()


app = Sanic()

app.static('/', './dist')


@app.route("/")
async def index(request):
    return await response.file('dist/index.html')


@app.route("/add_sentences", methods=["POST", ])
def create_user(request):
    img = generate_wordcloud(request.json.get("sentences"))
    return response.json({"submitted": True})
