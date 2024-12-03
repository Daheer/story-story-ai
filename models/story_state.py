from typing import Annotated, List, Dict, TypedDict
import operator

class StoryState(TypedDict):
    # input: List[str]
    historical_figure: str
    titles: List[str]
    chapters: List[str]
    prompts: List[str]
    images: List[str]
    publish: bool
