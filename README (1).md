
# Text to image and Text to video

## 🚀 Project Overview
This cutting-edge Python script leverages state-of-the-art AI technology to transform text prompts into dynamic video sequences using the Damo-Vilab text-to-video generation model.

## Note
- I have Implemented text to video in google colab due limitations of my system.
- I will not be uploading my mongoDB connection link and huggingface authentication because of security reasons.
- You can replace it with your own in the authentication.py file in variable auth and mongo.
- After the video is generated it will be stored in tmp folder inside files section.
- The video can be downloaded from there and can be played using VLC media player.
- The Api can be run using Postman.
- Further I have included a tinker basded application as well. 

## ✨ Features
- 🔤 Text-driven video generation
- 🤖 Advanced AI diffusion model
- 💻 GPU-accelerated processing
- 🎥 Customizable video generation

## 📋 System Requirements
- Python 3.8+
- CUDA-compatible NVIDIA GPU
- 16GB+ RAM
- 8GB+ GPU VRAM

## 🤖Stable Diffusion Architecture:

1. Model Components

- Text Encoder: CLIP text transformer
- Diffusion UNet: Latent space image generation
- Variational Autoencoder (VAE): Compression and decompression of images

2. Diffusion Process

- Text prompt is encoded into a conditioning vector
- Latent space noise is progressively denoised
- Cross-attention mechanism allows text conditioning
- Uses classifier-free guidance for prompt alignment


3. Key Technical Details

- Trained on LAION-5B dataset
- Uses 4x downscaling in latent space
- Supports various image sizes and aspect ratios
- Modular design allows for fine-tuning and customization

## 🤖 Vilab Text-to-Video Architectures:

1. VideoCrafter Architecture

- Transformer-based video generation
- Uses latent diffusion similar to image models
- Key innovations:

    - Temporal attention mechanisms
    - Frame-by-frame consistency modeling
    - Hierarchical generation approach

2. Technical Approach

- Text encoder: Similar to Stable Diffusion
- Video generation in latent space
- Temporal modeling through:

    - Cross-frame attention
    - Motion prediction modules
    - Consistency regularization

3. Model Variants

- VideoCrafter1: Initial research model
- VideoCrafter2: Improved temporal coherence
- Supports various video resolutions
- Can generate videos from 16 to 64 frames



## 🎨 Example Prompts
- "A peaceful sunset over mountain ranges"
- "Futuristic cityscape with flying vehicles"
- "Underwater exploration of a vibrant coral reef"
- "Abstract geometric shapes morphing and dancing"

## 🔧 Configuration Options
- Adjust `num_inference_steps` for quality vs. speed trade-off
- Modify model precision settings
- Implement custom video export paths

## 📦 Dependencies
- PyTorch
- Hugging Face Diffusers
- Transformers
- NumPy

## 🚧 Limitations
- Generation time: 30-60 seconds
- Video quality depends on prompt complexity
- Requires significant computational resources

## 🔬 Technology Stack
- **Model**: Damo-Vilab Text-to-Video MS 1.7b
- **Framework**: Hugging Face Diffusers
- **Precision**: Float16
- **Acceleration**: CUDA GPU (T4 GPU Google colab)
- **FastApi**: Backend
- **MongoDB Atlas**: Database 

## 🙏 Acknowledgments
- Damo-Vilab Research Team
- Hugging Face Diffusers Community

## 🔍 Troubleshooting
- Verify GPU compatibility
- Check CUDA and PyTorch installation
- Ensure sufficient GPU memory
- Update graphics drivers

## 📚 Learning Resources
- [Hugging Face Diffusers Docs](https://huggingface.co/docs/diffusers)
- [PyTorch CUDA Guide](https://pytorch.org/get-started/locally/)
- [Damo-Vilab Model Card](https://huggingface.co/damo-vilab/text-to-video-ms-1.7b)

## 🎉 Enjoy Creating Unique Videos!
Transform your imagination into moving images with AI-powered text-to-video generation.