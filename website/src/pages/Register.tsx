import React from "react";
import { AiOutlineUser, AiOutlineMail, AiOutlineLock } from "react-icons/ai";
import { register } from "../service/api.service";

const Register: React.FC = () => {
  const [username, setUsername] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");

  const submit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const register_onclick = async () => {
      return register(username, email, password);
    };

    const response = register_onclick();

    response.then((data) => {
      if (data.status === 200) {
        console.log("Register successful");
        window.location.href = "/";
      }
    });
  };

  return (
    <div className="h-screen flex flex-row justify-center items-center">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg text-center h-2/4 w-4/12">
        <h1 className="text-3xl font-semibold text-green-500 mb-6">
          Create Your Spotify Stats Account
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
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="flex flex-col space-y-2">
            <label className="text-green-500 flex items-center">
              <AiOutlineMail className="mr-2" /> Email
            </label>
            <input
              type="email"
              placeholder="Enter your email"
              className="p-2 rounded-lg bg-gray-100 text-black"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button
            type="submit"
            className="bg-green-600 hover:bg-green-700 text-white p-2 rounded-lg transition-all duration-300"
          >
            Register
          </button>
        </form>
        <p className="text-gray-400 mt-4">
          By registering, you agree to our{" "}
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
      <div className="bg-green-700 p-8 rounded-lg shadow-lg text-center h-2/4 w-4/12">
        <h1 className="text-3xl font-semibold text-white mb-2">
          Spotify Stats
        </h1>
        <p className="text-gray-300 mb-6">
          Spotify Stats is a web application that allows you to see your Spotify
          statistics.
        </p>
        <ul className="text-white mt-4">
          <li className="flex flex-row space-x-2 items-center mb-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 text-green-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
            <span>Able to export and import your data</span>
          </li>
          <li className="flex flex-row space-x-2 items-center mb-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 text-green-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
            <span>Discover your most played tracks and artists</span>
          </li>
          <li className="flex flex-row space-x-2 items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 text-green-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
            <span>Visualize your listening habits</span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Register;
