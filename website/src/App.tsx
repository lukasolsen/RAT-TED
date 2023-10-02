import { useAuth } from "./context/AuthContext";
import { FaChartBar } from "react-icons/fa";

const App: React.FC = () => {
  const { isLoggedIn } = useAuth();

  return (
    <>
      <div className="flex flex-row justify-between container mx-auto mt-16">
        <div className="w-6/12">
          <h1 className="text-2xl font-bold text-red-500">Rat-Ted</h1>
          <p className="text-gray-500 mt-2">
            A way to manage your finances and keep track of your spending. It's
            free and easy to use.
          </p>
          {!isLoggedIn && (
            <div className="flex flex-row space-x-4 items-center mt-8">
              <a
                href={"/register"}
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md w-6/12 text-center mx-auto"
              >
                Get Started
              </a>
            </div>
          )}

          {/* Display things such as 2 buttons for importing file, and going to dashboard */}
          {isLoggedIn && (
            <div className="flex flex-row space-x-4 items-center mt-8 justify-evenly">
              <a
                href={"/dashboard"}
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md text-center flex flex-row items-center"
              >
                <FaChartBar className="mr-2" />
                Go to Dashboard
              </a>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default App;
