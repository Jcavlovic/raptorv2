import React from "react";
import itemsFound from "./founditems";

const StatusBar = () => {
  const items = itemsFound;
  return (
    <div className="statusbar">
      <h1 className="statusbarTitle"> &ensp;Found Objects</h1>
      {itemsFound.map((itemFound, index) => (
        <li
          key={`${itemFound}${index}`}
          className="foundlist"
          onClick={() => {
            alert(`You clicked ${itemFound.item}`);
          }}
        >
          {" "}
          {itemFound.item} {itemFound.time}
        </li>
      ))}
    </div>
  );
};

export default StatusBar;
