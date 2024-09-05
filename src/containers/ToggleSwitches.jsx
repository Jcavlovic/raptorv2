import React, { useState } from "react";

const ToggleSwitches = () => {
  const [toggles, setToggles] = useState([
    {
      id: 1,
      text: "Life Raft",
      location: "./src/assets/Life_Raft.png",
      isChecked: false,
    },
    {
      id: 2,
      text: "Life Jacket",
      location: "./src/assets/Life_Jacket.png",
      isChecked: false,
    },
    {
      id: 3,
      text: "Life Ring",
      location: "./src/assets/Life_Ring.png",
      isChecked: false,
    },
  ]);

  const handleToggle = (id) => {
    setToggles((prevToggles) => {
      // Update the state by toggling the appropriate switch
      const updatedToggles = prevToggles.map((toggle) =>
        toggle.id === id ? { ...toggle, isChecked: !toggle.isChecked } : toggle
      );

      // Find the updated toggle and print its current state
      const currentToggle = updatedToggles.find((toggle) => toggle.id === id);
      console.log(
        `Switch ${currentToggle.id}: ${currentToggle.isChecked ? "ON" : "OFF"}`
      );

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
