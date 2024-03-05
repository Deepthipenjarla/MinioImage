import React, { useState, useEffect } from "react";
import "./Photouploader.css"; // Update the import statement

const PhotoUploader = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [photos, setPhotos] = useState([]);
  const [imageUrls, setImageUrls] = useState([]);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleUpload = () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append("file", selectedFile, selectedFile.name);

      fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          console.log("File uploaded successfully:", data.message);
          // After uploading, refresh the list of photos
          fetchPhotos();
        })
        .catch((error) => {
          console.error("Error uploading file:", error);
        });
    } else {
      console.warn("No file selected.");
    }
  };

  const fetchPhotos = () => {
    fetch("http://localhost:5000/photos")
      .then((response) => response.json())
      .then((data) => {
        setPhotos(data);
        // Set image URLs for rendering
        const urls = data.map(
          (photo) => `http://localhost:5000/photos/${photo}`
        );
        setImageUrls(urls);
      });
  };

  useEffect(() => {
    fetchPhotos();
  }, []);

  return (
    <div className="container">
      <nav className="navbar">
        <h1>UPLOAD YOUR PHOTO HERE</h1>
      </nav>
      <div className="upload-container">
        <input type="file" onChange={handleFileChange} />
        <button className="upload-button" onClick={handleUpload}>
          Upload
        </button>
      </div>
      <div className="photo-list">
        <h2>Stored Photos:</h2>
        <ul>
          {imageUrls.map((imageUrl, index) => (
            <li key={index}>
              <img src={imageUrl} alt={`Uploaded Photo ${index}`} />
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default PhotoUploader;
