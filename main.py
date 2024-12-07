import os
import io
import uuid
from datetime import datetime
from typing import List, Optional
from authentication import auth, mongo

import requests
from PIL import Image
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
from authentication import auth  # Importing your token from another file

HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
HUGGINGFACE_HEADERS = {
    "Authorization": f"Bearer {auth}"
}

# MongoDB Setup
client = MongoClient(mongo)
db = client['Project_0']
image_generations_collection = db['image_generations']

app = FastAPI(title="AI Image Generation Service")

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

def generate_image(prompt: str) -> bytes:
    """Generate an image using Hugging Face Stable Diffusion API"""
    try:
        response = requests.post(
            HUGGINGFACE_API_URL, 
            headers=HUGGINGFACE_HEADERS, 
            json={"inputs": prompt}
        )
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

@app.post("/generate-images", response_model=ImageGenerationResponse)
async def create_image_generation(request: ImageGenerationRequest):
    generation_id = str(uuid.uuid4())
    user_id = request.user_id or str(uuid.uuid4())
    
    # Create user directory if not exists
    user_dir = f"generated_content/{user_id}"
    os.makedirs(user_dir, exist_ok=True)
    
    # Generate 5 images
    image_paths = []
    for i in range(5):
        try:
            image_bytes = generate_image(request.prompt)
            image_path = f"{user_dir}/image_{generation_id}_{i}.png"
            
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            
            image_paths.append(image_path)
        except Exception as e:
            # Log error but continue generating other images
            print(f"Error generating image {i}: {e}")
    
    # Store generation metadata in MongoDB
    generation_record = {
        "_id": generation_id,
        "user_id": user_id,
        "prompt": request.prompt,
        "status": "Completed" if image_paths else "Failed",
        "image_paths": image_paths,
        "generated_at": datetime.utcnow(),
        "notification_time": request.notification_time
    }
    
    image_generations_collection.insert_one(generation_record)
    
    return ImageGenerationResponse(
        generation_id=generation_id,
        user_id=user_id,
        prompt=request.prompt,
        status="Completed" if image_paths else "Failed",
        image_paths=image_paths,
        generated_at=datetime.utcnow()
    )

@app.get("/generations/{user_id}", response_model=List[ImageGenerationResponse])
async def get_user_generations(user_id: str):
    """Retrieve all image generations for a specific user"""
    generations = list(image_generations_collection.find({"user_id": user_id}))
    
    return [
        ImageGenerationResponse(
            generation_id=str(gen['_id']),
            user_id=gen['user_id'],
            prompt=gen['prompt'],
            status=gen['status'],
            image_paths=gen['image_paths'],
            generated_at=gen['generated_at']
        ) for gen in generations
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

