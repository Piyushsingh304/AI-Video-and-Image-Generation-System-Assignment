import React, { useState } from "react";
import axios from "axios";
import ImageDisplay from "./ImageDisplay";
import "./MainPage.css";

const MainPage = () => {
  const [prompt, setPrompt] = useState("");
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!prompt) return alert("Please enter a prompt!");

    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/generate-images", {
        prompt,
      });
      setImages(response.data.images);
    } catch (error) {
      console.error("Generation error:", error);
      alert("Failed to generate images: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setPrompt("");
    setImages([]);
    setLoading(false);
  };

  return (
    <div className="main-container">
      <h1>AI Image Generator</h1>
      <div className="controls">
        <textarea
          className="prompt-input"
          placeholder="Enter your prompt here..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <div className="button-container">
          <button 
            className="generate-button" 
            onClick={handleGenerate} 
            disabled={loading}
          >
            {loading ? "Generating..." : "Generate Images"}
          </button>
          <button 
            className="reset-button" 
            onClick={handleReset}
            disabled={loading || (!prompt && !images.length)}
          >
            Reset
          </button>
        </div>
      </div>
      {images.length > 0 && <ImageDisplay images={images} />}
    </div>
  );
};

export default MainPage;