import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { FaCamera, FaFolder, FaSearch } from "react-icons/fa";
import { MdComputer, MdInfo, MdNetworkWifi, MdSettings } from "react-icons/md";
import { getVictim, runVictimCommand } from "../../service/api.service";
import Terminal from "../../components/Terminal";

const ClientDetail: React.FC = () => {
  const [tab, setTab] = useState("detail");
  const [client, setClient] = useState<Victim>();
  const location = useLocation();

  useEffect(() => {
    const fetchClient = async () => {
      // Example URL: http://localhost:5173/dashboard#client?id=119384632345157

      // Extract the hash part of the URL
      const hash = location.hash;

      // Use a regular expression to find the 'id' query parameter in the hash
      const match = hash.match(/id=([^&]+)/);

      if (match) {
        // Extract the 'id' value from the matched result
        const clientId = match[1];

        const response = await getVictim(clientId);
        setClient(response.data.client);
      }
    };

    fetchClient();
  }, [location]);

  /*const client = {
    id: 1,
    name: "Client 1",
    ipAddress: "127.0.0.1",
    isActive: true,
    platform: "Windows 10",
    vitalInfo: "High vulnerability discovered, exploit available.",
    osVersion: "10.0.19042",
    uptime: "5 days 3 hours",
    idleTime: "15 minutes",
    status: "Online",
    latency: "32 ms",
    privilege: "Admin",
    version: "1.0.0",
  };*/

  return (
    <div className="container mx-auto">
      <div className="bg-white dark:bg-gray-900 rounded-lg p-4 shadow-md">
        <div className="flex items-center justify-between">
          {/* Header with client status */}
          <div className="flex items-center">
            {/* Status Wheel */}
            <div className="w-16 h-16 rounded-full border-8 border-red-500 flex items-center justify-center">
              <div
                className={`w-10 h-10 rounded-full ${
                  "Online".toLowerCase() === "online"
                    ? "bg-green-500"
                    : "bg-red-500"
                }`}
              ></div>
            </div>
            <div className="ml-4">
              <h2 className="text-2xl font-semibold text-blue-700 dark:text-blue-300">
                {client?.Name}
              </h2>
              <p className="text-gray-500 dark:text-gray-400">
                IP Address: {client?.IPv4}
              </p>
            </div>
          </div>
          {/* Additional Information */}
          <div className="flex items-center">
            <div className="mr-4">
              <MdComputer
                size={24}
                className="text-gray-600 dark:text-gray-400"
              />
              <span className="text-sm text-gray-600 dark:text-gray-400 ml-1">
                {client?.System}
              </span>
            </div>
            <div>
              <MdInfo size={24} className="text-red-500" />
              <span className="text-sm text-red-500 ml-1">
                Dangerous Vulnerability
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-row mt-4 gap-x-2 w-full mx-auto justify-center">
        <button
          onClick={() => setTab("detail")}
          className={`py-2 px-4 hover:bg-blue-600 hover:text-white rounded-sm ${
            tab === "detail" ? "bg-blue-600 text-white" : ""
          }`}
        >
          Details
        </button>
        <button
          onClick={() => setTab("system")}
          className={`py-2 px-4 hover:bg-blue-600 hover:text-white rounded-sm ${
            tab === "system" ? "bg-blue-600 text-white" : ""
          }`}
        >
          System
        </button>

        <button
          onClick={() => setTab("terminal")}
          className={`py-2 px-4 hover:bg-blue-600 hover:text-white rounded-sm ${
            tab === "terminal" ? "bg-blue-600 text-white" : ""
          }`}
        >
          Terminal
        </button>
        {/* Render content based on the tab */}
      </div>

      {tab === "detail" && (
        <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div className="col-span-1 sm:col-span-2">
            <h1 className="text-xl font-bold">
              <MdComputer className="inline text-blue-700 dark:text-blue-300" />{" "}
              System Info:
            </h1>
            <div className="bg-white dark:bg-gray-900 rounded-lg p-4 shadow-md mt-4">
              <p className="text-gray-500 dark:text-gray-400">
                Computer Name: {client?.Name}
              </p>
              <p className="text-gray-500 dark:text-gray-400">
                OS Platform: {client?.System}
              </p>
              <p className="text-gray-500 dark:text-gray-400">
                OS Version: {client?.Version}
              </p>
              <p className="text-gray-500 dark:text-gray-400">
                System Uptime: {client?.Uptime}
              </p>
              <p className="text-gray-500 dark:text-gray-400">
                Idle Time: 50 minutes
              </p>
            </div>
          </div>
          <div className="col-span-1">
            <h1 className="text-xl font-bold">
              <MdNetworkWifi className="inline text-blue-700 dark:text-blue-300" />{" "}
              Network Info:
            </h1>
            <div className="bg-white dark:bg-gray-900 rounded-lg p-4 shadow-md mt-4">
              <p className="text-gray-500 dark:text-gray-400">
                Status:{" "}
                <span
                  className={`${
                    "Online".toLowerCase() === "online"
                      ? "text-green-500"
                      : "text-red-500 "
                  }`}
                >
                  Online
                </span>
              </p>
              <p className="text-gray-500 dark:text-gray-400">
                Latency:{" "}
                <span
                  className={`
                  ${parseInt("32") < 50 && "text-green-500"}
                  ${
                    parseInt("32") > 50 &&
                    parseInt("32") < 99 &&
                    "text-yellow-500"
                  }
                  ${32 > 99 && "text-red-500"}
                `}
                >
                  32
                </span>
              </p>
              <p className="text-gray-500 dark:text-gray-400">
                IP Address: {client?.IPv4}
              </p>
            </div>
          </div>
          <div className="col-span-1">
            <h1 className="text-xl font-bold">
              <MdSettings className="inline text-blue-700 dark:text-blue-300" />{" "}
              Rat-Ted Settings:
            </h1>
            <div className="bg-white dark:bg-gray-900 rounded-lg p-4 shadow-md mt-4">
              <p className="text-gray-500 dark:text-gray-400">
                Privilege Level: {client?.Privileges}
              </p>
              <p className="text-gray-500 dark:text-gray-400">
                Rat-Ted Version: {client?.RatTedVersion}
              </p>
            </div>
          </div>
        </div>
      )}

      {tab === "system" && (
        <div>
          <div className="grid grid-cols-3 gap-x-6">
            {/* Buttons such as Screen Capture, File Manager, File Search, Process Manager, Service Manager and so on */}

            <div className="bg-white dark:bg-gray-900 rounded-lg p-4 shadow-md mt-4">
              <div className="flex items-center">
                <FaCamera className="text-3xl mr-2 text-blue-600 dark:text-blue-400" />
                <div>
                  <h1 className="text-xl font-bold">Screen Capture:</h1>
                  <p className="text-gray-500 dark:text-gray-400">
                    Capture their screen in real-time:
                  </p>
                </div>
              </div>
              <button className="py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-sm mt-4">
                Start Screen Capture
              </button>
            </div>

            <div className="bg-white dark:bg-gray-900 rounded-lg p-4 shadow-md mt-4">
              <div className="flex items-center">
                <FaFolder className="text-3xl mr-2 text-green-600 dark:text-green-400" />
                <div>
                  <h1 className="text-xl font-bold">File Manager:</h1>
                  <p className="text-gray-500 dark:text-gray-400">
                    Browse their files:
                  </p>
                </div>
              </div>
              <button className="py-2 px-4 bg-green-600 hover:bg-green-700 text-white rounded-sm mt-4">
                Open File Manager
              </button>
            </div>

            <div className="bg-white dark:bg-gray-900 rounded-lg p-4 shadow-md mt-4">
              <div className="flex items-center">
                <FaSearch className="text-3xl mr-2 text-purple-600 dark:text-purple-400" />
                <div>
                  <h1 className="text-xl font-bold">File Search:</h1>
                  <p className="text-gray-500 dark:text-gray-400">
                    Search their files:
                  </p>
                </div>
              </div>
              <button className="py-2 px-4 bg-purple-600 hover:bg-purple-700 text-white rounded-sm mt-4">
                Open File Search
              </button>
            </div>
          </div>
        </div>
      )}

      {tab === "terminal" && (
        <div className="mt-4">
          <Terminal id={client?.ID || ""} />
        </div>
      )}
    </div>
  );
};

export default ClientDetail;
