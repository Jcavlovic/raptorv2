import { useState } from "react";
import "./App.css";

function App() {
  return (
    <div>
      <MenuBar />
      <ToggleSwitches />
      <StatusBar />
    </div>
  );
}

const Button = ({ href, text, className }) => {
  return (
    <a href={href} key={text} className={className}>
      <button>{text}</button>
    </a>
  );
};

const MenuBar = () => {
  const pages = [
    { webpage: "./gopro", text: "GoPro" },
    { webpage: "./drone", text: "Drone" },
    { webpage: "./library", text: "Library" },
    { webpage: "./help", text: "Help" },
  ];

  return (
    <div className="menubar">
      {pages.map((page, index) => (
        <Button
          href={page.webpage}
          key={page.text}
          className={`button-${index + 1}`}
          text={page.text}
        />
      ))}
    </div>
  );
};

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

const StatusBar = () => {
  return (
    <div className="statusbar">
      <h1>Status Updates</h1>
      <li>Life Jacket Found 00:00:00</li>
      <li>Life Jacket Found 00:00:00</li>
      <li>Life Jacket Found 00:00:00</li>
    </div>
  );
};
export default App;
