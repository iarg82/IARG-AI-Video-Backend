# IARG AI Video — Backend

This is a starter backend for the IARG AI Video app.

## What it does
- Text → Video
- Image → Video
- 9:16 or 16:9
- Uses Google's Veo 3.1 Gemini API
- Keeps the API key on the server via `GEMINI_API_KEY`

## Important
Do NOT put the Gemini API key inside the Android APK and do NOT send it in Chat.

## Install
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Android terminal: source .venv/bin/activate
pip install -r requirements.txt
```

Set the environment variable:
```bash
GEMINI_API_KEY="YOUR_KEY"
```

Run:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Then the Android app can call:
- POST /text-to-video
- POST /image-to-video
- GET /video/{filename}

Video generation is asynchronous and can take time. Veo 3.1 currently generates 4, 6, or 8 second videos and supports 9:16/16:9; generated audio is native.
