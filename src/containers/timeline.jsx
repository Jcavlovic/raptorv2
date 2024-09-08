import React from "react";

/*
  https://www.shecodes.io/athena/38751-how-to-import-all-images-of-a-folder-into-a-react-component
  Use this website to help create the timeline.
*/

const images = require.context("../assets", true);

const imageList = images.keys().map((image) => images(image));

function ImageGallary() {
  return (
    <div>
      {imageList.map((image, index) => (
        <img key={index} src={image.default} alt={`image-${index}`} />
      ))}
    </div>
  );
}

export default ImageGallary;
