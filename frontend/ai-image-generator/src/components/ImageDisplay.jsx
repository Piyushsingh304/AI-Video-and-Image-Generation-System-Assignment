// ImageDisplay.jsx
import React from "react";
import "./ImageDisplay.css";

const ImageDisplay = ({ images }) => {
  return (
    <div className="image-display">
      {images.map((img, index) => (
        <div key={index} className="image-container">
          <img
            src={`data:image/png;base64,${img}`}
            alt={`Generated ${index + 1}`}
            className="generated-image"
          />
        </div>
      ))}
    </div>
  );
};

export default ImageDisplay;
