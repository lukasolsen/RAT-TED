import axios from "axios";

const API_URL = "http://127.0.0.1:8001/api/v1/";

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

export const fileUpload = (file: File) => {
  const formData = new FormData();
  formData.append("in_file", file);
  return axios
    .post(API_URL + "upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    })
    .then((response) => {
      return response;
    });
};
