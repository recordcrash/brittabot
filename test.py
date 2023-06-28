import asyncio
import json
import os

import openai
from dotenv import load_dotenv

from models import EpisodeSceneParams, EpisodeParams, SceneLinesParams
from text_generation import query_chat_model, get_messages_from_system_and_user_prompts

SCRIPT_MODEL_NAME = 'gpt-4-0613'

SCRIPT_TEMPERATURE = 1.0

SCRIPT_OUTLINE_PROMPT = open("prompts/script_outline_prompt.txt", "r").read()

GET_SCENES_FUNCTION = {
    "name": "get_scenes",
    "description": "Gets all the scene summaries of a 20 minute Community episode for a particular premise",
    # premise: str
    # story_circle: List[str]
    # season: int
    # characters List[Literal[...]
    "parameters": EpisodeParams.schema()
}

GET_LINES_FUNCTION = {
    "name": "get_lines",
    "description": "Given a Community episode scene, generates the lines of dialogue for the scene",
    # scenes: Scene
    # Scene is outline: str, story_circle_steps: List[int], characters: List[str], guest_characters: [List[str]
    "parameters": EpisodeSceneParams.schema()
}

PRINT_LINES_FUNCTION = {
    "name": "print_lines",
    "description": "Given a Community scene, prints the lines of dialogue for each character in the scene",
    # lines: List[SceneHeading|CharacterLine|SceneAction]
    # SceneHeading is content: str
    # SceneAction is content: str
    # CharacterLine is characters: List[str], line: str, emotion: Literal[...], tone: Literal[...],
    # volume: Literal[...], speed: Literal[...], pitch: Literal[...], pause: Literal[...],
    # emphasis: Literal[...], punctuation: Literal[...]
    "parameters": SceneLinesParams.schema()
}

ALL_FUNCTIONS = [GET_SCENES_FUNCTION, GET_LINES_FUNCTION, PRINT_LINES_FUNCTION]


def write_json_to_jsonl_file(json_string: str, filename: str):
    with open(f"output/{filename}.jsonl", "a", encoding="UTF-8") as episodes_file:
        json_string = json_string.replace("    ", "")
        json_string = json_string.replace("   ", "")
        json_string = json_string.replace("  ", "")
        json_string_in_one_line = json_string.replace("\n", "")
        episodes_file.write(json_string_in_one_line + "\n")


def write_lines_to_episode_file(lines: list):
    with open(f"output/episode.txt", "a", encoding="UTF-8") as lines_file:
        for line in lines:
            lines_file.write(line + "\n")


# calls
def get_scenes(json_string: str):
    """
    Calls the GPT API to generate a list of scenes for a Community episode premise, using a JSON for an episode
    generated by a previous GPT API call
    """
    function_args = json.loads(json_string)
    write_json_to_jsonl_file(json_string, "episodes")
    episode = EpisodeParams.construct(**function_args)
    write_lines_to_episode_file([episode.premise, '\n'])
    return json_string


def get_lines(json_string: str):
    """
    Calls the GPT API to generate a list of lines for a Community scene, using a JSON for an episode generated by a
    previous GPT API call
    """
    function_args = json.loads(json_string)
    write_json_to_jsonl_file(json_string, "episode_scenes")
    # turn json object into a list of python objects we can use the period accessor for
    scene = EpisodeSceneParams.construct(**function_args['scene'])
    write_lines_to_episode_file([scene.scene_heading, '\n'])
    # return the JSON string as an object
    return json_string


def print_lines(json_string: str):
    """
    Prints the lines of dialogue for each character in a Community scene
    """
    function_args = json.loads(json_string)
    write_json_to_jsonl_file(json_string, "scene_lines")
    lines = [SceneLinesParams.construct(**line) for line in function_args['lines']]
    for line in lines:
        # check if it has the 'content' attribute
        if hasattr(line, 'content'):
            write_lines_to_episode_file([line.content, '\n'])
        else:
            characters_upper = [character.upper() for character in line.characters]
            characters_line = " ".join(characters_upper)
            write_lines_to_episode_file([characters_line, line.line, '\n'])
    return json_string


async def run_conversation(user_prompt: str, model_name: str):
    # Step 1: send the conversation and available functions to GPT
    print("1. Calling ChatGPT for get scenes request")

    messages = get_messages_from_system_and_user_prompts(
        system_prompts=[SCRIPT_OUTLINE_PROMPT],
        user_prompts=[user_prompt],
    )
    response = await query_chat_model(
        messages=messages,
        chat_model_name=model_name,
        temperature=SCRIPT_TEMPERATURE,
        functions=ALL_FUNCTIONS,
        function_call=GET_SCENES_FUNCTION,
    )
    response_message = response["choices"][0]["message"]

    while response_message is not None:
        if response_message.get("function_call"):
            available_functions = {
                "get_scenes": get_scenes,
                "get_lines": get_lines,
                "print_lines": print_lines,
            }
            function_name = response_message["function_call"]["name"]
            print(f"2. ChatGPT returns a function call for {function_name}")
            function_to_call = available_functions[function_name]
            function_arguments = response_message["function_call"]["arguments"]
            # check if function_arguments is a valid JSON string, otherwise, try again without pushing
            # messages
            try:
                json.loads(function_arguments)
            except json.decoder.JSONDecodeError as e:
                print("Invalid JSON string, retrying...", e)
                # remove invalid message
                messages.pop()
                # try again with the previous message
                response_message = messages[-1]
                continue
            function_response = function_to_call(function_arguments)
            messages.append(response_message)
            messages.append({
                "role": "function",
                "name": function_name,
                "content": function_response,
            })
            print(f"3. Calling ChatGPT for {function_name} request")

        else:
            print(f"3. ChatGPT returns no function call, breaking...")
            messages.append(response_message)
            break
        second_response = await query_chat_model(
            messages=messages,
            chat_model_name=model_name,
            temperature=SCRIPT_TEMPERATURE,
            functions=ALL_FUNCTIONS,
        )
        response_message = second_response["choices"][0]["message"]

    print("4. ChatGPT finishes!")
    print(response_message)


# define main
def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_KEY")
    print("Welcome to the ScriptBot test script!")
    default_prompt = "Come up with a novel and creative episode idea yourself and then outline it"
    message = asyncio.run(
        run_conversation(default_prompt,
                         SCRIPT_MODEL_NAME)
    )
    print(message)


main()