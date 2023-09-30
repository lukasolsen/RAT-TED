import { createContext, useContext, useState } from "react";
import { verifyToken } from "../service/api.service";

// Create a new context
type AuthContextType = {
  isLoggedIn: boolean;
  userDetails: any;
  checkToken: () => void;
  isLoading: boolean;
};

const AuthContext = createContext({} as AuthContextType);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userDetails, setUserDetails] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // You can define functions to update the state here if needed

  const checkToken = () => {
    setIsLoading(true);
    const token = localStorage.getItem("token");

    verifyToken(token!)
      .then((data) => {
        if (!data) return;
        if (data.status === 200) {
          console.log("Logged in");
          setIsLoggedIn(true);
          setUserDetails(data.data);
        } else {
          setIsLoggedIn(false);
        }
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  // Provide the context values to the components
  const contextValue = {
    isLoggedIn,
    userDetails,
    checkToken,
    isLoading,
  };

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
