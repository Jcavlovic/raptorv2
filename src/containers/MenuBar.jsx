import React from "react";

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

export default MenuBar;
