from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Union, Any

import base64
from langchain.chains import TransformChain
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

def load_image(inputs: dict) -> dict:
    image_path = inputs["image_path"]
    
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    image_base64 = encode_image(image_path)
    return {"image": image_base64}

load_image_chain = TransformChain(
    input_variables=["image_path"], output_variables=["image"], transform=load_image
)

class PublisherAgentStructure(BaseModel):
    publish: bool = Field(
        ...,
        example=True,
        description="Set to True if the story is ready for publication and False otherwise.",
    )

def PublisherModel(inputs: dict) -> str | list[str | dict[Any, Any]]:
    model: ChatOpenAI = ChatOpenAI(
        temperature=0.5,
        model="gpt-4o",
        max_tokens=1024,
    )
    msg = model.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": f"""
                    You are a publisher agent, you have a great historical background knowledge of Nigerian prominent figures. You have been hired by a children\'s story company. Your role is to verify the correctness, coherence between the illustration image and the chapter. Also you verify that it is children friendly.

                    Your response should be a boolean, True if the chapter is satisfactory and False otherwise

                    Chapter Text: {inputs['chapter']}
                    Historical figure: {inputs['historical_figure']}
                    """},
                    {"type": "text", "text": parser.get_format_instructions()},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{inputs['image']}"
                        },
                    },
                ]
            )
        ]
    )
    return msg.content

parser = JsonOutputParser(pydantic_object=PublisherAgentStructure)

PublisherAgent = load_image_chain | PublisherModel
PublisherAgent = PublisherAgent.with_structured_output(PublisherAgentStructure)