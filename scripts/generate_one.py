"""
Generate a single image via ComfyUI HTTP API.

Workflow mirrors script_examples/basic_api_example.py but polls /history until
the prompt finishes and downloads the resulting PNG.
"""

import json
import sys
import time
from pathlib import Path
from urllib import error, parse, request

BASE = "http://127.0.0.1:8188"
PROMPT_TEXT = """
{
    "3": {
        "class_type": "KSampler",
        "inputs": {
            "cfg": 8,
            "denoise": 1,
            "latent_image": ["5", 0],
            "model": ["4", 0],
            "negative": ["7", 0],
            "positive": ["6", 0],
            "sampler_name": "euler",
            "scheduler": "normal",
            "seed": 8566257,
            "steps": 20
        }
    },
    "4": {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {"ckpt_name": "v1-5-pruned-emaonly.safetensors"}
    },
    "5": {
        "class_type": "EmptyLatentImage",
        "inputs": {"batch_size": 1, "height": 512, "width": 512}
    },
    "6": {
        "class_type": "CLIPTextEncode",
        "inputs": {"clip": ["4", 1], "text": "PROMPT_PLACEHOLDER"}
    },
    "7": {
        "class_type": "CLIPTextEncode",
        "inputs": {"clip": ["4", 1], "text": "bad hands, blurry, low quality"}
    },
    "8": {
        "class_type": "VAEDecode",
        "inputs": {"samples": ["3", 0], "vae": ["4", 2]}
    },
    "9": {
        "class_type": "SaveImage",
        "inputs": {"filename_prefix": "ComfyUI_smoke", "images": ["8", 0]}
    }
}
"""


def http_post_json(url: str, payload: dict, timeout: int = 30) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def http_get_json(url: str, timeout: int = 10) -> dict:
    with request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read())


def http_get_bytes(url: str, timeout: int = 60) -> bytes:
    with request.urlopen(url, timeout=timeout) as resp:
        return resp.read()


def wait_for_completion(prompt_id: str, timeout: float = 600.0) -> dict:
    """Poll /history/<id> until outputs appear."""
    history_url = f"{BASE}/history/{parse.quote(prompt_id)}"
    deadline = time.monotonic() + timeout
    last_log = 0.0
    while time.monotonic() < deadline:
        try:
            history = http_get_json(history_url, timeout=10)
        except error.HTTPError as e:
            if e.code != 404:
                raise
            history = {}
        entry = history.get(prompt_id)
        if entry and entry.get("outputs"):
            return entry
        now = time.monotonic()
        if now - last_log > 10:
            print(f"  ... still waiting ({int(deadline - now)}s left)", flush=True)  # noqa: T201
            last_log = now
        time.sleep(2)
    raise TimeoutError(f"prompt {prompt_id} did not finish within {timeout}s")


def main() -> int:
    prompt_text = "a corgi astronaut floating in space, ultra detailed, cinematic lighting"
    out_path = Path("/Users/jinno/ComfyUI/output/comfyui_smoke.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    prompt = json.loads(PROMPT_TEXT)
    prompt["6"]["inputs"]["text"] = prompt_text
    prompt["3"]["inputs"]["seed"] = int(time.time()) % (2**31)

    print(f"[1/3] Queueing prompt: {prompt_text!r}")  # noqa: T201
    ack = http_post_json(f"{BASE}/prompt", {"prompt": prompt}, timeout=60)
    prompt_id = ack["prompt_id"]
    print(f"      prompt_id={prompt_id}")  # noqa: T201

    print("[2/3] Waiting for completion (this may take a couple of minutes on MPS)...")  # noqa: T201
    entry = wait_for_completion(prompt_id, timeout=600)
    outputs = entry["outputs"]

    # Find first SaveImage output image.
    image_info = None
    for node_out in outputs.values():
        if "images" in node_out:
            image_info = node_out["images"][0]
            break
    if image_info is None:
        print("No images in outputs:", outputs, file=sys.stderr)  # noqa: T201
        return 1

    filename = image_info["filename"]
    subfolder = image_info.get("subfolder", "")
    img_type = image_info.get("type", "output")
    qs = parse.urlencode({"filename": filename, "subfolder": subfolder, "type": img_type})
    img_url = f"{BASE}/view?{qs}"
    print(f"[3/3] Downloading image: {filename}")  # noqa: T201
    data = http_get_bytes(img_url)
    out_path.write_bytes(data)
    print(f"      saved: {out_path}  ({len(data):,} bytes)")  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())
