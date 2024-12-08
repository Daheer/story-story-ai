"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
import json


def upload_to_gemini(path, mime_type=None):
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


class PublisherAgentClass:
    def __init__(self, model_name) -> None:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        self.files = []
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            system_instruction="You are a publisher agent, you have a great historical background knowledge of Nigerian prominent figures. You have been hired by a children\\'s story company. Your role is to verify the correctness, coherence between the illustration image and the chapter. Also you verify that it is children friendly.\n\nYour response should be a boolean, True if the chapter is satisfactory and False otherwise",
        )

    def invoke(self, chapter, image, historical_figure):
        self.files = [
            upload_to_gemini(image, mime_type="image/webp"),
        ]
        chat_session = self.model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        self.files[0],
                    ],
                },
            ]
        )
        response = chat_session.send_message(
            f"""
            Chapter Text: {chapter} \n
            Historical Figure: {historical_figure}
            """
        )
        return json.loads(response.text)


PublisherAgent = PublisherAgentClass(model_name="gemini-1.5-flash")
