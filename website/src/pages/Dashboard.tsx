import React, { useEffect } from "react";
import Clients from "./dashboard/Clients";
import Home from "./dashboard/Home";
import ClientDetail from "./dashboard/ClientDetail";

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
    <div className="flex h-screen dark:bg-slate-900">
      {/* Sidebar */}
      <aside className="w-1/5 dark:bg-slate-950 text-white overflow-y-auto transition-transform duration-300 transform -translate-x-full dark:translate-x-0">
        <nav className="p-4 space-y-2">
          {/* Sidebar links */}
          <button
            onClick={() => changeTab("home")}
            className={`block py-2 px-4 hover:bg-blue-600 hover:text-white ${
              tab === "home" ? "bg-blue-600 text-white" : ""
            }`}
          >
            Dashboard
          </button>
          <button
            onClick={() => changeTab("clients")}
            className={`block py-2 px-4 hover:bg-blue-600 hover:text-white ${
              tab === "clients" ? "bg-blue-600 text-white" : ""
            }`}
          >
            Clients
          </button>
          <button
            onClick={() => changeTab("settings")}
            className={`block py-2 px-4 hover:bg-blue-600 hover:text-white ${
              tab === "settings" ? "bg-blue-600 text-white" : ""
            }`}
          >
            Settings
          </button>
        </nav>
      </aside>

      {/* Main content */}
      <main className="flex-1 ml-0 sm:ml-1/5 transition-transform duration-300 transform">
        <header className="py-4 ">
          <div className="container mx-auto">
            <h1 className="text-2xl text-white">Dashboard</h1>
          </div>
        </header>

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
