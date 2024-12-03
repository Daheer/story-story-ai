from typing import Optional, Any, Dict, Type

from langchain_core.callbacks import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain_core.pydantic_v1 import Field, SecretStr, BaseModel
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env

class ImageGenerationInput(BaseModel):
    query: str = Field(description="user query")

class ImageGenerationTool(BaseTool):

  """
  Image Generation Tool
  This tool uses FLUX.1 Schnell to generate images. It uses the HuggingFace Space API to interact with the model
  """

  name: str = "image_generation_tool"
  """Name of the tool."""
  description: str = "this tool can be used to generate images from a users prompt"
  """Description of the tool."""

  args_schema: Type[BaseModel] = ImageGenerationInput 

  def __init__(
      self,
      **kwargs: Any
  ) -> None:

    super().__init__(**kwargs)
    try:
        from gradio_client import Client
    except ImportError:
        raise ImportError(
            "Gradio Client is not installed. "
            "Please install it with `pip install gradio_client`"
        )

  def _generate_image(self, prompt="Story-Story: Once upon a time, Time-Time!"):

    try:

        from gradio_client import Client
        client = Client("ChristianHappy/FLUX.1-schnell")
        result = client.predict(
                prompt=prompt,
                seed=0,
                randomize_seed=True,
                width=1024,
                height=1024,
                num_inference_steps=4,
                api_name="/infer"
        )

        return result[0]
    
    except Exception as e:

        print("Error", e) 


  def _run(self, query: str) -> str:
      """Use the Image Generation Tool."""
      response = self._generate_image(prompt=query)
      return response

  async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return self._run(query, run_manager=run_manager.get_sync())