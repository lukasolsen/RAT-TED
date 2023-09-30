import React from "react";
import { useTable } from "react-table";

const Clients: React.FC = () => {
  const data = React.useMemo(
    () => [
      {
        clientName: "Client 1",
        ipAddress: "192.168.1.1",
        active: "Yes",
      },
      {
        clientName: "Client 2",
        ipAddress: "192.168.1.2",
        active: "No",
      },
      // Add more client data as needed
    ],
    []
  );

  // Define table columns
  const columns = React.useMemo(
    () => [
      {
        Header: "Client Name",
        accessor: "clientName",
      },
      {
        Header: "IP Address",
        accessor: "ipAddress",
      },
      {
        Header: "Active",
        accessor: "active",
        Cell: ({ row }: any) => (
          <span
            className={`${
              row.values.active === "Yes" ? "text-green-500" : "text-red-500"
            }`}
          >
            {row.values.active}
          </span>
        ),
      },
      {
        Header: "Actions",
        accessor: "actions",
        Cell: ({ row }: any) => (
          <button className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg">
            View
          </button>
        ),
      },
    ],
    []
  );

  // Create a table instance
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable({ columns, data });

  return (
    <div className="container mx-auto p-6">
      <div className="bg-white dark:bg-gray-900 rounded-lg p-4 shadow-md">
        <h2 className="text-lg font-semibold text-blue-700 dark:text-blue-300 mb-4">
          Clients
        </h2>

        {/* React Table */}
        <table {...getTableProps()} className="w-full">
          <thead>
            {headerGroups.map((headerGroup: any) => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map((column: any) => (
                  <th {...column.getHeaderProps()} className="text-left">
                    {column.render("Header")}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody {...getTableBodyProps()}>
            {rows.map((row: any) => {
              prepareRow(row);
              return (
                <tr {...row.getRowProps()}>
                  {row.cells.map((cell: any) => {
                    return (
                      <td {...cell.getCellProps()} className="py-2">
                        {cell.render("Cell")}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Clients;
