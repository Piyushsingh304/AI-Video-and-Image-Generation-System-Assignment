import React from "react";
import { useNavigate } from "react-router-dom";
import "./LandingPage.css";

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <h1>Welcome to AI Image Generator</h1>
      <button className="start-button" onClick={() => navigate("/main")}>
        Get Started
      </button>
    </div>
  );
};

export default LandingPage;
