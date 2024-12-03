import argparse
import asyncio
from workflows.story import app

async def run_app(historical_figure):
    inputs = {"historical_figure": historical_figure}
    config = {"recursion_limit": 50}
    
    logs = []
    async for event in app.astream(inputs, config=config):
        for k, v in event.items():
            if k != "__end__":
                logs.append(v)
    
    for log in logs:
        print(log)

def main():
    parser = argparse.ArgumentParser(description="Run the Story app for a historical figure.")
    parser.add_argument(
        "--historical_figure", 
        type=str, 
        required=True, 
        help="Name of the historical figure to generate a story for."
    )
    args = parser.parse_args()
    
    asyncio.run(run_app(args.historical_figure))

if __name__ == "__main__":
    main()
