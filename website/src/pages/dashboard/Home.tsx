import React from "react";
import { Link } from "react-router-dom";

const Home: React.FC = () => {
  return (
    <>
      <h2 className="text-lg font-semibold text-blue-700 dark:text-blue-300 mb-4">
        Welcome back, John Doe
      </h2>

      <div className="w-full h-full">
        {/* Make the grids at right bigger then the left */}
        <div className="grid grid-cols-3 grid-rows-3 gap-6">
          {/* Stat Cards */}
          <div className="flex flex-row justify-between items-center gap-4 col-span-2">
            <div className="bg-blue-200 dark:bg-gray-800 rounded-lg p-4 shadow-md w-full h-full">
              <h2 className="text-3xl font-semibold text-blue-800 dark:text-blue-200 mb-4">
                1000
              </h2>
              <p className="text-gray-600 dark:text-gray-300">Total Clients</p>
            </div>

            <div className="bg-green-200 dark:bg-gray-800 rounded-lg p-4 shadow-md w-full h-full">
              <h2 className="text-3xl font-semibold text-green-800 dark:text-green-200 mb-4">
                500
              </h2>
              <p className="text-gray-600 dark:text-gray-300">Active Clients</p>
            </div>

            <div className="bg-red-200 dark:bg-gray-800 rounded-lg p-4 shadow-md w-full h-full">
              <h2 className="text-3xl font-semibold text-red-800 dark:text-red-200 mb-4">
                200
              </h2>
              <p className="text-gray-600 dark:text-gray-300">
                Offline Clients
              </p>
            </div>
          </div>

          {/* Feature Card */}
          <div className="bg-white dark:bg-gray-800 border border-green-500 rounded-lg p-4 shadow-md">
            <h2 className="text-lg font-semibold text-blue-700 dark:text-blue-300 mb-4">
              Newest Features
            </h2>
            <Link
              to="/dashboard/news"
              className="text-blue-600 dark:text-blue-300 hover:underline"
            >
              View all features
            </Link>
          </div>

          {/* Graph Placeholder */}
          <div className="bg-white dark:bg-gray-800 border border-green-500 rounded-lg p-4 shadow-md col-span-2"></div>

          {/* Quick Actions Sidebar */}
          <div className="bg-white dark:bg-gray-800 border border-green-500 rounded-lg p-4 shadow-md col-span-2">
            <h2 className="text-lg font-semibold text-blue-700 dark:text-blue-300 mb-4">
              Quick Actions
            </h2>
            <Link
              to="/dashboard/news"
              className="text-blue-600 dark:text-blue-300 hover:underline"
            >
              View all features
            </Link>
          </div>

          <div className="bg-white dark:bg-gray-800 border border-green-500 rounded-lg p-4 shadow-md col-start-3 row-span-2 row-start-2">
            <h2 className="text-lg font-semibold text-blue-700 dark:text-blue-300 mb-4">
              Something else here
            </h2>
            <Link
              to="/dashboard/news"
              className="text-blue-600 dark:text-blue-300 hover:underline"
            >
              View all features
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;
