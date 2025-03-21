import React, { createContext, useContext, useState, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { ChevronFirst, ChevronLast, MoreVertical } from 'lucide-react';
import Header from "../../components/common/Header.tsx";
import axios from "axios";

const SidebarContext = createContext({ isExpanded: true });

const getInitials = (firstName, lastName) => {
    const firstInitial = firstName?.charAt(0)?.toUpperCase() || '';
    const lastInitial = lastName?.charAt(0)?.toUpperCase() || '';
    return `${firstInitial}${lastInitial}`;
};

const Logo = require("../../assets/image/logo.png");

export default function Sidebar({ children }) {
    const [message, setMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [isExpanded, setIsExpanded] = useState(false);
    const [userData, setUserData] = useState({
        firstName: "",
        lastName: "",
        username: "",
        email: "",
        phone: "",
        address: "",
    });
    const [showProfileMenu, setShowProfileMenu] = useState(false);
    const navigate = useNavigate();
    const location = useLocation(); // Lấy thông tin URL hiện tại

    useEffect(() => {
        const fetchUserData = async () => {
            setIsLoading(true);
            try {
                const response = await axios.get("https://do-an-da-nganh.onrender.com/api/users/info", {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                    },
                });
                console.log("API Response:", response.data);
                if (response.data.status == 201) {
                    setUserData(response.data.data);
                } else {
                    setMessage("Không thể tải thông tin người dùng.");
                }
            } catch (error) {
                console.error("Lỗi khi lấy thông tin user:", error);
                setMessage(error.response?.data?.message || "Đã xảy ra lỗi khi tải thông tin.");
            } finally {
                setIsLoading(false);
            }
        };
        fetchUserData();
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('persist:root');
        navigate('/login');
        setShowProfileMenu(false);
    };

    const userInitials = getInitials(userData.firstName, userData.lastName);
    const toggleSidebar = () => setIsExpanded((prev) => !prev);

    return (
        <div>
            <Header toggleSidebar={toggleSidebar} />
            <aside className="h-screen">
                <nav className={`fixed top-0 left-0 z-40 pt-20 h-full flex flex-col bg-white border-r shadow-sm lg:translate-x-0 transition-transform ${isExpanded ? "translate-x-0" : "-translate-x-full"}`}>
                    <SidebarContext.Provider value={{ isExpanded }}>
                        <ul className="flex-1 px-3">
                            {React.Children.map(children, (child) =>
                                React.cloneElement(child, {
                                    active: child.props.to === location.pathname, 
                                })
                            )}
                        </ul>
                    </SidebarContext.Provider>

                    {/* Profile section với dropdown */}
                    <div className="border-t flex p-3 relative">
                        <div
                            className="flex items-center cursor-pointer"
                            onClick={() => setShowProfileMenu(!showProfileMenu)}
                        >
                            <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center border border-gray-300">
                                <span className="text-lg font-semibold text-indigo-800">
                                    {userInitials || "U"}
                                </span>
                            </div>
                            <div className={`flex justify-between items-center overflow-hidden transition-all ${isExpanded ? "w-52 ml-3" : "w-0"}`}>
                                <div className="leading-4">
                                    <h4 className="font-semibold">{userData.firstName} {userData.lastName}</h4>
                                    <span className="text-xs text-gray-600">{userData.email}</span>
                                </div>
                                <MoreVertical size={20} />
                            </div>
                        </div>

                        {showProfileMenu && (
                            <div className="absolute bottom-full left-0 mb-2 w-48 bg-white rounded-md shadow-lg border border-gray-100">
                                <Link
                                    to="/profile"
                                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                    onClick={() => setShowProfileMenu(false)}
                                >
                                    Profile
                                </Link>
                                <button
                                    onClick={handleLogout}
                                    className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                >
                                    Logout
                                </button>
                            </div>
                        )}
                    </div>
                </nav>
            </aside>
        </div>
    );
}

export function SidebarItem({ icon, text, active, alert, to }) {
    const { isExpanded } = useContext(SidebarContext);
    const navigate = useNavigate();

    const handleClick = () => {
        if (to) {
            navigate(to);
        }
    };

    return (
        <li
            onClick={handleClick}
            className={`
                relative flex items-center py-2 px-3 my-1
                font-medium rounded-md cursor-pointer
                transition-colors group
                ${
                    active
                        ? "bg-gradient-to-tr from-indigo-200 to-indigo-100 text-indigo-800"
                        : "hover:bg-indigo-50 text-gray-600"
                }
            `}
        >
            {icon}
            <span className={`overflow-hidden transition-all ${isExpanded ? "w-52 ml-3" : "w-0"}`}>
                {text}
            </span>
            {alert && (
                <div className={`absolute right-2 w-2 h-2 rounded bg-indigo-400 ${isExpanded ? "" : "top-2"}`} />
            )}
            {!isExpanded && (
                <div
                    className={`
                        absolute left-full rounded-md px-2 py-1 ml-6
                        bg-indigo-100 text-indigo-800 text-sm
                        invisible opacity-20 -translate-x-3 transition-all
                        group-hover:visible group-hover:opacity-100 group-hover:translate-x-0
                    `}
                >
                    {text}
                </div>
            )}
        </li>
    );
}
