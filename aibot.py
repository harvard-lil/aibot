import json
import os
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import openai
from dotenv import load_dotenv


# setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
load_dotenv()
app = App()
openai.api_key = os.getenv('OPENAI_API_KEY')
OPENAI_PARAMS = {
    'model': "text-davinci-003",
    'temperature': 0.7,
    'max_tokens': 150,
    'top_p': 1,
    'frequency_penalty': 0,
    'presence_penalty': 0,
    # 'stop': ['Bot:', 'You:'],
}

def get_text(prompt):
    openai_response_obj = openai.Completion.create(**OPENAI_PARAMS, prompt=prompt)
    logger.debug(f"OpenAI response: {openai_response_obj}")
    return openai_response_obj.choices[0].text.strip().strip('"')

@app.command("/ai")
def ai(ack, respond, command):
    logger.debug(command)
    ack()

    response_type = "ephemeral"
    prompt = command['text']
    if prompt.split(maxsplit=1)[0] == "say":
        response_type = "in_channel"
        prompt = prompt.split(maxsplit=1)[1]

    formatted_prompt = f"{command['user_name']} asked: /ai {command['text']}"
    response = get_text(prompt)

    respond(
        formatted_prompt,
        response_type=response_type,
        attachments=[
            {
                "text": response,
                "callback_id": "public_repost",
                "color": "#3AA3E3",
                "actions": [
                    {
                        "name": "say",
                        "text": "Post publicly",
                        "type": "button",
                        "value": json.dumps({"prompt": formatted_prompt, "response": response}),
                    },
                ],
            }
        ]
    )

@app.action("public_repost")
def public_repost(ack, payload, respond, say):
    ack()
    to_repost = json.loads(payload['value'])
    respond(text='', replace_original=True, delete_original=True)
    say(to_repost["prompt"], response_type="in_channel", attachments=[
        {
            "text": to_repost["response"],
            "color": "#3AA3E3",
        }
    ])

if __name__ == "__main__":
    handler = SocketModeHandler(app)
    handler.start()