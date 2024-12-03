import os
from typing import Literal
from langgraph.graph import StateGraph, START

from models.story_state import StoryState

from agents.planner_agent import PlannerAgent
from agents.storyteller_agent import StoryTellerAgent
from agents.illustrator_agent import IllustratorAgent
from agents.publisher_agent import PublisherAgent

from tools.image_generator import image_generator

async def planner_node(state: StoryState):

  print("--- [Planner Agent] ---")
  planner_response = await PlannerAgent.ainvoke({
    "historical_figure": state['historical_figure']
  })
  return {
    "titles": planner_response['titles']
  }

async def storyteller_node(state: StoryState):
  print("--- [StoryTeller Agent] ---")
  storyteller_response = await StoryTellerAgent.ainvoke({
    "titles": state['titles']
  })
  return {
    "chapters": storyteller_response['chapters']
  }

async def illustrator_node(state: StoryState):
  print("--- [Illustrator Agent] ---")
  titles = state['titles']
  chapters = state['chapters']
  prompts = []
  for title, chapter in zip(titles, chapters):
    prompt = await IllustratorAgent.ainvoke({
      "historical_figure": state['historical_figure'],
      "title": title,
      "chapter": chapter,
    })
    prompt = prompt['prompt']
    prompts.append(prompt)
  return {
    "prompts": prompts
  }

async def publisher_node(state: StoryState):
  print("--- [Publisher Agent] ---")
  chapters = state['chapters']
  images = state['images']
  publish = []
  for chapter, image in zip(chapters, images):
    publisher_response = await PublisherAgent.ainvoke({
      "image_path": image,
      "chapter": chapter,
      "historical_figure": state['historical_figure']
    })
    publisher_response = publisher_response['publish']
    publish.append(publisher_response)
  print("Final Publication", publish)
  breakpoint()
  return {
    "publish": publish
  }

def generate_image(state: StoryState):
  print("--- [Image Creator] ---")
  images = []
  prompts = state['prompts']
  for prompt in prompts:
    image = image_generator.run(prompt)
    images.append(image)
  return {
    "images": images,
  }

def should_end(state: StoryState) -> Literal["planner", "__end__"]:
    print("--- [End] ---")
    if state["publish"]:
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

