from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

StoryTellerAgentStructure = {
    "title": "StoryTelling",
    "description": "Generate a ten-item list where each item is the page content in chronological order for the given chapter title in the historical figure's biography",
    "type": "object",
    "properties": {
        "chapters": {
            "type": "array",
            "description": "An array of ten items where each element is the appropriate and coherent page content corresponding to the chapter title in the historical figure's biography",
            "items": {
                "type": "string",
                "description": "chapter's story",
            },
        }
    },
    "required": ["chapters"],
}

StoryTellerPrompt = ChatPromptTemplate.from_template(
    """
    You are a story telling agent, you have a great historical background knowledge of Nigerian prominent figures. You have been hired by a children\'s story company. Your role is to generate the complete, rich and children-friendly content for the biography of any Nigerian historical figure they company provides you.

    Your response should be a list containing the complete story, each item being the corresponding chapter content for a given chapter title.

    Chapter titles \n {titles}
    """
)

StoryTellerAgent = StoryTellerPrompt | ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=1,
).with_structured_output(StoryTellerAgentStructure)
