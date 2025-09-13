import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
from agents.generator_agent import GeneratorAgent
from agents.descriptor_agent import DescriptorAgent
import asyncio

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-2024-08-06")

async def main():
    openai_model_client = OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=API_KEY
    )

    generator_agent = GeneratorAgent(openai_model_client)

    user_input = input("¿Qué quieres que genere el LLM? ")

    # 1. Primer paso: pedir al LLM que mejore el prompt
    pre_prompt = (
        "Reformula el siguiente pedido de usuario para generar un informe automatizado. "
        "Indica que el informe debe estar en HTML y, si hay datos, que incluya una lista en formato Python para graficar. "
        "No pidas aclaraciones metodológicas. Pedido del usuario: "
        f"{user_input}"
    )
    improved_prompt_response = await openai_model_client.create([
        UserMessage(content=pre_prompt, source="user")
    ])
    improved_prompt = improved_prompt_response.content.strip()

    # 2. Segundo paso: usar el prompt mejorado para generar el informe
    response = await openai_model_client.create([
        UserMessage(content=improved_prompt, source="user")
    ])
    generated_content = response.content

    # Genera ambos archivos automáticamente
    generator_agent.save_file(generated_content, 'pdf', 'output.pdf', user_input)
    generator_agent.save_file(generated_content, 'png', 'output.png', user_input)

    # Describe ambos archivos
    for file_path in ['output.pdf', 'output.png']:
        descriptor_agent = DescriptorAgent(file_path)
        description = descriptor_agent.describe_file()
        print(f"\nDescripción automática de {file_path}:")
        print(description)

    await openai_model_client.close()

if __name__ == "__main__":
    asyncio.run(main())