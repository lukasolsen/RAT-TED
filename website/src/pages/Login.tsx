import React from "react";
import { AiOutlineUser, AiOutlineLock } from "react-icons/ai";
import { login } from "../service/api.service";

const Login: React.FC = () => {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");

  const submit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const login_onclick = async () => {
      return login(username, password);
    };

    const response = login_onclick();
    response.then((data) => {
      if (data.status === 200) {
        console.log("Login successful");
        localStorage.setItem("token", data.data.access_token);
        window.location.href = "/";
      }
    });
  };

  return (
    <div className="h-screen flex flex-col justify-center items-center">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg text-center h-2/4 w-4/12">
        <h1 className="text-3xl font-semibold text-green-500 mb-6">
          Sign In to your Account
        </h1>
        <form className="space-y-4" onSubmit={submit}>
          <div className="flex flex-col space-y-2">
            <label className="text-green-500 flex items-center">
              <AiOutlineUser className="mr-2" /> Username
            </label>
            <input
              type="text"
              placeholder="Enter your username"
              className="p-2 rounded-lg bg-gray-100 text-black"
              autoComplete="on"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="flex flex-col space-y-2">
            <label className="text-green-500 flex items-center">
              <AiOutlineLock className="mr-2" /> Password
            </label>
            <input
              type="password"
              placeholder="Enter your password"
              className="p-2 rounded-lg bg-gray-100 text-black"
              autoComplete="on"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button
            type="submit"
            className="bg-green-600 hover:bg-green-700 text-white p-2 rounded-lg transition-all duration-300"
          >
            Log In
          </button>
        </form>
        <p className="text-gray-400 mt-4">
          By logging in, you agree to our{" "}
          <a className="text-green-500 hover:underline" href="#">
            Terms of Service
          </a>{" "}
          and{" "}
          <a className="text-green-500 hover:underline" href="#">
            Privacy Policy
          </a>
          .
        </p>
      </div>
    </div>
  );
};

export default Login;
