
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useLocation, createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import Navbar from './pages/Welcome/components/navbar.tsx';
import HeroSection from './pages/Welcome/components/HeroSection.tsx';
import Login from './pages/Login/Login.tsx';
import Register from './pages/Register/Register.tsx';
import Home from './pages/Home/Home.tsx';
import Devices from './pages/Devices/devices.tsx';
import NotificationPage from './pages/Notification/notification.tsx';
import Setting from './pages/Setting/Settings.tsx';
import Auth from './pages/authentication/authentication.tsx';
import Profile from './pages/Profile/Profile.tsx';
import Layout from  './Layout.tsx';
import ErrorPage from './ErrorPage.tsx'; // Tạo một component ErrorPage
import './app.css';


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
const ProtectedRoute = ({children}) => {
  const isAuthenticated = !!localStorage.getItem('access_token');

  return isAuthenticated ? children : <Navigate to="/login" />;
}
const router = createBrowserRouter(
  [
      { path: "/", element: <App />,
        errorElement: <ErrorPage />, // Hiển thị trang lỗi tùy chỉnh
       },
      { path: "/login", element: <Login /> },
      { path: "/register", element: <Register /> },
      {
          path: "/",
          element: <ProtectedRoute><Layout /></ProtectedRoute>, // Layout chứa Sidebar
          children: [
              { path: "home", element: <Home /> },
              { path: "devices", element: <Devices /> },
              { path: "notifications", element: <NotificationPage /> },
              { path: "settings", element: <Setting /> },
              { path: "auth", element: <Auth /> },
              { path: "profile", element: <Profile /> },

          ],
      },
  ],
  {
      future: {
          v7_relativeSplatPath: true,
      },
  }
);

function AppWrapper() {
  return <RouterProvider router={router} />;
}

export default AppWrapper;
