import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LandingPage from "./landingpage/LandingPage.jsx";
import AboutMe from "./aboutme/AboutMe.jsx";
import Projects from "./projects/Projects.jsx";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/aboutme" element={<AboutMe />} />
        <Route path="/projects" element={<Projects />} />
      </Routes>
    </Router>
  );
}

export default App;
