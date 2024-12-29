import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';
import logo from '../../../assets/image/logo.png';


function Navbar() {
  return (
    <header className="absolute top-0 left-0 w-full flex justify-between items-center p-4 bg-white bg-opacity-25">
      <div className="text-white text-2xl font-bold ml-2.5">
        <img src={logo} className="w-[69px] h-[43px]"/>
      </div>
      <nav>
      <div>
      <Link
        to="/login"
        className="w-full mx-2 px-4 py-2 border-white bg-white rounded-full font-bold hover:bg-gray-200 hover:text-black transition text-[12px] bg-opacity-40 text-white hover:text-black transition-all duration-500">
        LOGIN
      </Link>
      
      <Link
        to="/register"
        className="w-full mx-2 px-4 py-2 border-white bg-white rounded-full font-bold hover:bg-gray-200 hover:text-black transition text-[12px] bg-opacity-40 text-white hover:text-black transition-all duration-500"
      >
        SIGN UP
      </Link>
    </div>
      </nav>
    </header>
  );
};

export default Navbar;
