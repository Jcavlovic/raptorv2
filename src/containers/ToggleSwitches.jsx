import { useState } from "react";
import React from "react";

const ToggleSwitches = () => {
  const items = ["Life Raft", "Life Jacket", "Life Ring"];

  return (
    <div className="ToggleSwitches">
      <h1>Items</h1>
      {items.map((item, index) => (
        <ToggleSwitch
          key={`${item}${index}`}
          divClassName="switch_child"
          labelClassName="switch"
          textClassName="switch_text"
          text={item}
        />
      ))}
    </div>
  );
};

const ToggleSwitch = ({ divClassName, labelClassName, text }) => {
  const [isChecked, setIsChecked] = useState(false);

  const handleToggle = () => {
    setIsChecked((isChecked) => !isChecked);
    {
      isChecked
        ? console.log(`${text} ${isChecked}`)
        : console.log(`${text} ${isChecked}`);
    }
  };

  return (
    <div key={text} className={divClassName}>
      <h3>{text}</h3>
      <label className={labelClassName}>
        <input type="checkbox" checked={isChecked} onClick={handleToggle} />
        <span className="slider round"></span>
      </label>
    </div>
  );
};

export default ToggleSwitches;
