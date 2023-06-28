# Helper class for text generation, contacts OpenAI's API
# three models will be available:
# 1. A finetuned davinci model
# 2. GPT-3.5-turbo
# 3. GPT-4

import os

import openai
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

load_dotenv()

BASE_TEMPERATURE = float(os.getenv("BASE_TEMPERATURE"))


# Queries a chatGPT model with messages using OpenAI's api
async def query_chat_model(messages: list, chat_model_name: str, temperature: float = BASE_TEMPERATURE,
                           functions=None, function_call="auto"):
    if functions is None:
        functions = []
    response = await query_openai_chatgpt_model_with_backoff(
        model=chat_model_name,
        messages=messages,
        functions=functions,
        temperature=temperature,
        function_call=function_call,
    )
    return response


# API methods
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
async def query_openai_model_with_backoff(**kwargs):
    response = await openai.Completion.acreate(**kwargs)
    return response


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
async def query_openai_chatgpt_model_with_backoff(**kwargs):
    response = await openai.ChatCompletion.acreate(**kwargs)
    return response


def get_messages_from_system_and_user_prompts(system_prompts: list, user_prompts: list):
    messages = []
    for i in range(len(system_prompts)):
        messages.append({
            "role": "system",
            "content": system_prompts[i]
        })
    for i in range(len(user_prompts)):
        messages.append({
            "role": "user",
            "content": user_prompts[i]
        })
    return messages
