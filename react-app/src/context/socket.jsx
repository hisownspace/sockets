import { io } from "socket.io-client";

const URL =
  process.env.NODE_ENV == "production" ? "undefined" : "localhost:5000";

console.log(URL);

export const socket = io(URL, { transports: ["polling", "websocket"] });
