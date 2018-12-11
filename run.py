# -*- mode: python3 -*-
from os import getenv

from backend import main

main.app.run(host="0.0.0.0", port=int(getenv("PORT", 5000)), workers=2)
