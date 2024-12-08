"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
import json

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file


# Create the model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_schema": content.Schema(
        type=content.Type.OBJECT,
        properties={
            "publish": content.Schema(
                type=content.Type.BOOLEAN,
            ),
        },
    ),
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are a publisher agent, you have a great historical background knowledge of Nigerian prominent figures. You have been hired by a children\\'s story company. Your role is to verify the correctness, coherence between the illustration image and the chapter. Also you verify that it is children friendly.\n\nYour response should be a boolean, True if the chapter is satisfactory and False otherwise",
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
    upload_to_gemini(
        "/tmp/gradio/7de17a06f5bc7e38e7638628b7341cbfa99e9c1d93e10256b7a07cdb7f10618c/image.webp",
        mime_type="image/webp",
    ),
]

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                files[0],
            ],
        },
    ]
)

response = chat_session.send_message("Who are you")

print(response.text)
print(type(response.text))
print(json.loads(response.text)["publish"])
