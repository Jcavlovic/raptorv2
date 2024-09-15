import React, { useState } from "react";
import axios from "axios";

const ToggleSwitches = () => {
  const [toggles, setToggles] = useState([
    {
      id: 1,
      text: "Life Raft",
      location: "src/containers/assets/Life_Raft2.png",
      isChecked: false,
    },
    {
      id: 2,
      text: "Life Jacket",
      location: "assets/Life_Jacket.png",
      isChecked: false,
    },
    {
      id: 3,
      text: "Life Ring",
      location: "assets/Life_Ring.png",
      isChecked: false,
    },
  ]);

  const handleToggle = (id) => {
    setToggles((prevToggles) => {
      // Update the state by toggling the appropriate switch
      const updatedToggles = prevToggles.map((toggle) =>
        toggle.id === id ? { ...toggle, isChecked: !toggle.isChecked } : toggle
      );

      // Construct the object expected by FastAPI
      const switchState = {
        switch1: updatedToggles[0].isChecked,
        switch2: updatedToggles[1].isChecked,
        switch3: updatedToggles[2].isChecked,
      };

      // Send the updated switch state to the FastAPI backend
      axios
        .post("http://192.168.1.23:8000/switches", switchState)
        .then((response) => console.log("Toggle state updated:", response.data))
        .catch((error) => console.error("Error updating toggles:", error));

      return updatedToggles;
    });
  };

  return (
    <div className="ToggleSwitches">
      <h1 className="toggleheader">&ensp;&ensp;&ensp;Items</h1>
      {toggles.map((toggle) => (
        <ToggleSwitch
          key={toggle.id}
          text={toggle.text}
          isChecked={toggle.isChecked}
          onToggle={() => handleToggle(toggle.id)}
          location={toggle.location}
        />
      ))}
    </div>
  );
};

const ToggleSwitch = ({ text, isChecked, onToggle, location }) => {
  return (
    <div className="switch_child">
      <h2 className="togglelabel">{text}</h2>
      <label className="switch">
        <input type="checkbox" checked={isChecked} onChange={onToggle} />
        <span className="slider round" />
      </label>
      <img src={location} className="toggleimages" onClick={onToggle} />
    </div>
  );
};

export default ToggleSwitches;
