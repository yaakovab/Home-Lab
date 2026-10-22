from smolagents import CodeAgent, WebSearchTool, InferenceClientModel

model = InferenceClientModel(model_id='Qwen/Qwen2.5-Coder-32B-Instruct')
agent = CodeAgent(tools=[WebSearchTool()], model=model, stream_outputs=True)

agent.run("How many seconds would it take for a leopard at full speed to run through Pont Des A")
