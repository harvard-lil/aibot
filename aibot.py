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

    def show_prompt_response(text):
        respond(
            f"{text}" +
            ('\n_visible only to you_' if response_type == 'ephemeral' else ''),
            response_type=response_type)

    response_type = "ephemeral"
    prompt = command['text']
    if prompt.split(maxsplit=1)[0] == "say":
        response_type = "in_channel"
        prompt = prompt.split(maxsplit=1)[1]

    show_prompt_response(f"{command['user_name']} _/ai {command['text']}_\n{get_text(prompt)}")


if __name__ == "__main__":
    # Create an app-level token with connections:write scope
    handler = SocketModeHandler(app)
    handler.start()