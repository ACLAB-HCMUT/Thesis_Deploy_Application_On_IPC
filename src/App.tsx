import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';
import Navbar from './pages/Welcome/components/navbar.tsx';
import HeroSection from './pages/Welcome/components/HeroSection.tsx';
import Login from './pages/Login/Login.tsx';
import Register from './pages/Register/Register.tsx';
import Home from './pages/Home/Home.tsx';
import './app.css';

function App() {
  const location = useLocation();

  return (
    <div
    className="relative w-full h-screen welcome"
  >
    <div className="absolute top-0 left-0 w-full h-full bg-black opacity-35 z-10"></div>
    <div className="relative z-20">
      <Navbar />
      <HeroSection />
    </div>
  </div>

  );
}

function AppWrapper() {
  return (
    <Router>
      <Routes>
        {/* Trang mặc định */}
        <Route path="/" element={<App />} />
        {/* Các route cho Login và Register */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/home" element={<Home/>} />
      </Routes>
    </Router>
  );
}

export default AppWrapper;
