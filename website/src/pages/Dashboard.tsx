import React, { useEffect } from "react";
import Clients from "./dashboard/Clients";
import Home from "./dashboard/Home";
import ClientDetail from "./dashboard/ClientDetail";
import { FaHome, FaUsers, FaCog } from "react-icons/fa";

const Dashboard: React.FC = () => {
  // Function to update the tab based on the URL hash
  const updateTabFromHash = () => {
    const hash = window.location.hash.substr(1); // Remove the '#' character
    setTab(hash || "home"); // Use 'home' as the default tab if no hash is provided
  };

  // Use useEffect to update the tab when the hash changes
  useEffect(() => {
    window.addEventListener("hashchange", updateTabFromHash);
    updateTabFromHash(); // Initial tab setup
    return () => {
      window.removeEventListener("hashchange", updateTabFromHash);
    };
  }, []);

  // Function to change the URL hash and update the tab
  const changeTab = (newTab: string) => {
    window.location.hash = newTab;
    setTab(newTab);
  };

  // Sample data for clients
  const [tab, setTab] = React.useState("home");

  return (
    <div className="flex h-full min-h-screen dark:bg-slate-900">
      {/* Sidebar */}
      <aside className="w-1/5 dark:bg-slate-950 text-white overflow-y-auto transition-transform duration-300 transform -translate-x-full dark:translate-x-0">
        <nav className="p-4 space-y-2 w-full">
          {/* Sidebar links */}
          <button
            onClick={() => changeTab("home")}
            className={`flex items-center py-2 px-4 hover:bg-blue-600 hover:text-white w-full rounded-sm ${
              tab === "home" ? "bg-blue-600 text-white" : ""
            }`}
          >
            <FaHome className="mr-4 text-lg" /> Dashboard
          </button>
          <button
            onClick={() => changeTab("clients")}
            className={`flex items-center py-2 px-4 hover:bg-blue-600 hover:text-white w-full rounded-sm ${
              tab === "clients" ? "bg-blue-600 text-white" : ""
            }`}
          >
            <FaUsers className="mr-4 text-lg" /> Clients
          </button>
          <button
            onClick={() => changeTab("settings")}
            className={`flex items-center py-2 px-4 hover:bg-blue-600 hover:text-white w-full rounded-sm ${
              tab === "settings" ? "bg-blue-600 text-white" : ""
            }`}
          >
            <FaCog className="mr-4 text-lg" /> Settings
          </button>
        </nav>
      </aside>

      {/* Main content */}
      <main className="flex-1 transition-transform duration-300 transform container mx-auto p-4">
        {/* Render content based on the tab */}
        {tab.includes("clients") ? (
          <Clients />
        ) : tab.includes("client") ? (
          <ClientDetail />
        ) : (
          <Home />
        )}
      </main>
    </div>
  );
};

export default Dashboard;
