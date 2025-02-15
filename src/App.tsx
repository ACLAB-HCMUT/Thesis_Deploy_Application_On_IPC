// import React from 'react';
// import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';
// import Navbar from './pages/Welcome/components/navbar.tsx';
// import HeroSection from './pages/Welcome/components/HeroSection.tsx';
// import Login from './pages/Login/Login.tsx';
// import Register from './pages/Register/Register.tsx';
// import Home from './pages/Home/Home.tsx';
// import Devices from './pages/Devices/devices.tsx';
// import './app.css';

// function App() {
//   const location = useLocation();

//   return (
//     <div
//     className="relative w-full h-screen welcome"
//   >
//     <div className="absolute top-0 left-0 w-full h-full bg-black opacity-35 z-10"></div>
//     <div className="relative z-20">
//       <Navbar />
//       <HeroSection />
//     </div>
//   </div>

//   );
// }

// function AppWrapper() {
//   return (
//     <Router>
//       <Routes>
//         {/* Trang mặc định */}
//         <Route path="/" element={<App />} />
//         {/* Các route cho Login và Register */}
//         <Route path="/login" element={<Login />} />
//         <Route path="/register" element={<Register />} />
//         <Route path="/home" element={<Home/>} />
//         <Route path="/devices" element={<Devices/>} />
//       </Routes>
//     </Router>
//   );
// }

// export default AppWrapper;
import React from "react";
import {
  createBrowserRouter,
  RouterProvider
} from "react-router-dom";
import Navbar from "./pages/Welcome/components/navbar.tsx";
import HeroSection from "./pages/Welcome/components/HeroSection.tsx";
import Login from "./pages/Login/Login.tsx";
import Register from "./pages/Register/Register.tsx";
import Home from "./pages/Home/Home.tsx";
import Devices from "./pages/Devices/devices.tsx";
import "./app.css";

function App() {
  return (
    <div className="relative w-full h-screen welcome">
      <div className="absolute top-0 left-0 w-full h-full bg-black opacity-35 z-10"></div>
      <div className="relative z-20">
        <Navbar />
        <HeroSection />
      </div>
    </div>
  );
}

const router = createBrowserRouter(
  [
    { path: "/", element: <App /> },
    { path: "/login", element: <Login /> },
    { path: "/register", element: <Register /> },
    { path: "/home", element: <Home /> },
    { path: "/devices", element: <Devices /> },
  ],
  {
    future: {
      v7_relativeSplatPath: true, // ✅ Bật flag v7 để tránh cảnh báo
    },
  }
);

function AppWrapper() {
  return <RouterProvider router={router} />;
}

export default AppWrapper;
