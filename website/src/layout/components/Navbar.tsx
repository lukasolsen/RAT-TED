import { Link, useLocation } from "react-router-dom";

type NavbarProps = {
  hasAccount: boolean;
};

const Navbar: React.FC<NavbarProps> = ({ hasAccount }) => {
  const location = useLocation();

  return (
    <>
      {location.pathname.includes("/login") ||
      location.pathname.includes("/register") ? null : (
        <div className="flex flex-row justify-between items-center w-full p-4 pt-2 dark:text-white text-black border-b border-b-red-400">
          <Link to={"/"}>
            <h1 className="text-2xl font-bold text-red-500">Rat-Ted</h1>
          </Link>

          <div className="flex flex-row space-x-4 items-center">
            <Link
              to="/"
              className={`${location.pathname === "/" ? "text-red-400" : ""}`}
            >
              Home
            </Link>

            <Link
              to="/dashboard"
              className={`${
                location.pathname === "/dashboard" ? "text-red-400" : ""
              }`}
            >
              Dashboard
            </Link>
          </div>

          {!hasAccount && (
            <div className="flex flex-row space-x-4 items-center">
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </div>
          )}
        </div>
      )}
    </>
  );
};

export default Navbar;
