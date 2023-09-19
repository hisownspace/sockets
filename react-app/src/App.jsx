import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import { Route, Routes, BrowserRouter } from "react-router-dom";
import Login from "./Components/Login";
import Chat from "./Components/Chat";
import Room from "./Components/Room";

function App() {
  return (
    <BrowserRouter>
      <Login />
      <Routes>
        <Route path="/" element={<Chat />}>
          <Route path=":roomId" element={<Room />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
