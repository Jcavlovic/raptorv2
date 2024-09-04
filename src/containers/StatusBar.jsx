import React from "react";

const StatusBar = () => {
  const itemsFound = [
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
    { item: "Life Raft", time: "00:00:00" },
  ];
  return (
    <div className="statusbar">
      <h1 className="statusbarTitle"> &ensp;Found Objects</h1>
      {itemsFound.map((itemFound) => (
        <li className="foundlist">
          {" "}
          {itemFound.item} {itemFound.time}
        </li>
      ))}
    </div>
  );
};

export default StatusBar;
