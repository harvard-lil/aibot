![Dall-E generated image of a logo with books inside a brain, and the text 'AbbyLarby'](abbylarby.svg)

AbbyLarby is a Slack bot for connecting to generative AI helpers.

Features
---

    /ai some prompt

Reply only to the user with the OpenAI text completion of "some prompt".

    /ai say some prompt

Reply to the channel with the OpenAI text completion of "some prompt".

Install locally
---

(lazy requirements for now)

    pip install requirements.txt

Copy .env.example to .env and write credentials.

Run dev server:

    watchmedo auto-restart python aibot.py

This uses sockets to talk to Slack, so dev bot will be live if you're using live credentials.

Server hosting
---

Same thing but with systemd to keep it running instead of watchmedo.