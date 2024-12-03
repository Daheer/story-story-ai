from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Union

PlannerAgentStructure = {
    "title": "OutlineGenerate",
    "description": "Generate a list of ten chapter titles in chronological order for the given historical figure\'s biography",
    "type": "object",
    "properties": {
        "titles": {
            "type": "array",
            "description": "An array of ten items where each element is an appropriate and significant chapter in the historical figure\'s biography",
            "items": {
                "type": "string",
                "description": "chapter title",
            }
        }
    },
    "required": ["titles"]
}

PlannerPrompt = ChatPromptTemplate.from_template(
    """
    You are a story planner agent, you have a great historical background knowledge of Nigerian prominent figures including the milestones of their lives. You have been hired by a children\'s story company. Your role is to generate an outline for the biography of any Nigerian historical figure they company provides you.

    Your response should be a list containing the outline, each item being the title of a chapter in a chronological order, this will be used to generate the children-friendly content for the biography.
    
    Historical figure: {historical_figure}
    """
)

PlannerAgent = PlannerPrompt | ChatOpenAI(
    model="gpt-4o", temperature=0
).with_structured_output(PlannerAgentStructure)