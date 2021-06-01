# [eyedentity](https://eyedentity.herokuapp.com/) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/6d574afb56ba444ba3dc72aa49e8ea84)](https://www.codacy.com/app/thehappydinoa/eyedentity?utm_source=github.com&utm_medium=referral&utm_content=thehappydinoa/eyedentity&utm_campaign=Badge_Grade)

![brain](https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/155/brain_1f9e0.png)

## Installation

You should make sure you have:

- at least `python3.5` with `poetry`
- `npm`
- globally installed `webpack`

Then type

```bash
poetry install
yarn install
yarn build
```

Use `yarn start` to run sanic server with react app.

## Notes

- Use `yarn clear` to clear the s3 bucket
- Use [`?interval=x`](https://eyedentity.herokuapp.com?interval=1) to set the update interval
