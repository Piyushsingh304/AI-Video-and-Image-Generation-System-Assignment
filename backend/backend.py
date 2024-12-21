import os
import io
import uuid
import base64
from datetime import datetime
from typing import List, Optional

import requests
from PIL import Image
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from pymongo import MongoClient
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
from authentication import auth


load_dotenv()  

HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
HUGGINGFACE_HEADERS = {
    "Authorization": f"Bearer {auth}"
}

app = FastAPI(title="AI Image Generation Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ImageGenerationRequest(BaseModel):
    prompt: str
    user_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    notification_time: Optional[datetime] = None

class ImageGenerationResponse(BaseModel):
    generation_id: str
    user_id: str
    prompt: str
    status: str
    image_paths: List[str] = []
    generated_at: datetime

def generate_image_as_base64(prompt: str) -> str:
    """Generate an image using Hugging Face API and return as a base64 string."""
    try:
        response = requests.post(
            HUGGINGFACE_API_URL, 
            headers=HUGGINGFACE_HEADERS, 
            json={"inputs": prompt}
        )
        response.raise_for_status()
        # Encode the image bytes to base64
        return base64.b64encode(response.content).decode("utf-8")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

@app.post("/generate-images", response_model=dict)
async def create_image_generation(request: ImageGenerationRequest):
    # Define prompt variations and style modifiers
    prompt_variations = [
        f"({request.prompt}), award-winning photography, 32k ultra resolution, masterful composition, professional studio lighting, shot on Hasselblad H6D-400C, sharp focus throughout frame, perfect focus, centered, extreme detail, no blur, crystal clear",
        f"({request.prompt}), ultra photoreal, magazine quality, highly detailed 8k rendering, professional color grading, perfect lighting, sharp focus, no artifacts, pristine quality, masterful photography",
        f"({request.prompt}), photorealistic masterpiece, professional photography, extreme detail, perfect composition, hyperrealistic quality, ultra-precise details, flawless execution, unedited raw photo"
    ]

    style_modifiers = [
        "best quality, masterful technique, perfectly clear, extremely detailed, sharp focus, 32k UHD, professional photography, high-end production value, precise detailing, perfect composition -blur -haze -artifacts -noise -watermark",
        "ultra quality, perfect clarity, extreme resolution, highly detailed, precise shadows, commercial grade, absolute realism, natural perspective, high fidelity -painting -illustration -drawing -cartoon -artistic -render",
        "perfect exposure, impeccable detail, photographic excellence, true-to-life colors, natural lighting, ultra-realistic details, professional quality, RAW format, perfect clarity -grain -noise -distortion -aberration"
    ]

    # Generate base64 images
    images_base64 = []
    for i in range(len(prompt_variations)):
        try:
            # Combine variation and style modifier
            final_prompt = f"{prompt_variations[i]}, {style_modifiers[i]}"
            image_base64 = generate_image_as_base64(final_prompt)
            images_base64.append(image_base64)
        except Exception as e:
            print(f"Error generating image {i}: {e}")

    return {
        "prompt": request.prompt,
        "images": images_base64,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)