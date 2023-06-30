from typing import List, Literal

from pydantic import BaseModel, Field


class EpisodeParams(BaseModel):
    """
    Params for an episode for a particular Community episode premise
    """
    premise: str = Field(..., description="A high-level outline")
    story_circle: List[str] = Field(..., description="Short synopses for each step of the story circle")
    season: Literal[1, 2, 3, 4, 5, 6] = Field(...)
    characters: List[Literal[
        "abed", "jeff", "britta", "troy", "annie", "pierce", "chang", "dean", "elroy", "shirley", "frankie", "hickey"]] = \
        Field(..., description="Main characters involved in the episode.")


class Scene(BaseModel):
    """
    Params for a Community scene, with metadata about its position in the story circle
    """
    outline: str = Field(..., description="A medium-level outline")
    scene_heading: str = Field(..., description="Script scene headings")
    story_circle_steps: List[int] = Field(..., description="Story circle steps tackled")
    characters: List[Literal[
        "abed", "jeff", "britta", "troy", "annie", "pierce", "chang", "dean", "elroy", "shirley", "frankie", "hickey"]] = \
        Field(..., description="Main characters speaking")
    guest_characters: List[str] = Field(...)


class EpisodeSceneParams(BaseModel):
    """
    Params for a scene for a particular Community episode
    """
    scene: Scene


class CharacterLine(BaseModel):
    characters: List[str] = Field(..., description="Character/multiple characters speaking at once")
    line: str = Field(..., description="The line of dialogue")
    tone: Literal["normal", "sarcastic", "angry", "sad", "happy", "scared", "disgusted"] = \
        Field(...)
    # removed to save money on prompting
    # emotion: Literal["normal", "happy", "sad", "angry", "surprised", "scared", "disgusted"] = \
    #     Field(..., description="The emotion of the character saying the line.")
    # volume: Literal["normal", "whisper", "shout"] = \
    #     Field(..., description="The volume of the character saying the line.")
    # speed: Literal["normal", "slow", "fast"] = \
    #     Field(..., description="The speed of the character saying the line.")
    # pitch: Literal["normal", "low", "high"] = \
    #     Field(..., description="The pitch of the character saying the line.")
    # pause: Literal["normal", "short", "long"] = \
    #     Field(..., description="The pause between the character saying the line and the next character saying their "
    #                            "line.")
    # emphasis: Literal["normal", "emphasized"] = \
    #     Field(..., description="Whether the character is emphasizing their line or not.")
    # punctuation: Literal["normal", "exclamation", "question"] = \
    #     Field(..., description="The punctuation of the line. Exclamation points and question marks are only used for "
    #                            "the last line of a scene.")


class SceneAction(BaseModel):
    content: str = Field(..., description="actions in active voice and present tense, i.e. 'Jeff stands up'")


class SceneLinesParams(BaseModel):
    """
    Params for a list of lines for a particular Community scene
    """
    lines: List[CharacterLine | SceneAction] = \
        Field(..., description="Lines for a particular Community scene. "
                               "CharacterLine MUST be used for dialog, and SceneAction MUST be used for actions")
