import os
from typing import Literal
from langgraph.graph import StateGraph, START

from models.story_state import StoryState

from agents.planner_agent import PlannerAgent
from agents.storyteller_agent import StoryTellerAgent
from agents.illustrator_agent import IllustratorAgent
from agents.publisher_agent import PublisherAgent

from tools.image_generator import image_generator

from utils import supabase
import time


async def planner_node(state: StoryState):

    print("--- [Planner Agent] ---")
    time.sleep(30)
    planner_response = await PlannerAgent.ainvoke(
        {"historical_figure": state["historical_figure"]}
    )
    planner_response = planner_response[0]["args"]
    return {"titles": planner_response["titles"]}


async def storyteller_node(state: StoryState):
    print("--- [StoryTeller Agent] ---")
    time.sleep(30)
    storyteller_response = await StoryTellerAgent.ainvoke({"titles": state["titles"]})
    storyteller_response = storyteller_response[0]["args"]
    return {"chapters": storyteller_response["chapters"]}


async def illustrator_node(state: StoryState):
    print("--- [Illustrator Agent] ---")
    titles = state["titles"]
    chapters = state["chapters"]
    prompts = []
    for title, chapter in zip(titles, chapters):
        prompt = await IllustratorAgent.ainvoke(
            {
                "historical_figure": state["historical_figure"],
                "title": title,
                "chapter": chapter,
            }
        )
        time.sleep(30)
        prompt = prompt[0]["args"]
        prompt = prompt["prompt"]
        prompts.append(prompt)
    return {"prompts": prompts}


def publisher_node(state: StoryState):
    print("--- [Publisher Agent] ---")
    time.sleep(30)
    chapters = state["chapters"]
    images = state["images"]
    prompts = state["prompts"]
    historical_figure = state["historical_figure"]
    publish = []
    for chapter, image in zip(chapters, images):
        if image is not None:
            publisher_response = PublisherAgent.invoke(
                chapter=chapter,
                image=image,
                historical_figure=historical_figure,
            )
            time.sleep(30)
            publisher_response = publisher_response["publish"]
        else:
            publisher_response = False
        publish.append(publisher_response)
    print(f"--- [Story Score] = [{100*(publish.count(True)/len(publish))}%] ----")
    supabase.table("stories").upsert({"historical_figure": historical_figure}).execute()
    for i, (chapter, image, prompt) in enumerate(zip(chapters, images, prompts)):
        with open(image, "rb") as f:
            upload_response = supabase.storage.from_("illustrations").upload(
                file=f,
                path=f"public/{historical_figure.replace(' ', '-')}/image-{i+1}.png",
                file_options={"cache-control": "3600", "upsert": "true"},
            )
        illustration_url = supabase.storage.from_("illustrations").get_public_url(
            upload_response.path
        )
        supabase.table("story_pages").insert(
            {
                "page_number": i + 1,
                "historical_figure": historical_figure,
                "chapter": chapter,
                "illustration_url": illustration_url,
                "prompt": prompt,
            }
        ).execute()

    return {"publish": publish}


def generate_image(state: StoryState):
    print("--- [Image Creator] ---")
    images = []
    prompts = state["prompts"]
    for prompt in prompts:
        image = image_generator.run(prompt)
        images.append(image)
    return {
        "images": images,
    }


def should_end(state: StoryState) -> Literal["planner", "__end__"]:
    print("--- [End] ---")
    if state["publish"].count(True) >= 5:
        return "__end__"
    else:
        return "planner"


workflow = StateGraph(StoryState)

workflow.add_node("planner", planner_node)
workflow.add_node("storyteller", storyteller_node)
workflow.add_node("illustrator", illustrator_node)
workflow.add_node("image_generator", generate_image)
workflow.add_node("publisher", publisher_node)

workflow.add_edge(START, "planner")
workflow.add_edge("planner", "storyteller")
workflow.add_edge("storyteller", "illustrator")
workflow.add_edge("illustrator", "image_generator")
workflow.add_edge("image_generator", "publisher")

workflow.add_conditional_edges("publisher", should_end)

app = workflow.compile()
