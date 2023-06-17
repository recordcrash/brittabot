# Helper class for image generation, contacts local AUTOMATIC1111 stable diffusion API
# location is usually http://127.0.0.1:7860/api/
import base64
import io
from typing import Tuple

import requests
from PIL import Image

# in order to get this to work, just follow instructions at https://github.com/AUTOMATIC1111

SERVER_IP = "http://127.0.0.1:7860/"

TEXT2IMG_ENDPOINT = SERVER_IP + "sdapi/v1/txt2img/"

IMG2IMG_ENDPOINT = SERVER_IP + "sdapi/v1/img2img/"

OPTIONS_ENDPOINT = SERVER_IP + "sdapi/v1/options/"

REMBG_ENDPOINT = SERVER_IP + "rembg/"

DEFAULT_REMBG_PAYLOAD = {
    "input_image": "",
    "model": "silueta",
    "return_mask": False,
    "alpha_matting": False,
    "alpha_matting_foreground_threshold": 240,
    "alpha_matting_background_threshold": 10,
    "alpha_matting_erode_size": 10
}

DEFAULT_IMG2IMG_PAYLOAD = {
    "init_images": [],
    "denoising_strength": 0.75,
    "image_cfg_scale": 0,
    "mask_blur": 4,
    "inpainting_fill": 0,
    "inpaint_full_res": False,
    "prompt": "",
    "seed": -1,
    "subseed": -1,
    "subseed_strength": 0,
    "seed_resize_from_h": -1,
    "seed_resize_from_w": -1,
    "batch_size": 1,
    "n_iter": 1,
    "steps": 50,
    "cfg_scale": 7,
    "width": 512,
    "height": 512,
}

FANTASSIFIED_ICONS_CHECKPOINT = "fantassifiedIcons_fantassifiedIconsV20.safetensors [8340e74c3e]"

GAME_ICON_INSTITUTE_CHECKPOINT = "gameIconInstitute_v30.safetensors [c112297163]"

STABLE_DIFFUSION_1_5_CHECKPOINT = "v1-5-pruned.ckpt [e1441589a6]"

DEFAULT_TEXT2IMG_PAYLOAD = {
    "override_settings": {
        "sd_model_checkpoint": GAME_ICON_INSTITUTE_CHECKPOINT
    },
    "enable_hr": False,
    "denoising_strength": 0,
    "firstphase_width": 0,
    "firstphase_height": 0,
    "prompt": "",
    "styles": [],
    "seed": -1,
    "subseed": -1,
    "subseed_strength": 0,
    "seed_resize_from_h": -1,
    "seed_resize_from_w": -1,
    "sampler_name": "DPM++ 2M SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 50,
    "cfg_scale": 7,
    "width": 512,
    "height": 512,
    "restore_faces": False,
    "tiling": False,
    "do_not_save_samples": False,
    "do_not_save_grid": False,
    "negative_prompt": "",
    "eta": 0,
    "s_min_uncond": 0,
    "s_churn": 0,
    "s_tmax": 0,
    "s_tmin": 0,
    "s_noise": 1,
    "override_settings_restore_afterwards": True,
    "script_args": [],
    "sampler_index": "DPM++ 2M SDE Karras",
    "script_name": None,
    "send_images": True,
    "save_images": True,
    "alwayson_scripts": {}
}

# POSITIVE_PROMPT_SUFFIX = ", ((item)), ((isolated on green background))"
#
# NEGATIVE_PROMPT_SUFFIX = "easynegative, ng_deepnegative_v1_75t, bad_prompt_version2, bad-artist"

POSITIVE_PROMPT_SUFFIX = ", ((game icon))"
NEGATIVE_PROMPT_SUFFIX = ", easynegative, ng_deepnegative_v1_75t, bad_prompt_version2, bad-artist"

ALCHEMITER_ASSET = Image.open("images/alchemiter_pad.png").convert("RGBA")


def generate_image(positive_prompt: str, negative_prompt: str) -> Tuple[Image, str]:
    # 1. contact the API with that prompt, DPM++ 2M SDE Karras, and default settings with batch size 1
    # 2. return the image
    payload = DEFAULT_TEXT2IMG_PAYLOAD.copy()
    payload["prompt"] = positive_prompt
    payload["negative_prompt"] = negative_prompt
    print(f"Contacting txt2img API at {TEXT2IMG_ENDPOINT} with payload")
    response = requests.post(url=TEXT2IMG_ENDPOINT, json=payload)
    response_json = response.json()
    image_base64 = response_json["images"][0]
    image = Image.open(io.BytesIO(base64.b64decode(image_base64.split(",", 1)[0])))
    return image, image_base64


def remove_background_from_picture(image_base64: str) -> Tuple[Image, str]:
    # uses REMBG_ENDPOINT to remove the background from the image and returns it
    # edit DEFAULT_REMBG_PAYLOAD
    payload = DEFAULT_REMBG_PAYLOAD.copy()
    payload["input_image"] = image_base64
    print(f"Contacting REMBG api at {REMBG_ENDPOINT} with payload")
    response = requests.post(url=REMBG_ENDPOINT, json=payload)
    response_json = response.json()
    image_base64 = response_json["image"]
    image = Image.open(io.BytesIO(base64.b64decode(image_base64.split(",", 1)[0])))
    return image, image_base64


def img2img_image(image_base64: str) -> Tuple[Image, str]:
    # calls the img2img api with the image and returns it
    payload = DEFAULT_IMG2IMG_PAYLOAD.copy()
    payload["init_images"] = [image_base64]
    print(f"Contacting img2img api at {IMG2IMG_ENDPOINT} with payload")
    response = requests.post(url=IMG2IMG_ENDPOINT, json=payload)
    response_json = response.json()
    image_base64 = response_json["images"][0]
    image = Image.open(io.BytesIO(base64.b64decode(image_base64.split(",", 1)[0])))
    return image, image_base64


def generate_picture(prompt: str) -> Image:
    # add suffixes
    positive_prompt = prompt.lower() + POSITIVE_PROMPT_SUFFIX
    negative_prompt = NEGATIVE_PROMPT_SUFFIX

    prompt = positive_prompt if negative_prompt == "" else positive_prompt + ", " + negative_prompt

    # generate image
    print(f"Generating image with prompt: {prompt}")
    image, image_base64 = generate_image(positive_prompt, negative_prompt)
    image.save("output/image.png")

    # remove background
    image_no_bg, image_no_bg_base_64 = remove_background_from_picture(image_base64)
    image_no_bg.save("output/image2.png")

    final_image = image_no_bg

    return final_image
