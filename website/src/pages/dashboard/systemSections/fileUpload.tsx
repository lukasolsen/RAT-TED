import React, { useEffect, useRef, useState } from "react";
import { useLocation } from "react-router-dom";
import Import from "../../../components/FileUpload";

const FileUploader: React.FC = () => {
  const location = useLocation();
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [id, setId] = useState("");

  useEffect(() => {
    // Define the video source URL (replace with your actual URL)
    const getID = async () => {
      const hash = location.hash;

      // Use a regular expression to find the 'id' query parameter in the hash
      const match = hash.match(/id=([^&]+)/);

      if (match) {
        // Extract the 'id' value from the matched result
        setId(match[1]);
      }
    };
    getID();
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">File Upload</h1>
      <Import id={id} />
    </div>
  );
};

export default FileUploader;
