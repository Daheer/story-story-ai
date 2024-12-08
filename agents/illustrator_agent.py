from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

IllustratorAgentStructure = {
    "title": "Illustration",
    "description": "Generate an appropriate prompt to generate an image for the given the chapter in the historical figure's biography",
    "type": "object",
    "properties": {
        "prompt": {
            "type": "string",
            "description": "Detailed prompt that will be sent to an image-generator",
        }
    },
    "required": ["prompt"],
}

IllustratorPrompt = ChatPromptTemplate.from_template(
    """
    You are an illustrator agent, you have a great historical background knowledge of Nigerian prominent figures. You have been hired by a children\'s story company. Your role is to generate prompts according to a chapter in the biography of any Nigerian historical figure they company provides you. The prompts will be passed to an image-generator.

    Your response should be carefully crafted detailed prompt, that will result in a children-friendly image.

    Historical figure: {historical_figure}
    Chapter title: {title}
    Chapter content: {chapter}
    """
)

IllustratorAgent = IllustratorPrompt | ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=1,
).with_structured_output(IllustratorAgentStructure)
