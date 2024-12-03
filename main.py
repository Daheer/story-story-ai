import asyncio
from workflows.story import app

async def run_app():
    
    inputs = {"historical_figure": "Ahmadu Bello"}
    config = {"recursion_limit": 50}
    
    logs = []
    async for event in app.astream(inputs, config=config):
        for k, v in event.items():
            if k != "__end__":
                logs.append(v)
    
    for log in logs:
        print(log)

def main():
    asyncio.run(run_app())

if __name__ == "__main__":
    main()
