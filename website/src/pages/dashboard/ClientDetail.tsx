import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { FaCamera, FaFolder, FaSearch } from "react-icons/fa";
import { getVictim } from "../../service/api.service";
import Terminal from "../../components/Terminal";
import NotFound from "../404";
import Header from "./sections/Header";
import Details from "./sections/Details";
import ScreenCapture from "./systemSections/ScreenCapture";

const ClientDetail: React.FC = () => {
  const [tab, setTab] = useState("detail");
  const [systemTab, setSystemTab] = useState(""); // ["screen-capture", "file-manager", "file-search"]
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

  return (
    <div className="container mx-auto">
      {client?.ID && (
        <>
          <Header client={client} />

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

          {tab === "detail" && <Details client={client} />}

          {tab === "system" && (
            <div>
              {systemTab === "screen-capture" && <ScreenCapture />}

              {systemTab.length === 0 && (
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
                    <button
                      className="py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-sm mt-4"
                      onClick={(e) => {
                        e.preventDefault();
                        setSystemTab("screen-capture");
                      }}
                    >
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
              )}
            </div>
          )}

          {tab === "terminal" && (
            <div className="mt-4">
              <Terminal
                id={client.ID}
                currentDirectory={client.Current_Directory}
              />
            </div>
          )}
        </>
      )}

      {!client?.ID && <NotFound />}
    </div>
  );
};

export default ClientDetail;
