import requests
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from authentication import auth
import io

# Hugging Face API configuration
API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
headers = {"Authorization": f"Bearer {auth}"}

app = ctk.CTk()
app.geometry("532x633")
app.title("Stable Bud")
ctk.set_appearance_mode("dark")

prompt = ctk.CTkEntry(master=app, height=40, width=512, font=("Arial", 20), text_color="black", fg_color="white")
prompt.place(x=10, y=10)

lmain = ctk.CTkLabel(master=app, height=512, width=512)
lmain.place(x=10, y=100)

def generate():
    payload = {
        "inputs": prompt.get(),
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        # Convert the image from bytes to PIL Image
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        
        # Save the image
        image.save('generatedimage.png')
        
        # Display the image in tkinter
        img = ImageTk.PhotoImage(image)
        lmain.configure(image=img)
        lmain.image = img
    else:
        print(f"Error: {response.status_code}, {response.text}")

trigger = ctk.CTkButton(master=app, height=40, width=120, font=("Arial", 20), text_color="white", fg_color="blue", command=generate)
trigger.configure(text="Generate")
trigger.place(x=206, y=60)

app.mainloop()