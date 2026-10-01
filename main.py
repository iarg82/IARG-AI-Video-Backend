import os, time, base64
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from google import genai
from google.genai import types

app = FastAPI(title="IARG AI Video API")
OUT = Path("generated")
OUT.mkdir(exist_ok=True)

def client():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise HTTPException(500, "GEMINI_API_KEY is not configured")
    return genai.Client(api_key=key)

@app.get("/")
def home():
    return {"app":"IARG AI Video","status":"running"}

@app.post("/text-to-video")
def text_to_video(prompt: str = Form(...), aspect_ratio: str = Form("9:16")):
    if aspect_ratio not in ("9:16","16:9"):
        raise HTTPException(400, "aspect_ratio must be 9:16 or 16:9")
    c = client()
    op = c.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        config=types.GenerateVideosConfig(aspect_ratio=aspect_ratio)
    )
    while not op.done:
        time.sleep(10)
        op = c.operations.get(op)
    video = op.response.generated_videos[0]
    filename = f"{int(time.time())}.mp4"
    path = OUT / filename
    c.files.download(file=video.video, destination=str(path))
    return {"ok": True, "video": f"/video/{filename}"}

@app.post("/image-to-video")
async def image_to_video(
    prompt: str = Form(...),
    aspect_ratio: str = Form("9:16"),
    image: UploadFile = File(...)
):
    if aspect_ratio not in ("9:16","16:9"):
        raise HTTPException(400, "aspect_ratio must be 9:16 or 16:9")
    data = await image.read()
    mime = image.content_type or "image/png"
    c = client()
    input_image = types.Image(image_bytes=data, mime_type=mime)
    op = c.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        image=input_image,
        config=types.GenerateVideosConfig(aspect_ratio=aspect_ratio)
    )
    while not op.done:
        time.sleep(10)
        op = c.operations.get(op)
    video = op.response.generated_videos[0]
    filename = f"{int(time.time())}.mp4"
    path = OUT / filename
    c.files.download(file=video.video, destination=str(path))
    return {"ok": True, "video": f"/video/{filename}"}

@app.get("/video/{filename}")
def video(filename: str):
    path = OUT / Path(filename).name
    if not path.exists():
        raise HTTPException(404, "Video not found")
    return FileResponse(path, media_type="video/mp4")
