from workflows.story import app
from IPython.display import Image

Image(app.get_graph(xray=True).draw_mermaid_png(output_file_path="arch.png"))