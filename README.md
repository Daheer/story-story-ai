# Story-Story: Once upon a time, Time-Time!

![](thumbnail.png)

**Story-Story** is an engaging storytelling app designed for children. It takes the rich histories of Nigerian and African figures and turns them into child-friendly, factual stories. With vibrant illustrations and captivating narratives, Story-Story aims to make history come alive for young minds. Stories are generated using an LLM agentic workflow, see demo [here](https://naija-heroes.vercel.app).

---

## 🌟 AI Agents Orchestration

**Story-Story** uses an ensemble of AI LLM agents implemented with **LangGraph** to generate entire 10-page stories about a hero from a single input (the hero's name).
Below is the architecture

![](arch.png)

## Agents Breakdown

1. Planner Agent
   - Responsible for generating the outline / chapter titles for the story
   - **input**: `historical_figure`
   - **output**: `chapter_title`
   - model: GPT-4o
2. Storyteller Agent (GPT-4o)
   - Responsible for generating accurate content for the chapter
   - **input**: `historical_figure` `chapter_title`
   - **output**: `chapter_content`
   - model: GPT-4o
3. Illustrator Agent
   - Responsible for generating prompts that will be used to generate images
   - **input**: `chapter_title` `historical_figure`
   - **output**: `prompt`
   - model: GPT-4o
4. Image Creator
   - Responsible for generating the illustrations given a prompt
   - **input**: `historical_figure` `prompt`
   - **outputs**: `image`
   - model: Flux.1 Schnell
5. Publisher Agent
   - Responsible for verifying validity of outputs, making sure it's okay for child consumption
   - **inputs**: `historical_figure` `chapter_content` `image`
   - **outputs**: `score`
   - model: GPT-4v

---

## 🚀 Getting Started
- Install requirements
```bash
pip install -r requirements.txt
```

- Add OpenAI API Key to environment
```bash
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"  
```

## Run app
```bash
python main.py --historical_figure "Ahmadu Bello"
```
This will create the `10-page` content including illustrations about Ahmadu Bello and upload to a `Supabase` database

