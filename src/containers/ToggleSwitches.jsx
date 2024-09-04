import { useState } from "react";
import React from "react";

const [toggles, setToggles] = useState([
  { id: 1, text: "Life Raft", isChecked: false },
  { id: 2, text: "Life Jacket", isChecked: false },
  { id: 3, text: "Life Ring", isChecked: false },
]);

const ToggleSwitches = () => {
  const items = ["Life Raft", "Life Jacket", "Life Ring"];

  return (
    <div className="ToggleSwitches">
      <h1>Items</h1>
      {items.map((item, index) => (
        <ToggleSwitch key={`${item}${index}`} />
      ))}
    </div>
  );
};

const ToggleSwitch = ({ divClassName, labelClassName, text }) => {
  const [{ isChecked }, setIsChecked] = useState(false);

  const handleToggle = () => {
    setIsChecked((isChecked) => !isChecked);
    {
      isChecked
        ? console.log(`${text} ${isChecked}`)
        : console.log(`${text} ${isChecked}`);
    }
  };

  return (
    <div key={text} className="switch_child">
      <h3>{text}</h3>
      <label className="switch">
        <input
          type="checkbox"
          defaultChecked={isChecked}
          onClick={handleToggle}
        />
        <span className="slider round"></span>
      </label>
    </div>
  );
};

export default ToggleSwitches;
