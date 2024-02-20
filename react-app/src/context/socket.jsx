import { io } from "socket.io-client";

const URL =
  process.env.NODE_ENV == "production"
    ? "wss://serenity-chat.onrender.com"
    : "localhost:5000";

console.log(URL);

export const socket = io(URL, {
  // autoConnect: false,
  transports: ["websocket", "polling"],
});
