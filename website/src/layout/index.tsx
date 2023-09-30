import { Outlet, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import { useEffect } from "react";
import { useAuth } from "../context/AuthContext";

const Layout: React.FC = () => {
  const pathname = useLocation().pathname;
  const { checkToken, isLoggedIn } = useAuth();

  useEffect(() => {
    // check if they are logged in
    /*const getData = async () => {
      const token = localStorage.getItem("token");

      if (token) {
        return await verifyToken(token);
      }
    };

    const response = getData();
    response.then((data) => {
      if (!data) return;
      console.log(data);
      if (data.status === 200) {
        if (pathname === "/login" || pathname === "/register")
          window.location.href = "/";
        setLoggedIn(true);
      } else {
        setLoggedIn(false);
      }
    });*/

    checkToken();
  }, []);

  return (
    <>
      <div className="dark:bg-gray-900 dark:text-white text-black bg-slate-100 overscroll-auto h-full min-h-screen break-all">
        {!pathname.includes("/profile") && <Navbar hasAccount={isLoggedIn} />}
        <Outlet />
      </div>
    </>
  );
};

export default Layout;
