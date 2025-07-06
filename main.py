from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os
from moviepy.editor import ImageClip

app = FastAPI()

class MediaRequest(BaseModel):
    imageDownloadUrl: str

@app.post("/assemble")
async def assemble_video(req: MediaRequest):
    image_url = req.imageDownloadUrl

    # Download the image
    img_response = requests.get(image_url)
    if img_response.status_code != 200:
        return {"error": "Failed to download image"}

    os.makedirs("tmp", exist_ok=True)
    image_path = "tmp/background.png"
    with open(image_path, "wb") as f:
        f.write(img_response.content)

    # Create video using MoviePy
    output_path = "tmp/final_video.mp4"
    clip = ImageClip(image_path, duration=600)  # 10 minutes
    clip.write_videofile(output_path, fps=1)

    return {"status": "success", "video": output_path}
