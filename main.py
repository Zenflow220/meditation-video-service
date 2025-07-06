from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
import requests
import os
from moviepy.editor import ImageClip

app = FastAPI()

class MediaRequest(BaseModel):
    imageDownloadUrl: str

@app.post("/assemble")
async def assemble_video(req: MediaRequest, background_tasks: BackgroundTasks):
    image_url = req.imageDownloadUrl

    # Try downloading the image
    img_response = requests.get(image_url)
    if img_response.status_code != 200:
        return {"error": "Failed to download image"}

    os.makedirs("tmp", exist_ok=True)
    image_path = "tmp/background.png"
    with open(image_path, "wb") as f:
        f.write(img_response.content)

    output_path = "tmp/final_video.mp4"

    # Start video creation in the background
    background_tasks.add_task(generate_video, image_path, output_path)

    return {
        "status": "processing",
        "message": "Video generation started. It will complete in the background.",
        "videoPath": output_path
    }

def generate_video(image_path, output_path):
    try:
        clip = ImageClip(image_path, duration=10)  # 10 minutes
        clip.write_videofile(output_path, fps=1)
    except Exception as e:
        print(f"Error during video generation: {e}")
