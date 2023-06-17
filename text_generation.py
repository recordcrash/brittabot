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

FINETUNED_MODEL_NAME = os.getenv("MODEL_NAME")

BASE_TEMPERATURE = float(os.getenv("BASE_TEMPERATURE"))

CHEAP_CHAT_MODEL_NAME = 'gpt-3.5-turbo'

EXPENSIVE_CHAT_MODEL_NAME = 'gpt-4'

IMAGE_DESCRIPTION_SYSTEM_PROMPT = open("prompts/image_description_system_prompt.txt", "r").read()
IMAGE_DESCRIPTION_FAKE_USER_PROMPT = open("prompts/image_description_fake_user_prompt.txt", "r").read()

ALCHEMY_SYSTEM_PROMPT = open("prompts/alchemy_system_prompt_json.txt", "r").read()
ALCHEMY_FAKE_USER_PROMPT = open("prompts/alchemy_fake_user_prompt_json.txt", "r").read()


# Queries a chatGPT model with messages using OpenAI's api
async def query_chat_model(messages: list, chat_model_name: str, temperature: float = BASE_TEMPERATURE):
    response = await query_openai_chatgpt_model_with_backoff(
        model=chat_model_name,
        messages=messages,
        temperature=temperature,
    )
    # get the first result
    text = response.choices[0].message.content
    return text


# Directly queries the finetuned model using OpenAI's api
async def query_finetuned_openai_model(prompt_with_items: str, temperature: float = BASE_TEMPERATURE):
    response = await query_openai_model_with_backoff(
        model=FINETUNED_MODEL_NAME,
        prompt=prompt_with_items,
        max_tokens=500,
        temperature=temperature,
        stop=[" END"]
    )
    # get the first result
    text = response.choices[0].text
    # remove empty space at the beginning
    processed_text = text[1:]
    return processed_text


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


def get_image_description_messages(prompt: str):
    messages = get_messages_from_system_and_user_prompts(system_prompts=[IMAGE_DESCRIPTION_SYSTEM_PROMPT],
                                                         user_prompts=[IMAGE_DESCRIPTION_FAKE_USER_PROMPT, prompt])
    return messages
